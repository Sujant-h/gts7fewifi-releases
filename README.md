# LineageOS 24.0 for the Galaxy Tab S7 FE Wi-Fi (gts7fewifi)

Unofficial LineageOS 24.0 (Android 17) builds for the **Samsung Galaxy Tab S7 FE Wi-Fi, SM-T733** only (not for
the LTE/5G models). Monthly releases, built from public sources plus Samsung firmware blobs.

## Variants

| Variant | Google services | For whom |
|---|---|---|
| `microg` | microG (GmsCore, FakeStore, GsfProxy) + F-Droid preinstalled, signature spoofing for microG only | no Google apps, apps from F-Droid / Aurora Store |
| `vanilla` | none | flash your own GApps package (e.g. MindTheGapps 17), or use it without |

Both are built from the same sources and signed with the same private release keys. Switching between them, or
coming from any other build, needs Format data (see [INSTALL.md](INSTALL.md)).

## Downloads

Downloads are on the [Releases page](https://github.com/Sujant-h/gts7fewifi-releases/releases). Each release
contains, per variant (`microg`, `vanilla`): the installation ZIP, `recovery-<variant>.img`, `vbmeta-<variant>.img`,
`boot-<variant>.img`, `dtbo-<variant>.img`, `vendor_boot-<variant>.img`, plus one `SHA256SUMS.txt` for all files.

### Verify the download

```
sha256sum -c SHA256SUMS.txt                                     # Linux/macOS
Get-FileHash .\lineage-*.zip -Algorithm SHA256                  # Windows PowerShell, compare with SHA256SUMS.txt
```

All APKs, APEXes and the OTA package are signed with these release keys (SHA-256 fingerprints of the
certificates):

| Certificate | SHA-256 |
|---|---|
| releasekey | `97:22:64:C2:B3:93:9F:85:DF:D6:2C:B8:43:B6:59:4B:2D:4D:71:2C:A0:26:8F:7F:2B:96:CC:DC:0E:8F:4A:0A` |
| platform | `58:86:C5:03:0D:31:A8:31:D0:BE:74:4D:68:B0:AB:55:77:42:07:FB:88:6A:29:91:BC:61:00:17:51:7B:87:24` |

## Documentation

- [INSTALL.md](INSTALL.md) - first installation, switching from other builds, updates
- [CHANGELOG.md](CHANGELOG.md) - what differs from LineageOS, per release
- [KNOWN_ISSUES.md](KNOWN_ISSUES.md)

## Sources

Every release is tagged with its version (e.g. `24.0-20261113`) in the repositories below; the tag points to the
exact commit that was built (including the applied LineageOS Gerrit changes). The full pinned manifest of all
projects is in [`manifests/`](manifests/).

| Part | Repository |
|---|---|
| Device tree | https://github.com/Sujant-h/android_device_samsung_gts7fewifi |
| Common tree | https://github.com/Sujant-h/android_device_samsung_sm7325-common (+ open LineageOS Gerrit changes, topic `T733-bringup`) |
| Kernel (GPL source) | https://github.com/Sujant-h/android_kernel_samsung_sm7325 |
| Common vendor blobs | https://github.com/Sujant-h/proprietary_vendor_samsung_sm7325-common |
| microG | https://github.com/lineageos4microg/android_vendor_partner_gms (commit `8b49146`) |

Branch for development: `lineage-24.0-ss`. The device-specific Samsung blobs (`vendor/samsung/gts7fewifi`) are not
published separately; to build yourself, extract them from a tablet running T733XXS9DYF1 with
`extract-files.py` from the device tree.

## Development

Device changes, build scripts and tests were developed with an AI coding assistant (Claude Code by Anthropic).
Every change was reviewed, built and tested on an SM-T733 before release; commits made with AI help carry a
`Co-Authored-By: Claude` trailer.

## Credits

This build stands on the work of others:

- **Bush-cat**: the gts7fewifi bring-up (device tree, vendor blobs, kernel drivers from T733XXS9DYF1).
- **Simon1511**: LineageOS maintainer of the sm7325 platform (common device tree, kernel, vendor), including the
  kernel fix that makes PayPal start again.
- **Rocky7842** and **J0SH1x**: kernel changes for charging control and the flip cover.
- **The LineageOS team** (Bruno Martins, Michael Bestas, Nolen Johnson, Cosmin Tanislav, Tim Zimmermann and many
  others): LineageOS and the Samsung hardware support it builds on.
- **OpenELA**: Linux 5.4 stable updates.
- **microG** and **lineageos4microg**; **F-Droid**.

## Disclaimer

Unofficial build, not supported by LineageOS. You flash it at your own risk; your warranty is void anyway once
the bootloader is unlocked (Knox is tripped).
