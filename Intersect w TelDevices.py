# coding=utf-8
# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "Rezvov"

# region import
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


def ProcessList(_func, _list):
    return map(lambda x: ProcessList(_func, x) if type(x) == list else _func(x), _list)
###
# Выборка элементов ил LINK файла
###


try:
    errorReport = None
    collectorRvt = FilteredElementCollector(doc)
    filter = ElementCategoryFilter(BuiltInCategory.OST_RvtLinks)
    linkinst = collectorRvt.WherePasses(filter).WhereElementIsNotElementType().ToElements()

    linkdoc = []
    telDevices = []
    for lnk in linkinst:
        linkdoc.append(lnk.GetLinkDocument())

    for lnk in linkdoc:
        sublist = []
        telephoneDev = FilteredElementCollector(lnk).OfCategory(BuiltInCategory.OST_TelephoneDevices).WhereElementIsNotElementType().ToElements()
        for td in telephoneDev:
            sublist.append(td.ToDSType(True))
        if sublist:
        	telDevices.append(sublist)

except:  # if error accurs anywhere in the process catch it
    import traceback

    errorReport = traceback.format_exc()  # End Transaction

# Assign your output to the OUT variable
if errorReport == None:
    OUT = telDevices
else:
    OUT = errorReport
