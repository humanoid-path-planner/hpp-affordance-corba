# Copyright (c) 2016, 2020, CNRS Author: Anna Seppala, Guilhem Saurel
#
# This file is part of hpp-corbaserver. hpp-corbaserver is free software: you
# can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# hpp-corbaserver is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Lesser Public License for more
# details.  You should have received a copy of the GNU Lesser General Public
# License along with hpp-corbaserver.  If not, see
# <http://www.gnu.org/licenses/>.

set(IDL_SOURCES affordance)

include(${HPP_CORBASERVER_CMAKE_PLUGIN})
omniidl_include_directories(${HPP_CORBASERVER_DATAROOTDIR}/idl
                            ${CMAKE_SOURCE_DIR}/idl)
include_directories(${CMAKE_CURRENT_BINARY_DIR})
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/hpp/corbaserver/affordance)
foreach(IDL ${IDL_SOURCES})
  generate_idl_cpp(${IDL} ${CMAKE_SOURCE_DIR}/idl/hpp/corbaserver/affordance
                   HEADER_SUFFIX -idl.hh)
  generate_idl_python(
    ${IDL}
    ${CMAKE_SOURCE_DIR}/idl/hpp/corbaserver/affordance
    ENABLE_DOCSTRING
    STUBS
    hpp_stubs.affordance
    ARGUMENTS
    -Wbmodules=hpp_idl
    -Wbextern=common:hpp_stubs)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${IDL}-idl.hh
          DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/hpp/corbaserver/affordance/)
endforeach()

install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/hpp_idl/hpp/corbaserver/affordance
        DESTINATION ${PYTHON_SITELIB}/hpp_idl/hpp/corbaserver)
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/hpp_stubs/affordance
        DESTINATION ${PYTHON_SITELIB}/hpp_stubs)

add_custom_target(generate_idl_cpp DEPENDS ${ALL_IDL_CPP_STUBS})
add_custom_target(generate_idl_python DEPENDS ${ALL_IDL_PYTHON_STUBS})

hpp_add_server_plugin(
  affordance-corba
  SOURCES
  ${ALL_IDL_CPP_STUBS}
  affordance.impl.hh
  affordance.impl.cc
  server.cc
  LINK_DEPENDENCIES
  hpp-corbaserver::hpp-corbaserver
  hpp-affordance::hpp-affordance
  PKG_CONFIG_DEPENDENCIES
  omniORB4)

add_dependencies(affordance-corba generate_idl_cpp)
add_dependencies(affordance-corba generate_idl_python)

python_install_on_site(hpp/corbaserver/affordance __init__.py)
python_install_on_site(hpp/corbaserver/affordance affordance.py)
python_install_on_site(hpp/corbaserver/affordance client.py)
python_install_on_site(hpp/corbaserver/affordance corba.py)
python_install_on_site(hpp/corbaserver/affordance robot.py)

install(FILES ${CMAKE_SOURCE_DIR}/idl/hpp/corbaserver/affordance/affordance.idl
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/idl/hpp/corbaserver/affordance)

# Generate and install python code for each dependency idl file
foreach(IDL ${HPP_CORBASERVER_IDL_SOURCES})
  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/hpp/corbaserver/affordance/${IDL}_idl.py
    COMMAND
      ${OMNIIDL} ARGS -bpython -Wbpackage=""
      -I${HPP_CORBASERVER_DATAROOTDIR}/idl
      ${HPP_CORBASERVER_DATAROOTDIR}/idl/hpp/corbaserver/${IDL}.idl
    MAIN_DEPENDENCY
      ${HPP_CORBASERVER_DATAROOTDIR}/idl/hpp/corbaserver/${IDL}.idl)
  set_source_files_properties(${CMAKE_CURRENT_BINARY_DIR}/${IDL}_idl.py
                              GENERATED=ON)
  set_source_files_properties(
    ${CMAKE_CURRENT_BINARY_DIR}/hpp/corbaserver/affordance/__init__.py
    GENERATED=ON)
  install(
    FILES ${CMAKE_CURRENT_BINARY_DIR}/${IDL}_idl.py
          ${CMAKE_CURRENT_BINARY_DIR}/hpp/corbaserver/affordance/__init__.py
    DESTINATION ${PYTHON_SITELIB}/hpp/corbaserver/affordance)
endforeach()
