# Análisis del parche EBT v2 — LG D625

## Imagen y arquitectura

La imagen viva original tiene 860160 bytes, SHA256
`10bc066b7f99256f87b05e82b5087c5c6f815a3e865dc094169176fcc69706f7`.
Su dirección de carga/entrada es `0x80108000`. Los parches son instrucciones
Thumb del bootloader principal ARMv7. El miniloader ejecutado en el AVP es
ARMv4T; son componentes diferentes con juegos de instrucciones distintos.

El EBT de staging/USP incluye un prefijo de `0x1c` bytes. El offset histórico
`0x12600` de staging corresponde a `0x125e4` en el original vivo. El generador
rechaza otras imágenes mediante SHA256, en vez de asumir que comparten offsets.

## Dos instrucciones, tres bytes distintos

| Offset vivo | Dirección cargada | Original | v2 | Efecto |
| --- | --- | --- | --- | --- |
| `0xec5e` | `0x80116c5e` | `88 b1` | `11 e0` | CBZ R0 → B, mismo destino de continuación exitosa |
| `0x125e4` | `0x8011a5e4` | `1b d0` | `1b e0` | BEQ → B, mismo destino de continuación exitosa |

Se conservan las llamadas de verificación y sus posibles efectos secundarios.
El primer parche evita el rechazo del wrapper tras la llamada de verificación;
el segundo fuerza la continuación exitosa tras finalizar la verificación
genérica. El resultado SHA256 es
`c2c787a409ef6fd3ea01f9225dca4f40d81cf5164de631f9bb067bf4ff43541b`.

La versión v1 modificaba solamente el segundo punto. Las antiguas pruebas
con escritura raw no establecieron que el BootROM ejecutara el candidato:
podía rechazar su integridad y arrancar la otra copia original. No sirven
para concluir que v1/v2 fallan una vez instalados correctamente.

## Integridad: la instalación forma parte del método

El BootROM utiliza información de bootloaders contenida en el BCT. Modificar
EBT sin actualizar esa información puede producir fallback a RBL. Modificar
ambas copias puede dejar al teléfono sin una copia válida. El intento anterior
de editar manualmente hashes del BCT dejó el teléfono solamente en APX.

El comando probado es `nvflash --resume --download 5 <v2> --sync`, usando el
nvflash original 4.10.1800 y un servidor Wiko en RAM. La ayuda local
`--cmdhelp --download` prescribe el flujo simple para NvProduction. El teléfono
reportó modo 3 y SBK no quemado. La variante con blob y `--updatebct BLINFO`
está descrita por esa ayuda para PKC/SBK seguro; no se usó en esta unidad.

Antes de instalar, las lecturas mostraron EBT y RBL originales y las 60 copias
BCT intactas. Después de la instalación y de un nuevo bootstrap APX:

- EBT comienza con los 860160 bytes exactos de v2.
- Toda la partición RBL sigue idéntica a la lectura previa.
- Las 60 copias originales contienen el hash EBT nuevo, AES-CMAC con clave
  cero: `d32d749ea72110408fbe4861288892f2`.
- Los 60 hashes RBL permanecen idénticos a los originales.
- En la primera copia BCT del conjunto, solamente cambiaron los campos
  de 16 bytes `0x310` (firma BCT) y `0x1308` (hash EBT).
- Nvflash escribió además una copia BCT en el bloque inicial. El área BCT
  completa difiere en 5466 bytes; no se intentó mantenerla idéntica, porque
  nvflash debía actualizar su integridad.

Por tanto, conservar el BCT original como respaldo no equivale a impedir
toda modificación del BCT: la actualización administrada por nvflash fue
necesaria y funcionó. La restauración también debe usar `--download … --sync`.

## Resultado de hardware y límites

Probado en una unidad LG D625, Android KOT49I, firmware D62510c:

1. Android arrancó después de instalar el candidato.
2. Fastboot reportó `unlocked: yes` y `secure: no`.
3. `fastboot boot` aceptó la recovery stock con firma alterada.
4. El propietario confirmó la pantalla de Android/menú de recovery.
5. Se leyeron EBT/RBL/BCT y se verificaron los resultados descritos arriba.
6. El propietario confirmó el reinicio final a Android.

La evidencia prueba que esta recovery con firma inválida puede arrancar;
no establece compatibilidad de TWRP del Wiko con el D625. Tampoco se probaron
otros firmwares, kernels modificados ni todas las rutas de verificación.
No se ejecutó `fastboot oem unlock`, factory reset, reparticionado ni escritura
de fusibles. Los flags fastboot por sí solos no fueron el criterio de éxito.

Ver [la evidencia sanitizada](evidence/unlock-2026-10-13.json) y el
[checkpoint de recuperación](https://github.com/chijure/lg-d625-tegra4i-recovery/tree/recovery-v0.1.0).
