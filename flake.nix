{
  description = "corbaserver to provide affordance utilities in python";

  inputs.gepetto.url = "github:gepetto/nix";

  outputs =
    inputs:
    inputs.gepetto.lib.mkFlakoboros inputs (
      { lib, ... }:
      {
        overrideAttrs.hpp-affordance-corba = {
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
    );
}
