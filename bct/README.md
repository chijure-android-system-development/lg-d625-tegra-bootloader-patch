# BCT original probado — LG D625 / D62510c

`bct-original-slot.cfg` es un **BCT binario**, pese a su extensión `.cfg`.
Contiene 5424 bytes originales, sin editar y anteriores al parche EBT v2.

| Campo | Valor |
| --- | --- |
| Dispositivo probado | LG G2 Mini D625, Tegra 4i / T148 |
| Firmware observado | D62510c, Android KOT49I |
| Fecha de recuperación y prueba | 13 de octubre de 2026 |
| Tamaño | 5424 bytes |
| SHA256 | `8583855d33606748415f65ae291a194500bab1110c8d8cc34119c59854423193` |

Se extrajo del respaldo original de la región BCT de nuestra unidad. Las
60 copias originales recuperadas contenían esta misma estructura. Se usó
como entrada para cargar el servidor RAM Wiko mediante nvflash original
4.10.1800, tanto antes como después de instalar EBT v2.

Su configuración de memoria y arranque está validada solamente en esa unidad.
No se ha comprobado compatibilidad con otras unidades D625, revisiones RAM
u otros modelos. Conservar el BCT propio antes de realizar cambios.

Desde la raíz del repositorio, comprobar en PowerShell:

```powershell
(Get-FileHash bct/bct-original-slot.cfg -Algorithm SHA256).Hash
```

En sistemas con `sha256sum`, el manifiesto se comprueba con:

```sh
sha256sum -c bct/SHA256SUMS
```

## Uso probado

Como entrada del bootstrap en APX, con la batería colocada:

```powershell
nvflash.exe --bct bct/bct-original-slot.cfg --getpartitiontable ptable.txt --bl wiko-bootloader-server.bin --go
```

Este archivo es el BCT **original**; no representa los metadatos posteriores
al parche. Instalar EBT mediante `--download 5 … --sync` permite que nvflash
actualice el hash EBT y la firma BCT. No editar este archivo ni escribirlo
directamente sobre el BCT de un teléfono que conserve EBT parcheado.
La restauración del bootloader usa también el flujo administrado descrito
en el [README principal](../README.md#restaurar-ebt-original).

La licencia MIT del repositorio corresponde al código original del proyecto.
Este BCT se publica como artefacto binario extraído del dispositivo; no es
código creado por el proyecto ni se atribuye autoría sobre su contenido.
