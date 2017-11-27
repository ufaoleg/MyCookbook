
import clr

clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
activeV = doc.ActiveView

# Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *
from itertools import repeat
import System
from System import Array
from System.Collections.Generic import *

import sys

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

def Unwrap(e):
	return UnwrapElement(e)

outdata_rooms = []
outdata_areas = []

list_levels = [Unwrap(i).Level for i in IN[0]]

for lvl in xrange(len(list_levels)):
	sublist_rooms = []
	sublist_areas = []
	for room, areas in zip(IN[0],IN[1]):
		elev = Unwrap(room).Level.Elevation*304.8
		levelName = Unwrap(room).Level.Name
		if elev < 7400:
			sublist_rooms.append(room)
			sublist_areas.append(areas)
	outdata_rooms.append(sublist_rooms)
	outdata_areas.append(sublist_areas)

OUT = outdata_rooms, outdata_areas