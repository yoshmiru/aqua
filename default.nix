{ nixpkgs ? import <nixpkgs> {}}:
let
  inherit (nixpkgs) pkgs;
in pkgs.stdenv.mkDerivation {
  name = "aqua-env";
  buildInputs = with pkgs; [
    python3Packages.virtualenv
    gcc pkgconfig freetype libpng
  ];

  shellHook = ''
  '';
}
