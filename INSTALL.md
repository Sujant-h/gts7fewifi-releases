# Installation

Applies to the Galaxy Tab S7 FE **Wi-Fi** (SM-T733, `gts7fewifi`) only. There is no official LineageOS wiki
page for this tablet; the steps follow the official guide for the Galaxy A52s 5G (`a52sxq`, same SoC, same
method): https://wiki.lineageos.org/devices/a52sxq/install/

You need: a PC with [samloader-rs](https://github.com/topjohnwu/samloader-rs/releases/latest) and
[Android platform tools](https://developer.android.com/tools/releases/platform-tools) (adb), a USB cable, battery
above 50 %. **Back up your data.** Every first installation and every switch between this build and another one
(other signing keys, or between GApps and microG) needs **Format data**, which erases the internal storage.

Files of a release (check them first, see "Verify the download" in README.md):

| File | Used for |
|---|---|
| `lineage-24.0-<date>-UNOFFICIAL-gts7fewifi-<variant>.zip` | the system, installed with `adb sideload` |
| `recovery-<variant>.img` | Lineage Recovery of the same release, flashed with samloader-rs |
| `vbmeta-<variant>.img` | disables verified boot (first installation only) |
| `boot-<variant>.img`, `dtbo-<variant>.img`, `vendor_boot-<variant>.img` | not needed for installation (they are inside the ZIP); `boot-<variant>.img` is for Magisk |

## 0. Firmware

The ZIP needs Android 13 firmware or newer and refuses to install otherwise. The last Samsung firmware for the
SM-T733 is **T733XXS9DYF1**; update the stock system to it (Settings, Software update) before you start.

## 1. First installation (from Samsung stock)

1. Unlock the bootloader and flash `vbmeta-<variant>.img` exactly as in the a52sxq guide, section "Pre-Install
   Instructions" (OEM unlock, "Device unlock mode" in Download mode, then
   `samloader flash --partition VBMETA vbmeta-<variant>.img`, factory reset). This erases all data.
2. Flash the recovery from this release in Download mode (Volume Up + Volume Down, then connect USB):
   `samloader flash --partition RECOVERY recovery-<variant>.img --no-reboot`
3. Boot into the recovery **right away**: hold Volume Down + Power for 8-10 s until the screen turns black,
   release immediately, then hold Volume Up + Power with the USB cable connected. Otherwise the stock system
   replaces the recovery again.
4. In the recovery: **Factory reset -> Format data / factory reset**.
5. **Apply update -> Apply from ADB**, on the PC: `adb -d sideload lineage-24.0-<date>-UNOFFICIAL-gts7fewifi-<variant>.zip`
   (stopping at 47 % with "failed to read command" is normal).
6. Variant **vanilla** only, if you want Google apps: Apply update -> Apply from ADB again and sideload a GApps
   package for Android 17 / LineageOS 24.0, arm64 (e.g. MindTheGapps 17). Confirm "Signature verification
   failed" with Yes (expected for add-ons). Variant **microg**: do **not** flash GApps.
7. Reboot system now. The first boot can take up to 15 minutes.

## 2. Coming from another LineageOS build (e.g. the Bush-cat build or a self-built test-keys build)

Different signing keys: an update that keeps the data does not work, **Format data is required**.

1. Flash `recovery-<variant>.img` of this release with samloader-rs as in section 1, steps 2-3. **Do not skip this
   step**: neither the ZIP nor later updates replace the recovery, an old one (e.g. Lineage Recovery 23.2) stays
   until you flash the new one by hand. Check the header line in the recovery: it must read
   `Version 24.0 (<date>)`. If it still shows an older version, the flash did not happen; repeat it.
2. **If you used GApps before and install the microg variant**: GApps packages put a script into
   `/system/addon.d` (MindTheGapps: `30-gapps.sh`). The recovery runs these scripts during every ZIP installation
   and copies the old Google apps back into the new system, next to microG - even after Format data, because
   `addon.d` lives on the system partition. Remove it before the sideload. In the Lineage Recovery with
   "Enable ADB" (Advanced menu) on:
   ```
   adb root
   adb shell
   mkdir -p /tmp/ps && mount -o rw -t ext4 /dev/block/mapper/system /tmp/ps
   rm /tmp/ps/system/addon.d/30-gapps.sh
   umount /tmp/ps
   ```
   (Other GApps packages may use a different file name; list `/tmp/ps/system/addon.d` first. Only
   `50-lineage.sh` should remain.)
3. Factory reset -> Format data / factory reset, then continue with section 1, steps 5-7.

## 3. Updates between releases of this build

Same keys and same variant, data stays:

- **On the tablet**: Settings -> System -> Updater -> check for updates, download, install. The Updater only
  offers newer releases of the variant you run; the tablet reboots into recovery and installs the ZIP.
- **From a PC**: Recovery -> Apply update -> Apply from ADB -> sideload the new ZIP.

Updates do **not** update the recovery, and the Updater option "Update recovery" has no effect (see
KNOWN_ISSUES.md). This is normal for this tablet: the recovery you flashed once keeps installing later releases.
A new `recovery-<variant>.img` only needs to be flashed by hand (section 1, steps 2-3) when the release notes
ask for it or when you move to a new LineageOS version.

GApps flashed by you (vanilla) survive through `addon.d`. Changing the variant (microg <-> vanilla with GApps)
needs Format data and the `addon.d` step above.

## 4. After the first boot

- **microg**: open microG Settings -> Self-Check: all items green, in particular signature spoofing. Then, as
  needed: Google device registration and Cloud Messaging (both off by default, required for push
  notifications), Google SafetyNet (off by default, needed by apps using Play Integrity), add a Google account.
  Apps from the Play Store: install Aurora Store from F-Droid.
- **vanilla**: set up Google as usual if you flashed GApps.
- USB debugging stays off unless you enable it in Developer options; adb then needs the authorization dialog on
  the tablet. Turn it off again when you do not need it.

## Optional: root with Magisk

This tablet has no fastboot and no A/B slots; patch the `boot-<variant>.img` **of the release and variant you are running**:

1. Install the Magisk app (https://github.com/topjohnwu/Magisk/releases), copy `boot-<variant>.img` to the tablet, Install ->
   "Select and Patch a File". Copy the resulting `magisk_patched-*.img` back to the PC.
2. Download mode, then `samloader flash --partition BOOT magisk_patched-<...>.img`.
3. After every update (new ZIP, also through the Updater) boot is unpatched again: repeat with the new release's `boot-<variant>.img`.
4. To remove root: `samloader flash --partition BOOT boot-<variant>.img` with the original image, or sideload the release ZIP
   again (data stays).

Root makes apps with root detection (banking, PayPal) more likely to fail.

## Back to Samsung stock

Flash the full stock firmware (AP, BL, HOME_CSC) with samloader-rs in Download mode, see the a52sxq guide /
"firmware_update" for the command form. This erases all data.
