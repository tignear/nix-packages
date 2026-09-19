#!/usr/bin/env python3
"""Update mbx from the latest stable upstream release."""

import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request


def main():
    release = json.loads(subprocess.check_output(
        ["gh", "api", "repos/jdx/mr-boxington/releases/latest"], text=True
    ))
    tag = release["tag_name"]
    if release["draft"] or release["prerelease"] or not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise ValueError(f"Unexpected stable release: {tag}")
    version = tag[1:]
    path = Path(__file__).resolve().parents[1] / "pkgs/mbx/default.nix"
    original = path.read_text()
    current = re.search(r'version = "(\d+\.\d+\.\d+)";', original).group(1)
    changed = tuple(map(int, version.split('.'))) > tuple(map(int, current.split('.')))
    if changed:
        updated = original.replace(f'version = "{current}";', f'version = "{version}";')
        assets = {asset["name"] for asset in release["assets"]}
        for arch in ("x86_64", "aarch64"):
            name = f"mbx-{arch}-unknown-linux-musl.tar.gz"
            if name not in assets:
                raise ValueError(f"Missing release asset: {name}")
            url = f"https://github.com/jdx/mr-boxington/releases/download/{tag}/{name}"
            digest = hashlib.sha256()
            with urllib.request.urlopen(url, timeout=120) as response:
                while chunk := response.read(1024 * 1024):
                    digest.update(chunk)
            sri = "sha256-" + base64.b64encode(digest.digest()).decode()
            pattern = rf'({arch}-linux = \{{\s*arch = "{arch}";\s*hash = ")[^"]+(";)'
            updated, count = re.subn(pattern, lambda match: match[1] + sri + match[2], updated)
            if count != 1:
                raise ValueError(f"Expected exactly one hash for {arch}")
        path.write_text(updated)
    print(f"mbx: {current} -> {version}" if changed else f"mbx {current} is up to date")
    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a") as stream:
            stream.write(f"changed={str(changed).lower()}\nversion={version}\n")


if __name__ == "__main__":
    main()
