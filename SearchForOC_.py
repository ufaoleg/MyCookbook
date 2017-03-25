# Copyright(c) 2016, Konrad K Sobon
# @arch_laboratory, http://archi-lab.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

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

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import System
from System import Array
from System.Collections.Generic import *

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

#The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN

def ProcessList(_func, _list):
    return map( lambda x: ProcessList(_func, x) if type(x)==list else _func(x), _list )

def ProcessListArg(_func, _list, _arg):
    return map( lambda x: ProcessListArg(_func, x, _arg) if type(x)==list else _func(x, _arg), _list )

def ProcessParallelLists(_func, *lists):
    return map( lambda *xs: ProcessParallelLists(_func, *xs) if all(type(x) is list for x in xs) else _func(*xs), *lists )

def Unwrap(item):
    return UnwrapElement(item)

# Convert single element to list
def ToList(x):
    if hasattr(x,'__iter__'):
        return x
    else:
        return [x]
wallList = []

try:
    errorReport = None
    walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).ToElements()
    for wall in walls:
        wType = wall.LookupParameter("Имя типа").AsString()
        if wType:
            if "ОС-" in wType:
                wallList.append(wall)

except:
    # if error accurs anywhere in the process catch it
    import traceback
    errorReport = traceback.format_exc()

#Assign your output to the OUT variable
if errorReport == None:
    OUT = wallList
else:
    OUT = errorReport