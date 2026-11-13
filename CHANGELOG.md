# Changelog

Unofficial LineageOS 24.0 (Android 17) for the Samsung Galaxy Tab S7 FE Wi-Fi (SM-T733, `gts7fewifi`).

Release tags follow `24.0-YYYYMMDD` (build date, same as `ro.lineage.version`). One release per month after
syncing LineageOS; both variants of a release are built from the same sources and signed with the same keys.

## 24.0-20261113 (first public release)

Base: LineageOS 24.0 as of 2026-11-13, Android security patch level 2026-11-01, vendor patch level 2025-06-01
(firmware T733XXS9DYF1, the last Samsung firmware for this model).

### Builds and signing

- Two variants from identical sources:
  - **microg**: microG (GmsCore, FakeStore, GsfProxy) and F-Droid with privileged extension preinstalled
    (lineageos4microg `android_vendor_partner_gms`, microG v0.3.17.252432). Signature spoofing for microG only.
  - **vanilla**: no Google or microG components; flash a GApps package yourself.
- Signed with private release keys (APKs, APEX containers and payloads, OTA package):
  `ro.build.tags=release-keys`.
- `userdebug` build type with the LineageOS defaults: `ro.debuggable=0`, `ro.adb.secure=1` (USB debugging has to
  be authorized on the tablet). As on official LineageOS builds, `adb root` only works after enabling Developer
  options -> Rooted debugging on the tablet. No root for apps; use Magisk if you need that (see INSTALL.md).

### Differences to the LineageOS sources / the bring-up tree

Device tree (`android_device_samsung_gts7fewifi`, based on the bring-up tree by Bush-cat):

- Correct partition sizes from the PIT: recovery 101584896 and vendor_boot 69206016 bytes (the common tree used
  the Galaxy A52s values, which put the AVB footer at the wrong offset: "invalid vbmeta header").
- Memory tuning for 4 GB RAM, each measured on the device before it was built in:
  - Dalvik heap: `heapgrowthlimit` 192m and the rest of the AOSP 4 GB heap profile (heapstartsize 8m,
    heaptargetutilization 0.6, heapmaxfree 16m) instead of the 6 GB phone values.
  - lmkd: `ro.lmk.lowmem_min_oom_score=1001` (no LOW_MEM kills, kills rely on PSI/swap/thrashing) and
    `ro.lmk.swap_compression_ratio=2` (lmkd counts zram swap as compressed). Measured in an app load test
    together with zram 75 %: cold restarts of cached apps 4.5 -> 0 per run, lmkd kills -82 %.
  - Multi-gen LRU enabled (kernel config fragment).
  - Removed the swappiness 160 override.
- Touch boost on user interaction (power HAL `INTERACTION` hint): fewer janky frames when scrolling and in gestures
  (measured -37 % janky frames, CPU temperature +2 °C on average).
- Bluetooth: device class reported as tablet; MAP, PBAP and SAP servers disabled (no phone functions).
- Credential Manager: `config_defaultCredentialManagerHybridService` set, so security keys (e.g. YubiKey over USB)
  work for WebAuthn/passkeys in browsers when microG (or Google Play services) provides the hybrid service.

Common tree (`android_device_samsung_sm7325-common`):

- Open LineageOS Gerrit changes for this tablet applied (topic `T733-bringup` and the chain it depends on).
- zram increased to 75 % of RAM.

Kernel (`android_kernel_samsung_sm7325`, Linux 5.4):

- Updated to 5.4.305 with the OpenELA stable tags (5.4.303 to 5.4.305).
- Merge of `android_kernel_qcom_sm8350` lineage-20 (LineageOS Gerrit 510534, Qualcomm driver updates).
- Multi-gen LRU backport.
- Wi-Fi fix: firmware crash when the hotspot changes from 2.4 to 5 GHz with a client connected (partial revert in
  qcacld-3.0).
- Open Gerrit changes for this tablet: gts7fewifi drivers from T733XXS9DYF1, touch gesture fix, flip cover event
  code, charging control node.

Not changed on purpose:

- No Samsung camera driver security fixes from newer stock kernels (see KNOWN_ISSUES.md).
- No debloating; F-Droid stays in the microg variant (disable it in Settings if you do not need it).
