{
  description = "Shared Nix package definitions for use by other flakes";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in
    {
      packages = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          mbx = pkgs.callPackage ./pkgs/mbx { };
        in
        {
          inherit mbx;
          default = mbx;
        });
    };
}
