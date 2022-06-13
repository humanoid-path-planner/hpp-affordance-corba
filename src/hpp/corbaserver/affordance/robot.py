# Copyright (c) 2015 CNRS
# Author: Anna Seppala
#
# This file is part of hpp-affordance-corba.
# hpp-affordance-corba is free software: you can redistribute it
# and/or modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# hpp-affordance-corba is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Lesser Public License for more details.  You should have
# received a copy of the GNU Lesser General Public License along with
# hpp-affordance-corba.  If not, see
# <http://www.gnu.org/licenses/>.

from hpp.corbaserver.robot import Robot as Parent


class Robot(Parent):
    packageName = "hpp-affordance-corba"
    urdfName = "hyq_trunk_large"
    urdfSuffix = ""
    srdfSuffix = ""

    def __init__(self, robotName, load=True):
        Parent.__init__(self, robotName, "freeflyer", load)
        self.rightWrist = ""
        self.leftWrist = ""
