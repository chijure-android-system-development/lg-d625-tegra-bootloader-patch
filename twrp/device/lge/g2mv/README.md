# TWRP device tree - LG D625 (g2mv)

**Device**: LG G2 Mini LTE / LG-D625  
**Codename**: g2mv  
**SoC**: NVIDIA Tegra 4i  
**CPU**: ARM Cortex-A9  
**Display**: 540x960, 32 bpp  
**Recovery base**: TWRP 3.1.1 / Android 4.4

This device tree builds a bootable TWRP recovery for the LG D625. It has been
tested on real hardware by loading the image temporarily with `fastboot boot`.

| Feature | Status |
|---|---|
| Display, touch, brightness, battery | Works |
| ADB | Works |
| Internal storage (`/data/media`) | Works |
| Backup of System, Data and Boot (1945 MB, split archive) | Works, MD5 verified |
| Backup of LG/Icera partitions (MDM, CST, MPT, ...) | Works, matches raw `dd` dumps |
| Restore of Boot, System (split archive) and Data | Works, Android boots |
| MicroSD | Not tested |
| MTP, exFAT, `/data` decryption | Not included |

## Important display settings

The Tegra framebuffer has padding at the end of each row. These settings are
required to avoid a stretched or slanted interface:

```make
TARGET_RECOVERY_PIXEL_FORMAT := "RGBX_8888"
DEVICE_RESOLUTION := 540x960
RECOVERY_GRAPHICS_FORCE_USE_LINELENGTH := true
RECOVERY_GRAPHICS_FORCE_SINGLE_BUFFER := true
TW_THEME := portrait_hdpi
```

`portrait_hdpi` has a 9:16 reference resolution and therefore scales evenly to
the D625 panel. The recovery header displays `3.1.1-1 by chijure` through
`TW_DEVICE_VERSION` and `TW_BUILD_AUTHOR`.

The file `recovery/graphics.c` is retained as a historical Tegra 4i reference
from the NVIDIA S8515/Wiko Wax device tree. It is not compiled by this tree;
the validated build uses TWRP's standard fbdev backend with the two settings
above.

## Boot image layout

The values were read from the original LG recovery image. The partition size
comes from the kernel GPT; nvflash reports 16 MiB for SOS, but the last 4 MiB
belong to the following DTB partition.

| Field | Value |
|---|---:|
| Kernel address | `0x10008000` |
| Ramdisk address | `0x11000000` |
| Second address | `0x10f00000` |
| Tags address | `0x10000100` |
| Page size | `2048` |
| Command line | `androidboot.hardware=g2mv vmalloc=440M` |
| Recovery/boot partition size | `12582912` bytes |

## Kernel

`prebuilt/kernel` is the stock LG kernel and is not stored in Git. The boot
(LNX) and recovery (SOS) images of firmware D62510c carry the same kernel.
Extract it from a stock boot image, a stock recovery image or a TWRP
`boot.emmc.win` backup:

```bash
device/lge/g2mv/extract-kernel.py boot.emmc.win
```

The script refuses any kernel whose SHA-256 is not:

```text
7273a61c75b31d6c5e620bb2ea6dd4cea53a8326e71438b43600acf8b8b67b38
```

## Partitions

The recovery uses the Tegra by-name paths exposed by the stock kernel:

| Mount point | Type | Partition |
|---|---|---|
| `/recovery` | emmc | `SOS` |
| `/boot` | emmc | `LNX` |
| `/system` | ext4 | `APP` |
| `/cache` | ext4 | `CAC` |
| `/data` | ext4 | `UDA` |
| `/misc` | emmc | `MSC` |
| `/staging` | emmc | `USP` |
| `/encrypt` | emmc | `MDA` |
| `/external_sd` | auto | external microSD partition 1 |

The data crypto footer lives in `MDA`, as in the stock fstab. This build does
not include decryption support, so an encrypted `/data` cannot be backed up.

These LG/Icera partitions are offered as optional raw-image backups. Back them
up once before installing any ROM:

| Mount point | Partition | Size |
|---|---|---:|
| `/modem` | `MDM` (Icera modem, ext4) | 16 MiB |
| `/cust` | `CST` (carrier customization, ext4) | 50 MiB |
| `/mpt` | `MPT` | 16 MiB |
| `/pst` | `PST` | 8 MiB |
| `/sns` | `SNS` | 8 MiB |
| `/rct` | `RCT` | 2 MiB |
| `/drm` | `DRM` | 8 MiB |
| `/sep` | `SEP` | 2 MiB |

## Build

Place this repository at `device/lge/g2mv` in an Android 4.4 TWRP source tree:

```bash
device/lge/g2mv/extract-kernel.py /path/to/stock-boot.img
device/lge/g2mv/apply-recovery-patches.sh
source build/envsetup.sh
lunch omni_g2mv-eng
make -j$(nproc) recoveryimage
device/lge/g2mv/revert-recovery-patches.sh
```

The local patch fixes a TWRP 3.1.1 deadlock in the tar child processes. Those
children called GUI functions after `fork()`, which hung every `/system`
backup when it was split into multiple archives. The patch removes every GUI
call from the backup and restore children, including the error paths. The helper scripts apply it only for the build
and restore `bootable/recovery` afterward, which keeps the upstream source tree
clean. Always run the revert script after the build, including after a failed
build.

Output:

```text
out/target/product/g2mv/recovery.img
```

## Test without flashing

Boot the image temporarily from the unlocked bootloader:

```bash
fastboot boot out/target/product/g2mv/recovery.img
```

This command does not install the recovery. Verify the display, touch, ADB and
mounts before considering any permanent write. APX/nvflash is not required for
this test.

