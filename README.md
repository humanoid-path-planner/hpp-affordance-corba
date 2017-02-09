#  Humanoid Path Planner - AFFORDANCE-CORBA module

Copyright 2016 LAAS-CNRS

Author: Anna Seppala

##Description
hpp-affordance-corba implements python bindings for hpp-affordance, and presents a few example files.
Please refer to this [link](https://github.com/anna-seppala/hpp-affordance) for information on hpp-affordance.

##Installation on ubuntu-14.04 64 bit with ros-indigo

To install hpp-affordance-corba:

  1. install HPP
	- see https://github.com/humanoid-path-planner/hpp-doc/tree/devel

  2. install HPP-AFFORDANCE
	- see https://github.com/humanoid-path-planner/hpp-affordance
	
  3. Install hpp-template-corba :
  			
	- see 	https://github.com/laas/hpp-template-corba
	
  4. Clone the HPP-AFFORDANCE-CORBA repository onto your local computer and update the submodule:

			git clone --recursive https://github.com/humanoid-path-planner/hpp-affordance-corba/
			cd $HPP_AFFORDANCE_CORBA_DIR/

  5. Use CMake to install the HPP-AFFORDANCE-CORBA library. For instance:

			mkdir build
			cd build
			cmake -DCMAKE_INSTALL_PREFIX=${DEVEL_DIR}/install ..
			make install

  6. Optionally, install the HPP-RBPRM and HPP-RBPRM-CORBA packages that implement an efficient acyclic contact planner,
		 and its python bindings, respectively.
	- see https://github.com/stonneau/hpp-rbprm, and
		https://github.com/stonneau/hpp-rbprm-corba

##Documentation

  Open $DEVEL_DIR/install/share/doc/hpp-affordance-corba/doxygen-html/index.html in a web browser and you
  will have access to the code documentation. If you are using ipython, the documentation of the methods implemented
  is also directly available in a python console.

##Example

To see how to use the CORBA server and the affordance functionality, please refer to the python scripts provided within the 'tests' directory of this package. These python scripts use the HyQ model found in the 'data' directory (retrieved from https://github.com/iit-DLSLab/hyq-description).

To run the test files, launch the hpp-affordance-server executable, then open a python terminal, and copy one of the test scripts (e.g. test-affordance-description.py) into the python terminal bit by bit. This allows you to see the procedure in the viewer as you go through the comments in the example script.
