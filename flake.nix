# https://gist.github.com/sagittaros/32dc6ffcbc423dc0fed7eef24698d5ca 
{
  description = "Flake to manage python workspace";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    mach-nix.url = "github:DavHau/mach-nix";
  };

  outputs = { self, nixpkgs, flake-utils, mach-nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        python = "python39"; # <--- change here
        pkgs = import nixpkgs {
          inherit system;
          config = { allowUnfree = true; };
        };

        mach-nix-wrapper = import mach-nix { inherit pkgs python; };
        requirements = builtins.readFile ./requirements.txt;
        pythonBuild = mach-nix-wrapper.mkPython { inherit requirements; };
      in
      {
        packages.venv = pythonBuild;
        defaultPackage = self.packages.x86_64-linux.venv;
        devShell = pkgs.mkShell {
          buildInputs = [
            pythonBuild
          ];
        };
      });
}
