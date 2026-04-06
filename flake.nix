{
  description = "corbaserver to provide affordance utilities in python";

  inputs = {
    gepetto.url = "github:gepetto/nix";
    flake-parts.follows = "gepetto/flake-parts";
    systems.follows = "gepetto/systems";
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } (
      { lib, ... }:
      {
        systems = import inputs.systems;
        imports = [
          inputs.gepetto.flakeModule
          {
            flakoboros.overrideAttrs.hpp-affordance-corba = _: {
              src = lib.fileset.toSource {
                root = ./.;
                fileset = lib.fileset.unions [
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
            };
          }
        ];
      }
    );
}
