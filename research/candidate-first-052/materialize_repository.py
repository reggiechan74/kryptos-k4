#!/usr/bin/env python3
"""Restore original compact-package bytes in a new directory, offline."""
import argparse
import gzip
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def safe_path(root, name):
    relative = Path(name)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("Unsafe manifest path: " + name)
    return root / relative

def verify(path, size, digest):
    if not path.is_file() or path.stat().st_size != size or sha(path) != digest:
        raise ValueError("Byte verification failed: " + str(path))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", help="New directory outside this source package")
    args = parser.parse_args()
    destination = Path(args.destination).expanduser().resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("Destination must be outside the source package")
    if destination.exists():
        raise ValueError("Destination already exists; use a new directory")
    if any(path.is_symlink() for path in ROOT.rglob("*")):
        raise ValueError("Unexpected symlink in source package")
    transport = json.loads((ROOT / "GITHUB_TRANSPORT.json").read_text())
    manifest_path = ROOT / "ARCHIVE_MANIFEST.json"
    if sha(manifest_path) != transport["original_archive_manifest_sha256"]:
        raise ValueError("Original archive manifest changed")
    for entry in transport["entries"]:
        verify(safe_path(ROOT, entry["stored_path"]), entry["stored_bytes"], entry["stored_sha256"])
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
    restored = []
    for entry in transport["entries"]:
        source = safe_path(ROOT, entry["stored_path"])
        target = safe_path(destination, entry["original_path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(source, "rb") as incoming, target.open("wb") as outgoing:
            shutil.copyfileobj(incoming, outgoing)
        verify(target, entry["original_bytes"], entry["original_sha256"])
        restored.append(entry["original_path"])
    payload = json.loads(manifest_path.read_text())["files"]
    for name, entry in payload.items():
        verify(safe_path(destination, name), entry["bytes"], entry["sha256"])
    print(json.dumps({
        "passed": True, "destination": str(destination),
        "original_payload_hashes_verified": len(payload),
        "losslessly_restored": restored,
        "source_payloads_modified": False,
        "network_used": False,
        "omitted_original_compact_payloads": "Still omitted; see original omission inventory"
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
