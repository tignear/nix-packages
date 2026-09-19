# nix-packages

Shared Nix package definitions for use by other flakes.

## Usage

Add this repository as a flake input:

```nix
inputs.tignear-packages.url = "github:tignear/nix-packages";
```

Include `tignear-packages` in the `outputs` arguments, then reference a package
using the consuming environment's `system`:

```nix
mbx = tignear-packages.packages.${system}.mbx;
```

For example, add it to a development shell:

```nix
pkgs.mkShell {
  packages = [ tignear-packages.packages.${system}.mbx ];
}
```

The consuming flake's `flake.lock` pins the revision. To update it:

```sh
nix flake update tignear-packages
```

## Packages

| Package | Source | Platforms |
| --- | --- | --- |
| `mbx` | [mr-boxington](https://github.com/jdx/mr-boxington) release binaries | `x86_64-linux`, `aarch64-linux` |

The mbx version and release hashes are defined in
[`pkgs/mbx/default.nix`](pkgs/mbx/default.nix).

## Updates

The `Update mbx` workflow checks upstream daily at 21:23 UTC and can also be
run manually. New stable releases produce a pull request updating the version
and both Linux archive hashes after validation. Updates are merged manually.
