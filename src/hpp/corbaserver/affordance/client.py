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

from omniORB import CORBA
import CosNaming

from hpp.corbaserver.affordance import Afford

class CorbaError(Exception):
    """
    Raised when a CORBA error occurs.
    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Client:
  """
  Connect and create clients for hpp-affordance library.
  """
  def __init__(self, postContextId = ""):
    """
    Initialize CORBA and create default clients.
    """
    import sys
    self.orb = CORBA.ORB_init (sys.argv, CORBA.ORB_ID)
    obj = self.orb.resolve_initial_references("NameService")
    self.rootContext = obj._narrow(CosNaming.NamingContext)
    if self.rootContext is None:
        raise CorbaError ('failed to narrow the root context')

    name = [CosNaming.NameComponent ("hpp" + postContextId, "corbaserver"),
            CosNaming.NameComponent ("affordanceCorba", "affordance")]

    try:
        obj = self.rootContext.resolve (name)
    except CosNaming.NamingContext.NotFound, ex:
        raise CorbaError ('failed to find affordance service.')
    try:
        client = obj._narrow (Afford)
    except KeyError:
        raise CorbaError ('invalid service name affordanceCorba')

    if client is None:
      # This happens when stubs from client and server are not synchronized.
        raise CorbaError (
            'failed to narrow client for service affordanceCorba')
    self.affordance = client
