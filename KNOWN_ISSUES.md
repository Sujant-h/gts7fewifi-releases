# Known issues

Status as of release 24.0-20261113. Reports with logs (`adb logcat -d`, time of the problem) are welcome as issues.

## Release 24.0-20261113: recovery images cannot install the release ZIP

`recovery-microg.img` and `recovery-vanilla.img` of 24.0-20261113 were built with the test keys instead of the
release keys. Sideloading the release ZIP with them fails (`signature verification failed`, error 21). Do not
install 24.0-20261113; use the next release, which builds the recovery from the signed sources and checks it.

## Apps

- **PayPal closes right after start.** Its tamper check (`AppVerifier`) fails on this build; seen with test-keys,
  `ro.debuggable=1` and unlocked bootloader. Not yet tested with this release (release-keys, `ro.debuggable=0`);
  turning off USB debugging and Developer options may help. The unlocked bootloader stays detectable.
- **Banking and other apps with Play Integrity** may refuse to work: the bootloader is unlocked, so the device
  never passes "device integrity". With the microg variant, enable Google SafetyNet in microG Settings first.
- **Aurora Store 4.8.4 crashes about 2 s after start** (home feed contains an app twice). Upstream issue:
  https://gitlab.com/AuroraOSS/AuroraStore/-/work_items/1611. Workaround: tap "Search" right after start.
- **microG**: push notifications need Google device registration and Cloud Messaging (both off by default).
  Some Google features (e.g. ML Kit modules that are downloaded by Play services) may be missing.

## System

- **Colors look washed out after turning the screen on**, for about 20 s up to minutes; turning the screen off
  and on again fixes it. Seen once, cause under investigation (display configuration comes from an AMOLED phone,
  the tablet has an LCD).
- **SystemUI restarts** occasionally in desktop mode or when opening Recents (WM Shell exceptions in framework
  code, not device specific). Observed twice on one day; under observation.
- **`factory.ssc` tombstones** (`SIGABRT`) appear in the logs from time to time. It is a closed-source Samsung
  sensor calibration service; sensors keep working. Harmless.
- dmesg: `sysfs: cannot create duplicate filename '//wifi'` at boot. Harmless.

## Security notes

- Unlocked bootloader and disabled verified boot (`vbmeta` flags 3), as with every build for this tablet. Anyone
  with physical access can flash other software. Use a screen lock; data is encrypted (FBE).
- Vendor security patch level stays at **2025-06-01**: T733XXS9DYF1 is the last Samsung firmware, Samsung
  delivers no newer blobs. Android framework patches follow LineageOS monthly.
- Samsung camera driver security fixes from newer stock kernels are **not** ported to this kernel yet. The
  affected driver is only reachable through the camera HAL (no direct app access).
- `adb root` is available after enabling Developer options -> Rooted debugging (LineageOS default). Leave it off.
