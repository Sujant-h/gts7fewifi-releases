# Changelog

Unofficial LineageOS 24.0 (Android 17) for the Samsung Galaxy Tab S7 FE Wi-Fi (SM-T733, `gts7fewifi`).

Release tags follow `24.0-YYYYMMDD` (build date, same as `ro.lineage.version`). One release per month after
syncing LineageOS; both variants of a release are built from the same sources and signed with the same keys.

## 24.0-20261125 (first public release)

Base: LineageOS 24.0 as of 2026-11-13, Android security patch level 2026-11-01, vendor patch level 2025-06-01
(firmware T733XXS9DYF1, the last Samsung firmware for this model).

### Builds and signing

- Two variants from identical sources:
  - **microg**: microG and F-Droid preinstalled, signature spoofing for microG only.
  - **vanilla**: no Google or microG components; flash GApps yourself.
- Signed with private release keys.
- `ro.debuggable=0`, USB debugging needs authorization; `adb root` only via Developer options -> Rooted debugging.

### Changes

Device tree (`android_device_samsung_gts7fewifi`, based on the bring-up tree by Bush-cat):

- Fixed partition sizes (recovery, vendor_boot).
- Memory tuning for 4 GB RAM (Dalvik heap, lmkd, multi-gen LRU): fewer app reloads.
- Smoother scrolling (touch boost).
- Bluetooth: reported as tablet, phone profiles disabled.
- Security keys (e.g. YubiKey) work for passkeys in browsers.
- Privacy: hardware serial numbers hidden from apps.
- Wi-Fi: randomized MAC address on open networks.
- OTA updates through the LineageOS Updater.

Common tree (`android_device_samsung_sm7325-common`):

- Pending LineageOS changes for this tablet applied.
- zram increased to 75 % of RAM.

Kernel (`android_kernel_samsung_sm7325`, Linux 5.4):

- Updated to Linux 5.4.305.
- Updated Qualcomm drivers.
- Fixed Wi-Fi crash when switching the hotspot band.
- Fixed apps with tamper checks crashing at start (e.g. PayPal).
- Touchscreen: improved palm rejection.

Vendor files (private repository, built into the images):

- Dolby Atmos: steadier loudness for speech in the Smart and Voice profiles.
