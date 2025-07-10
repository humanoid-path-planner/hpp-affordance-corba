# Copyright (c) 2016, 2020, CNRS Authors: Anna Seppala, Guilhem Saurel
#
# This file is part of hpp-affordance-corba. hpp-affordance-corba is free
# software: you can redistribute it and/or modify it under the terms of the GNU
# Lesser General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# hpp-affordance-corba is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Lesser Public License
# for more details.  You should have received a copy of the GNU Lesser General
# Public License along with hpp-affordance-corba.  If not, see
# <http://www.gnu.org/licenses/>.

cmake_minimum_required(VERSION 3.22)

set(PROJECT_NAME hpp-affordance-corba)
set(PROJECT_DESCRIPTION
    "Corba server for Humanoid Path Planner Affordance applications")

set(CUSTOM_HEADER_DIR hpp/corbaserver/affordance)
set(PROJECT_USE_CMAKE_EXPORT TRUE)
set(CXX_DISABLE_WERROR TRUE)

# Check if the submodule cmake have been initialized
set(JRL_CMAKE_MODULES "${CMAKE_CURRENT_LIST_DIR}/cmake")
if(EXISTS "${JRL_CMAKE_MODULES}/base.cmake")
  message(STATUS "JRL cmakemodules found in 'cmake/' git submodule")
else()
  find_package(jrl-cmakemodules QUIET CONFIG)
  if(jrl-cmakemodules_FOUND)
    get_property(
      JRL_CMAKE_MODULES
      TARGET jrl-cmakemodules::jrl-cmakemodules
      PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
    message(STATUS "JRL cmakemodules found on system at ${JRL_CMAKE_MODULES}")
  else()
    message(STATUS "JRL cmakemodules not found. Let's fetch it.")
    include(FetchContent)
    FetchContent_Declare(
      "jrl-cmakemodules"
      GIT_REPOSITORY "https://github.com/jrl-umi3218/jrl-cmakemodules.git")
    FetchContent_MakeAvailable("jrl-cmakemodules")
    FetchContent_GetProperties("jrl-cmakemodules" SOURCE_DIR JRL_CMAKE_MODULES)
  endif()
endif()

include("${JRL_CMAKE_MODULES}/hpp.cmake")
include("${JRL_CMAKE_MODULES}/idl.cmake")
include("${JRL_CMAKE_MODULES}/python.cmake")

compute_project_args(PROJECT_ARGS LANGUAGES CXX)
project(${PROJECT_NAME} ${PROJECT_ARGS})

list(APPEND PKG_CONFIG_ADDITIONAL_VARIABLES cmake_plugin)

# Dependencies
add_project_dependency("hpp-core" REQUIRED)
add_project_dependency("hpp-affordance" REQUIRED)
add_project_dependency("hpp-corbaserver" REQUIRED)
add_required_dependency("omniORB4 >= 4.1.4")
# search for python
if(NOT FINDPYTHON_ALREADY_CALLED)
  findpython()
endif()

# Make sure that python submodule is installed in the same prefix as module.
if(NOT ${HPP_CORBASERVER_PREFIX} STREQUAL ${CMAKE_INSTALL_PREFIX})
  message(
    WARNING
      "  THIS PACKAGE SHOULD BE INSTALLED IN THE SAME PREFIX AS HPP-CORBASERVER,\n"
      "  SINCE IT INSTALLS A PYTHON SUBMODULE OF HPP.CORBASERVER.")
  message("CMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}")
  message("HPP_CORBASERVER_PREFIX=${HPP_CORBASERVER_PREFIX}")
endif()

set(${PROJECT_NAME}_HEADERS include/${CUSTOM_HEADER_DIR}/fwd.hh
                            include/${CUSTOM_HEADER_DIR}/server.hh)

set(${PROJECT_NAME}_SOURCES src/${PROJECT_NAME}.cc)

# Standalone corba server
add_executable(hpp-affordance-server ${${PROJECT_NAME}_SOURCES}
                                     ${${PROJECT_NAME}_HEADERS})
target_include_directories(
  hpp-affordance-server PUBLIC $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
target_link_libraries(hpp-affordance-server hpp-corbaserver::hpp-corbaserver
                      hpp-affordance::hpp-affordance)
install(
  TARGETS hpp-affordance-server
  EXPORT ${TARGETS_EXPORT_NAME}
  DESTINATION bin)

add_subdirectory(src)

config_files(include/${CUSTOM_HEADER_DIR}/doc.hh)

install(FILES data/urdf/hyq/hyq_trunk_large.urdf data/urdf/darpa.urdf
              data/urdf/box.urdf DESTINATION share/${PROJECT_NAME}/urdf)

install(FILES data/srdf/hyq/hyq_trunk_large.srdf data/srdf/darpa.srdf
              data/srdf/box.srdf DESTINATION share/${PROJECT_NAME}/srdf)

install(FILES data/meshes/darpareduced.stl data/meshes/box.stl
        DESTINATION share/${PROJECT_NAME}/meshes)

install(FILES data/meshes/hyq/hyq_all.stl data/meshes/hyq/hyq_trunk_large.stl
        DESTINATION share/${PROJECT_NAME}/meshes/hyq)

pkg_config_append_libs(${PROJECT_NAME})
