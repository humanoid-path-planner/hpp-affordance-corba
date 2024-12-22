{
  description = "corbaserver to provide affordance utilities in python";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/refs/pull/362956/head";
    flake-parts = {
      url = "github:hercules-ci/flake-parts";
      inputs.nixpkgs-lib.follows = "nixpkgs";
    };
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      perSystem =
        { pkgs, self', ... }:
        {
          devShells.default = pkgs.mkShell { inputsFrom = [ self'.packages.default ]; };
          packages = {
            default = self'.packages.hpp-affordance-corba;
            hpp-affordance-corba = pkgs.python3Packages.hpp-affordance-corba.overrideAttrs (_: {
              src = pkgs.lib.fileset.toSource {
                root = ./.;
                fileset = pkgs.lib.fileset.unions [
                  ./CMakeLists.txt
                  ./data
                  ./doc
                  ./idl
                  ./include
                  ./package.xml
                  ./src
                  ./tests
                ];
              };
            });
          };
        };
    };
}
