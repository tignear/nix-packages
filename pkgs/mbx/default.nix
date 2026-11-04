{ pkgs }:
let
  releases = {
    x86_64-linux = {
      arch = "x86_64";
      hash = "sha256-YL4/+7TXFBiCftKGhsd2uGvbuATt1Dc5sdv83xYvvLU=";
    };
    aarch64-linux = {
      arch = "aarch64";
      hash = "sha256-vXkErt/3ikiwM5q4784MO4ZQXAt3/mOWRQTa4vhDudY=";
    };
  };

in
pkgs.stdenvNoCC.mkDerivation (finalAttrs: {
  pname = "mbx";
  version = "1.29.2";

  src = pkgs.fetchurl {
    url = "https://github.com/jdx/mr-boxington/releases/download/v${finalAttrs.version}/mbx-${
      releases.${pkgs.stdenv.hostPlatform.system}.arch
    }-unknown-linux-musl.tar.gz";
    hash = releases.${pkgs.stdenv.hostPlatform.system}.hash;
  };

  sourceRoot = ".";
  dontConfigure = true;
  dontBuild = true;

  installPhase = ''
    runHook preInstall
    install -Dm755 mbx $out/bin/mbx
    runHook postInstall
  '';

  meta = {
    description = "A shared cache for Cargo builds";
    homepage = "https://mr-boxington.jdx.dev";
    license = pkgs.lib.licenses.mit;
    mainProgram = "mbx";
    platforms = [
      "x86_64-linux"
      "aarch64-linux"
    ];
    sourceProvenance = [ pkgs.lib.sourceTypes.binaryNativeCode ];
  };
})
