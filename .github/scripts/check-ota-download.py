#!/usr/bin/env python3
"""Verify that the public GitHub OTA exactly matches the staged update feed."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import subprocess

RELEASE_URL = "https://github.com/Sujant-h/gts7fewifi-releases/releases/download/"
OTA_NAME = re.compile(
    r"lineage-(?P<tag>\d+\.\d+-\d{8})-UNOFFICIAL-gts7fewifi-(?P<variant>microg|vanilla)\.zip"
)


def parse_feed(path, contents):
    records = json.loads(contents)
    (record,) = records
    (asset,) = record["files"]
    name = asset["filename"]
    match = OTA_NAME.fullmatch(name)
    if not match:
        raise ValueError(f"Unerwarteter oeffentlicher OTA-Dateiname: {name}")
    tag, variant = match.group("tag", "variant")
    if path.name != f"gts7fewifi-{variant}.json":
        raise ValueError(f"Updater-JSON und OTA-Variante passen nicht: {path}")
    if asset["url"] != f"{RELEASE_URL}{tag}/{name}":
        raise ValueError(f"Unerwartete Download-URL in {path}")
    if not re.fullmatch(r"[0-9a-f]{64}", asset["sha256"]):
        raise ValueError(f"Ungueltiger SHA-256-Wert in {path}")
    if type(asset["size"]) is not int or asset["size"] <= 0:
        raise ValueError(f"Ungueltige OTA-Groesse in {path}")
    if type(record["datetime"]) is not int or record["datetime"] <= 0:
        raise ValueError(f"Ungueltiger Build-Zeitstempel in {path}")
    if record["type"] != "unofficial" or record["version"] != tag.split("-")[0]:
        raise ValueError(f"Build-Typ oder Version passt nicht: {path}")
    if type(asset["os_sdk_level"]) is not int or asset["os_sdk_level"] <= 0:
        raise ValueError(f"Ungueltiger SDK-Level in {path}")
    date.fromisoformat(asset["os_patch_level"])
    return tag, record["datetime"], asset


def read_feed(path):
    return parse_feed(path, path.read_text())


def verify_download(asset):
    digest = hashlib.sha256()
    size = 0
    command = [
        "curl", "--disable", "--fail", "--silent", "--show-error", "--location",
        "--proto", "=https", "--proto-redir", "=https", "--connect-timeout", "20",
        "--max-time", "1800", "--max-filesize", str(asset["size"]), asset["url"],
    ]
    with subprocess.Popen(command, stdout=subprocess.PIPE) as curl:
        for block in iter(lambda: curl.stdout.read(1024 * 1024), b""):
            size += len(block)
            if size > asset["size"]:
                curl.kill()
                raise ValueError(f"Download zu gross: {asset['url']}")
            digest.update(block)
        if curl.wait():
            raise ValueError(f"Download fehlgeschlagen: {asset['url']}")
    if size != asset["size"] or digest.hexdigest() != asset["sha256"]:
        raise ValueError(f"Download stimmt nicht mit Updater-JSON ueberein: {asset['url']}")
    print(f"OK {asset['filename']}: {size} Byte, SHA-256 {digest.hexdigest()}")


def verify_feed_pr(base):
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        raise ValueError("Ungueltiger Basis-Commit")
    for variant in ("microg", "vanilla"):
        path = Path(f"gts7fewifi-{variant}.json")
        old = subprocess.check_output(["git", "show", f"{base}:{path}"], text=True)
        current = path.read_text()
        if json.loads(old) == json.loads(current):
            continue
        _, old_timestamp, _ = parse_feed(path, old)
        _, timestamp, asset = parse_feed(path, current)
        if timestamp <= old_timestamp:
            raise ValueError(f"Build-Zeitstempel muss steigen: {path}")
        if variant == "microg":
            report = json.loads(Path("ota-upgrade-microg.json").read_text())
            expected = {
                "result": "PASS", "device": "gts7fewifi", "variant": "microg",
                "from_datetime": old_timestamp, "to_datetime": timestamp,
                "filename": asset["filename"], "sha256": asset["sha256"],
            }
            if any(report.get(key) != value for key, value in expected.items()):
                raise ValueError("microG-Upgradebericht passt nicht zu Ausgangsbuild und OTA")
        verify_download(asset)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", action="store_true", help="Nur den Release-Tag ausgeben")
    parser.add_argument("--feed-pr-base", help="Feed-Aenderungen gegen diesen Git-Commit pruefen")
    parser.add_argument("feeds", type=Path, nargs="*")
    args = parser.parse_args()
    try:
        if args.feed_pr_base:
            if args.feeds or args.tag:
                parser.error("--feed-pr-base ist ein separater Modus")
            verify_feed_pr(args.feed_pr_base)
            return
        if not args.feeds:
            parser.error("Mindestens ein Updater-JSON angeben")
        feeds = [read_feed(path) for path in args.feeds]
        tags = {tag for tag, _, _ in feeds}
        if len(tags) != 1:
            raise ValueError("Updater-Dateien gehoeren zu verschiedenen Release-Tags")
        if args.tag:
            print(tags.pop())
        else:
            for _, _, asset in feeds:
                verify_download(asset)
    except (ValueError, TypeError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"FEHLER: {exc}\n")


if __name__ == "__main__":
    main()
