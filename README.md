# LG D625 (Tegra 4i) Bootloader Patch — Recovery con firma alterada

Parche del bootloader EBT del **LG G2 Mini D625, NVIDIA Tegra 4i / T148**.
Verificado en una unidad con firmware **D62510c** el **13 de octubre de 2026**:
Android stock arranca y una recovery stock con un byte de firma alterado
arranca mediante `fastboot boot`, sin rechazo de seguridad de LG.

**Resultado: v2, dos instrucciones modificadas y tres bytes distintos.**
Fastboot reporta `unlocked: yes` y `secure: no`. La confirmación incluye la
pantalla de recovery observada por el propietario y lectura posterior de
EBT, RBL y BCT. TWRP, kernels modificados y otros firmwares no se han probado.

## Inicio rápido

Requiere el respaldo **vivo** original EBT de 860160 bytes. El archivo de
staging/USP tiene una cabecera adicional y no es una entrada equivalente.
El script valida la entrada, aplica v2 y comprueba el SHA256 de salida;
trabaja offline y no sobrescribe el respaldo ni una salida existente.

```powershell
python validate_and_patch_ebt.py bootloader-original.bin ebt-patched-v2.bin
```

| Archivo | SHA256 |
| --- | --- |
| Original vivo | `10bc066b7f99256f87b05e82b5087c5c6f815a3e865dc094169176fcc69706f7` |
| Parcheado v2 | `c2c787a409ef6fd3ea01f9225dca4f40d81cf5164de631f9bb067bf4ff43541b` |

## Instalación mediante nvflash

**Usar el flujo administrado `--download … --sync`. No editar el BCT a mano
ni instalar EBT con `dd`, `--rawdevicewrite` o una escritura de sectores.**
Nvflash actualiza el hash del bootloader y la firma del BCT. Una escritura
raw omite esa actualización y puede provocar fallback a RBL o impedir el arranque.

Se probó **nvflash 4.10.1800 original** con el servidor RAM del Wiko Wax,
el BCT original del D625 y la tabla de particiones leída del dispositivo.
El servidor Wiko y el candidato LG son archivos diferentes. No usar el
BCT Wiko ni copiar sus números de partición: en este D625 **EBT=5, RBL=4,
SOS/recovery=16**. Mantener la batería colocada al trabajar en APX.

1. Entrar en APX con Vol+ y Vol− al conectar USB. Habilitar el controlador
   APX/WinUSB correspondiente y abrir la consola como administrador.
2. Cargar el servidor en RAM y leer la tabla:

```powershell
nvflash.exe --bct bct-original-slot.cfg --getpartitiontable ptable.txt --bl wiko-bootloader-server.bin --go
```

3. Confirmar el layout y respaldar antes de instalar:

```powershell
nvflash.exe --resume --read 5 ebt-before.bin
nvflash.exe --resume --read 4 rbl-before.bin
nvflash.exe --resume --rawdeviceread 0 1024 bct-before.bin
```

La última operación es solamente lectura. Sus unidades son sectores nvflash
de **4096 bytes**. Los primeros 860160 bytes de EBT/RBL deben coincidir con
el original esperado. Conservar también el BCT original y los respaldos completos.

4. Instalar solamente EBT, conservando RBL original:

```powershell
nvflash.exe --resume --download 5 ebt-patched-v2.bin --sync
```

En la prueba, `--sync` terminó con código 0 y desapareció la conexión USB.
Reiniciar físicamente para arrancar Android. Para verificar por lectura,
entrar nuevamente en APX y repetir el bootstrap del paso 2 antes de:

```powershell
nvflash.exe --resume --read 5 ebt-after.bin
nvflash.exe --resume --read 4 rbl-after.bin
nvflash.exe --resume --rawdeviceread 0 1024 bct-after.bin
```

El candidato debe coincidir byte por byte con el inicio de EBT. RBL debe
permanecer idéntico y el BCT debe contener los metadatos nuevos coherentes.
Ver [el análisis y las verificaciones](BOOTLOADER_PATCH_ANALYSIS.md).

## Prueba de arranque

Con Android arrancado y ADB autorizado:

```powershell
adb reboot bootloader
fastboot getvar unlocked
fastboot getvar secure
fastboot boot recovery_test_badsig.img
```

La imagen de diagnóstico probada conserva kernel y ramdisk stock; tiene un
byte de su firma alterado. SHA256:
`8c55f9f3b1f3298415d4d8c83a6191a9b2e414645927a297b2c019431841575a`.
El teléfono llegó a la pantalla Android/menú de recovery. `fastboot boot`
la carga en RAM; esta prueba no instaló recovery ni borró userdata.

## Restaurar EBT original

Después del mismo bootstrap APX, instalar el original usando el flujo
administrado para restaurar también sus metadatos de integridad:

```powershell
nvflash.exe --resume --download 5 bootloader-original.bin --sync
```

No restaurar solamente el BCT original mientras queda EBT parcheado.
La [recuperación completa desde APX](https://github.com/chijure/lg-d625-tegra4i-recovery)
queda disponible con su checkpoint `recovery-v0.1.0`.

## Contenido

| Archivo | Descripción |
| --- | --- |
| `validate_and_patch_ebt.py` | Generador v2 con validación SHA256 de entrada y salida |
| `BOOTLOADER_PATCH_ANALYSIS.md` | Instrucciones, diferencias de offsets, integridad y resultados |
| `evidence/unlock-2026-10-13.json` | Evidencia sanitizada de la prueba de hardware |

Los binarios de firmware, BCT, ejecutables de terceros, dumps y registros
privados no se distribuyen en este repositorio. Utilizar respaldos propios.
El generador usa solamente la biblioteca estándar de Python.

## Referencias

- [Proyecto hermano LG E450g LK patch](https://github.com/chijure-android-system-development/lg-e450g-lk-patch): referencia de organización del repositorio.
- [NVIDIA: Flashing Tools And Protocols](https://download.nvidia.com/tegra-public-appnotes/flashing-tools.html): flujo RCM/NV3P e integridad del BCT.
- [Wiko Wax: TWRP 2.8.0.0-02](https://forum.frandroid.com/topic/203892-recovery-twrp-2800-02/): referencia histórica de APX y nvflash para Tegra 4i.
- [Wiko Wax: root y cambio de ROM](https://forum.frandroid.com/topic/241543-tuto-rooter-changer-de-rom-sur-wiko-wax-4g/): DumpWAX y uso del servidor RAM.
- [Recuperación D625 y código ARMv4T](https://github.com/chijure/lg-d625-tegra4i-recovery).
