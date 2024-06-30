{
  lib,
  cmake,
  hpp-affordance,
  hpp-corbaserver,
  pkg-config,
  python3Packages,
}:

python3Packages.buildPythonPackage {
  pname = "hpp-affordance-corba";
  version = "5.0.0";
  pyproject = false;

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

  strictDeps = true;

  nativeBuildInputs = [
    cmake
    pkg-config
  ];
  buildInputs = [
    python3Packages.boost
  ];
  propagatedBuildInputs = [
    hpp-affordance
    hpp-corbaserver
    python3Packages.omniorbpy
  ];

  enableParallelBuilding = false;

  doCheck = true;

  meta = {
    description = "corbaserver to provide affordance utilities in python";
    homepage = "https://github.com/humanoid-path-planner/hpp-affordance-corba";
    license = lib.licenses.bsd2;
    maintainers = [ lib.maintainers.nim65s ];
  };
}
