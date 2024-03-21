#!/usr/bin/env python
# Copyright (c) 2016 CNRS
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


from hpp.corbaserver.affordance.client import Client as AffClient
from hpp.corbaserver.client import Client as BasicClient


class CorbaClient:
    """
    Container for corba clients to various interfaces.
    """

    def __init__(self, context=None, port=13331):
        if context is None:
            self.basic = BasicClient(port=port)
            self.affordance = AffClient(port=port)
        else:
            self.basic = BasicClient(context=context, port=port)
            self.affordance = AffClient(context=context, port=port)


class AffordanceTool:
    """
    \\brief Load and handle an AffordanceTool for analysis of the environment.

     AffordanceTool offers a set of helper functions that combines the affordance
    analysis on the C++ side with visualisation tools. The objective is to make the
    analysis tools more intuitive for the user.
    """

    def __init__(self, context=None, port=13331):
        self.client = CorbaClient(context, port=port)

    def removeObstacleFromJoint(self, objectName, jointName, collision, distance):
        """
        \\brief Remove an obstacle from outer objects of a joint body.

         This function also deletes all affordance objects created
         for the given obstacle, both from the problem solver and
         from the viewer.

         \\param objectName name of the object to remove,
         \\param jointName name of the joint owning the body,
         \\param collision whether collision with object should be computed,
         \\param distance whether distance to object should be computed.
        """
        self.client.basic.obstacle.removeObstacleFromJoint(
            objectName, jointName, collision, distance
        )
        return self.deleteAffordances(obstacleName)  # noqa TODO

    def resetAffordanceConfig(self):
        """
        \\brief Reset the current configuration of the given affordance
         type requirement to default values.
        """
        self.client.affordance.affordance.resetAffordanceConfig()

    def setAffordanceConfig(self, affType, config):
        """
        \\brief  changes the default configuration of the given affordance type
        requirement

         The configuration vector has size 3 and comprises the error margin,
         the angle margin for neighbouring triangles and the minimum area,
         in that order.

         \\param affType affordance type for which the change is made
         \\param conf configuration vector of size 3
        """
        return self.client.affordance.affordance.setAffordanceConfig(affType, config)

    def getAffordanceConfig(self, affType):
        """
        \\brief Returns the configuration of the given affordance type requirement

         \\param affType affordance type for which the configuration is requested
        """
        return self.client.affordance.affordance.getAffordanceConfig(affType)

    def setMargin(self, affType, margin):
        """
        \\brief Changes the error margin used to evaluate the affordance requirement
         of a given affordance type

         \\param affType affordance type for which the change is made
         \\param margin new value for the error margin
        """
        return self.client.affordance.affordance.setMargin(affType, margin)

    def setNeighbouringTriangleMargin(self, affType, nbTriMargin):
        """
        \\brief Changes the angle margin used to evaluate whether neighbouring
         triangles form part of the potential affordance as the current
         triangle.

         \\param affType affordance type for which the change is made
         \\param nbTriMargin new value for the neighbouring triangle margin
        """
        return self.client.affordance.affordance.setNeighbouringTriangleMargin(
            affType, nbTriMargin
        )

    def setMinimumArea(self, affType, minArea):
        """
        \\brief Changes the minimum area used to evaluate the affordance requirement
          of a given affordance type
         \\param affType affordance type for which the change is made
         \\param nimArea new value for the minimum accepted area
        """
        return self.client.affordance.affordance.setMinimumArea(affType, minArea)

    def analyseAll(self, reduceSizes=[]):
        """
        \\brief Analyse all loaded obstacles in the problem solver.

         All found affordance objects are added to their corresponding
         container in problem solver.
         \\param reduceSizes : dimension of the reduction applied to the plan (to shrink
         the borders of each affordances plans).
           The order of the value in the vector correspond to the order of the
           affordance type creation in affordance.impl.cc : Afford::createOperations ().
        """
        return self.client.affordance.affordance.analyseAll(reduceSizes)

    def analyseObject(self, objectName, reduceSizes):
        """
        \\biref Analyse one object by name

         Found affordance objects are added to a container in problem solver.

         \\param objectName name of the object to analyse.
         \\param reduceSizes : dimension of the reduction applied to the plan (to shrink
         the borders of each affordances plans).
           The order of the value in the vector correspond to the order of the
           affordance type creation in affordance.impl.cc : Afford::createOperations ().
        """
        return self.client.affordance.affordance.analyseObject(objectName, reduceSizes)

    def getAffordancePoints(self, affordanceType):
        """
        \\brief Get vertex points of all triangles of an affordance type.

          Returns the global position of of all vertices of the triangles
          of individual affordance obstacles of given type. Useful for
          visualisation purposes. The size of the return variable is the number
         of affordance obstacles of the requested type. The order of the
         returned objects is the same as that returned by the function
         getAffRefObstacles. Useful for visualisation.

         \\param affordanceType name of the affordance type for which
                the triangle points will be provided.
        """
        return self.client.affordance.affordance.getAffordancePoints(affordanceType)

    def getAffordanceTypes(self):
        """
        \\brief Get list of affordance types used in affordance analysis.

         Helper function that returns a list of strings. Useful as many
         functions require an affordance type as input parameter, and the
         spelling (capital letters etc.) matters.
        """
        return self.client.affordance.affordance.getAffordanceTypes()

    def getAffRefObstacles(self, affType):
        """
        \\brief Get list of CollisionObstacle names corresponding to affordance objects
         of a scpecific type.

         Helper function that returns a list of the reference collisionObstacles
         (as string type) for all affordance object of given affordance type. The
         return variable has the same size as the number of affordance obstacles
         of the requested type, and the order matches that of the affordance objects
         returned by function getAffordancePoints. Useful for visualisation.

         \\param affType The affordance type for which the reference obstacles will
                be provided.
        """
        return self.client.affordance.affordance.getAffRefObstacles(affType)

    def loadObstacleModel(
        self, filename, prefix, Viewer, guiOnly=False, reduceSizes=[]
    ):
        """
        \\brief Load obstacles, visualise them in viewer and analyse them for
        affordances.

         Loads obstacle model and saves it in problem solver. The obstacle is
         also shown in the viewer, and subsequently searched for affordance
         objects. To do the affordance analysis on the added object, it is
         searched for in the list of existing obstacles in problem solver.
         This search works without problems only if the prefix parameter
         does not contain the '/' character!

         \\param filename name of the urdf file, may contain "package://"
         \\param prefix prefix added to object names in case the same file
                is loaded several times. It should not cointain the '/' character
         \\param Viewer viewer object to load loaded obstacles to visualiser
         \\param guiOnly whether to control only gepetto-viewer-server
        """
        Viewer.loadObstacleModel(filename, prefix, guiOnly)
        import re

        objNames = self.client.basic.obstacle.getObstacleNames(True, False)
        for name in objNames:
            print("obs name ", name)
            splt = re.split("/", name)
            if splt[0] == prefix:
                self.analyseObject(name, reduceSizes)
        return

    def visualiseAllAffordances(self, affType, Viewer, colour):
        """
        \\brief Visualise all found affordance surfaces for an affordance type.

         For a given type of affordance, this function creates
         a group node of the same name, and adds nodes to this group.
         The nodes correspond to the triangles (and their global position)
         of all affordance objects of the given affordance type. The naming
         convention is as follows:
         "AffordanceType-ReferenceObstacleName.indexInAffObjectVector.triangleIndex"
         where indexInAffObjectVector is the index of one affordance object in the
         vector corresponding to the given affordance type (within a container in
         problem solver). triangleIndex is the index of one triangle within the
         current affordance object.
         Before creating the group node, any node with the same name is deleted.


         \\param affType the type of affordance to be visualised
         \\Viewer viewer object to load affordance objects to visualiser
         \\groupName name of group in the viewer that the objects will be added to
         \\colour vector of length 4 (normalized rgba)  defined in the interval [0, 1]
        """
        if len(colour) < 4:  # if the colour is only rgb we suppose alpha = 1
            colour = [*colour, 1]
        self.deleteNode(str(affType), True, Viewer)
        objs = self.getAffordancePoints(affType)
        refs = self.getAffRefObstacles(affType)
        Viewer.client.gui.createGroup(str(affType))
        for aff in objs:
            count = 0
            for tri in aff:
                Viewer.client.gui.addTriangleFace(
                    str(affType)
                    + "-"
                    + str(refs[objs.index(aff)])
                    + "."
                    + str(objs.index(aff))
                    + "."
                    + str(count),
                    tri[0],
                    tri[1],
                    tri[2],
                    [colour[0], colour[1], colour[2], colour[3]],
                )
                Viewer.client.gui.addToGroup(
                    str(affType)
                    + "-"
                    + str(refs[objs.index(aff)])
                    + "."
                    + str(objs.index(aff))
                    + "."
                    + str(count),
                    str(affType),
                )
                count += 1
        groupNodes = Viewer.client.gui.getGroupNodeList(Viewer.sceneName)
        if groupNodes is not None:
            Viewer.client.gui.addToGroup(str(affType), Viewer.sceneName)
            # By default, oldest node is displayed in front. Removing and re-adding
            # object from scene assure that the new triangles are displayed on top
            for groupNode in groupNodes:
                Viewer.client.gui.removeFromGroup(groupNode, Viewer.sceneName)
                Viewer.client.gui.addToGroup(groupNode, Viewer.sceneName)
        return

    def visualiseAffordances(self, affType, Viewer, colour, obstacleName=""):
        """
        \\brief Visualise affordance surfaces of given type for one obstacle.

         For a given affordance type and collisionObstacle, this function
         visualised the affordance surfaces and adds them as triangles into
         the viewer. If no obstacleName is provided, the visualiseAllAffordances
         function is executed instead.
         If a name is given, the affordance surfaces for the corresponding
         obstacle are first deleted, and if no node of the name affType is
         found, it is created. Then, the function adds nodes to this group.
         The nodes correspond to the triangles (and their global position)
         of all affordance objects of the given affordance type. The naming
         convention is as follows:
         "AffordanceType-ReferenceObstacleName.indexInAffObjectVector.triangleIndex"
         where indexInAffObjectVector is the index of one affordance object in the
         vector corresponding to the given affordance type (within a container in
         problem solver). triangleIndex is the index of one triangle within the
         current affordance object.

         \\param affType the type of affordance to be visualised
         \\param Viewer viewer object to load affordance objects to visualiser
         \\param colour vector of length 4 (normalized rgba),
                defined in the interval [0, 1]
         \\param obstacleName Name of collision obstacle for which affordances
                will be visualised
        """
        if len(colour) < 4:  # if the colour is only rgb we suppose alpha = 1
            colour = [*colour, 1]
        if obstacleName == "":
            return self.visualiseAllAffordances(affType, Viewer, colour)
        else:
            self.deleteAffordancesByTypeFromViewer(affType, Viewer, obstacleName)
            nodes = Viewer.client.gui.getNodeList()
            if affType not in nodes:
                Viewer.client.gui.createGroup(str(affType))
            objs = self.getAffordancePoints(affType)
            refs = self.getAffRefObstacles(affType)
            for aff in objs:
                if refs[objs.index(aff)] == obstacleName:
                    count = 0
                    for tri in aff:
                        name = (
                            str(affType)
                            + "-"
                            + str(refs[objs.index(aff)])
                            + "."
                            + str(objs.index(aff))
                            + "."
                            + str(count)
                        )
                        Viewer.client.gui.addTriangleFace(
                            name,
                            tri[0],
                            tri[1],
                            tri[2],
                            [colour[0], colour[1], colour[2], colour[3]],
                        )
                        Viewer.client.gui.addToGroup(name, str(affType))
                        count += 1
            groupNodes = Viewer.client.gui.getGroupNodeList(Viewer.sceneName)
            Viewer.client.gui.addToGroup(str(affType), Viewer.sceneName)
            # By default, oldest node is displayed in front. Removing and re-adding i
            # object from scene assure that the new triangles are displayed on top
            for groupNode in groupNodes:
                Viewer.client.gui.removeFromGroup(groupNode, Viewer.sceneName)
                Viewer.client.gui.addToGroup(groupNode, Viewer.sceneName)
        return

    def deleteAffordances(self, Viewer, obstacleName=""):
        """
        \\brief Delete affordances for given object.

         Deletes affordance objects both from problem solver and from viewer.
         If no objectName provided, all affordances will be deleted.

         \\param Viewer viewer object to erase affordance objects from visualiser
         \\param obstacleName name of obstacle the affordances of which will
                be deleted.
        """
        self.deleteAffordancesFromViewer(Viewer, obstacleName)
        return self.client.affordance.affordance.deleteAffordances(obstacleName)

    def deleteAffordancesFromViewer(self, Viewer, obstacleName=""):
        """
        \\brief Delete affordance surfaces from viewer.

         For a given collisionObstacle, delete all nodes in viewer that
         correspond to its affordance surfaces. The function goes through,
         for all affordance types, the list of nodes in the group, and deletes
         the nodes that have obstacleName as part of their name.

        \\param Viewer viewer object to erase affordance objects from visualiser
        \\param obstacleName Name of collision obstacle for which affordances
               will be deleted
        """
        affs = self.getAffordanceTypes()
        if obstacleName == "":
            for aff in affs:
                self.deleteNode(aff, True, Viewer)
        else:
            import re

            for aff in affs:
                refs = self.getAffRefObstacles(aff)
                count = 0
                while count < len(refs):
                    if refs[count] == obstacleName:
                        toDelete = aff + "-" + refs[count]
                        nodes = Viewer.client.gui.getGroupNodeList(aff)
                        for node in nodes:
                            splt = re.split(r"\.", node)
                            if splt[0] == toDelete:
                                self.deleteNode(node, True, Viewer)
                    count += 1
        return

    def deleteAffordancesByType(self, affordanceType, Viewer, obstacleName=""):
        """
        \\brief Delete affordances of given type for a collisionObstacle.

         If no objectName provided, all affordances of given type will be
         deleted. Deleted affordance objects from problem solver and viewer.

         \\param affordanceType type of affordance to be deleted
         \\param Viewer viewer object to erase affordance objects from visualiser
         \\param obstacleName name of obstacle the affordances of which will
                be deleted.
        """
        self.deleteAffordancesByTypeFromViewer(affordanceType, Viewer, obstacleName)
        return self.client.affordance.affordance.deleteAffordancesByType(
            affordanceType, obstacleName
        )

    def deleteAffordancesByTypeFromViewer(
        self, affordanceType, Viewer, obstacleName=""
    ):
        """
        \\brief Delete affordance objects of given type from viewer for a
        collisionObstacle

         For a given collisionObstacle, delete nodes in viewer that correspond
         to a specific affordance type. The function goes through, for all
         affordance types, the list of nodes in the group, and deletes the
         nodes that have obstacleName as part of their name. If no obstacleName
         is given, all affordance ojbects of type affordanceType are deleted
         from viewer.

         \\param affordanceType type of affordance to be deleted
           \\param Viewer viewer object to erase affordance objects from visualiser
         \\param obstacleName name of obstacle the affordances of which will
                be deleted.
        """
        if obstacleName == "":
            Viewer.client.gui.deleteNode(affordanceType, True)
        else:
            import re

            affs = self.getAffordanceTypes()
            for aff in affs:
                if aff == affordanceType:
                    refs = self.getAffRefObstacles(aff)
                    count = 0
                    while count < len(refs):
                        if refs[count] == obstacleName:
                            toDelete = aff + "-" + refs[count]
                            nodes = Viewer.client.gui.getNodeList()
                            for node in nodes:
                                splt = re.split(r"\.", node)
                                if splt[0] == toDelete:
                                    self.deleteNode(node, True, Viewer)
                        count += 1
        return

    def deleteNode(self, nodeName, all, Viewer):
        """
        \\brief Delete node from visualiser

        \\param nodeName name of node to be deleted
        \\param all boolean that determines ...?
        \\param Viewer viewer object used to execute deletion function
        """
        return Viewer.client.gui.deleteNode(nodeName, all)

    def getObstacleNames(self, collision, distance):
        """
        get list of obstacles in problem solver.

        \\param collision  whether to return obstacle for collision (boolean)
        \\param distance whether to return obstacles for distance
         computation (boolean).
        """

        return self.client.basic.obstacle.getObstacleNames(collision, distance)
