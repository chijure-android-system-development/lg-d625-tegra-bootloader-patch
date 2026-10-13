# nvflash Windows original usado en la prueba

Se incluye una copia sin modificar del `nvflash.exe` conservado con las
herramientas de referencia del Wiko Wax y usado en el LG D625 durante la
instalación administrada y verificación del 13 de octubre de 2026.

| Campo | Valor |
| --- | --- |
| Versión mostrada | Nvflash 4.10.1800 |
| Formato | Windows PE, x86 de 32 bits |
| Tamaño | 550912 bytes |
| SHA256 | `000fa264d6614a1d3490b81c0e8fba5a72b0f70e74ca8141e108229dc7fab466` |

Es el ejecutable **original**. Las versiones experimentales `PATCHED`,
`PLLM` y similares de la investigación anterior no están incluidas.

Desde la raíz del repositorio:

```powershell
(Get-FileHash tools/nvflash.exe -Algorithm SHA256).Hash
.\tools\nvflash.exe --cmdhelp --download
```

La ayuda se ejecuta sin conexión al teléfono. Sus importaciones PE directas
son `KERNEL32.dll` y `SETUPAPI.dll`, bibliotecas del sistema Windows. La ayuda
se comprobó desde esta carpeta sin las DLL NVIDIA del directorio de trabajo
original. La prueba real previa utilizó este mismo ejecutable con su entorno
de trabajo original; no se ha repetido la instalación desde una máquina limpia.

El controlador APX/WinUSB, el servidor Wiko cargado con `--bl` y el respaldo
LG original siguen siendo insumos separados. Incluir nvflash no incluye ese
servidor RAM ni sustituye al controlador USB. Ver la instalación del
[README principal](../README.md#instalación-mediante-nvflash).

## Procedencia y licencia

Nvflash es una herramienta de NVIDIA; este proyecto no es su autor. La
licencia MIT del repositorio se aplica al código original del proyecto,
no concede una licencia nueva sobre este ejecutable de terceros. El archivo
se conserva íntegro, identificado por hash, como herramienta de la prueba.

Referencias: [NVIDIA: Flashing Tools And Protocols](https://download.nvidia.com/tegra-public-appnotes/flashing-tools.html)
y [tutorial Wiko Wax con nvflash 4.10.1800](https://forum.frandroid.com/topic/203892-recovery-twrp-2800-02/).
