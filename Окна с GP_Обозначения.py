# coding=utf-8
# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "ООО АБ Проспект"

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

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)


def ProcessList(_func, _list):
    return map(lambda x: ProcessList(_func, x) if type(x) == list else _func(x), _list)


koef = 304.8

if isinstance(IN[0], list):
    elements = []
    for i in IN[0]:
        elements.append(UnwrapElement(i))
else:
    elements = [UnwrapElement(IN[0])]

output = []
output_elements = []

try:
    errorReport = None
    for element in elements:
        el_width = element.Symbol.LookupParameter('Ширина').AsDouble() * koef
        el_height = element.Symbol.LookupParameter('Высота').AsDouble() * koef
        el_mark = element.Symbol.LookupParameter('Маркировка типоразмера').AsString()
        el_type_name = element.Name
        output.append("ОП ОСП {}-{} ПО-СБ ГОСТ 23166-99".format(str(round(el_width / 100))[:1] if el_width < 1000 else str(round(el_width / 100))[:2], str(el_height / 100)[:2] ))
        output_elements.append(element)

except:  # if error accurs anywhere in the process catch it
    import traceback

    errorReport = traceback.format_exc()  # End Transaction
    TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable
if errorReport == None:
    OUT = [output_elements, output]
else:
    OUT = errorReport
