# TWRP port for LG D625 (`g2mv`)

TWRP 3.1.1 device tree for the LG G2 Mini LTE (D625, NVIDIA Tegra 4i), built
on the Android 4.4 branch of OmniROM/TWRP. It uses the stock LG kernel from
firmware D62510c.

See [device/lge/g2mv/README.md](device/lge/g2mv/README.md) for the tested
features, partition layout, kernel extraction and build steps.

Expected source layout:

```text
<android>/device/lge/g2mv -> this directory
```

Build with the historical Android 4.4 TWRP/OmniROM tree:

```sh
device/lge/g2mv/extract-kernel.py /path/to/stock-boot.img
device/lge/g2mv/apply-recovery-patches.sh
. build/envsetup.sh
lunch omni_g2mv-eng
mka recoveryimage
device/lge/g2mv/revert-recovery-patches.sh
```

Test with `fastboot boot` before installing the image to SOS. The bootloader
must first be patched as described in the main README of this repository.
