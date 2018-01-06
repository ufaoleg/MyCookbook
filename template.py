# coding=utf-8
# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "ООО АБ Проспект"

import sys

import Autodesk.DesignScript.Geometry
import clr
import Revit
import RevitServices
import System
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
from System import Array
from System.Collections.Generic import *

clr.AddReference('ProtoGeometry')

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")

clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Add a reference to RevitServices to gain access to the Revit Document.
# Then import a DocumentManager from RevitServices to get the document.
clr.AddReference("RevitServices")

# Get the document from DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
UIdoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
ActiveView = doc.ActiveView

# Add a reference to the RevitAPI and import the DB namespace.
clr.AddReference("RevitAPI")


clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)


def process_list(_func, _list):
    return map(lambda x: process_list(_func, x) if type(x) == list else _func(x), _list)


def process_list_arg(_func, _list, _arg):
    return map(lambda x: process_list_arg(_func, x, _arg) if type(x) == list else _func(x, _arg), _list)


def process_parallel_lists(_func, *lists):
    return map(lambda *xs: process_parallel_lists(_func, *xs) if all(type(x) is list for x in xs) else _func(*xs),
               *lists)


"""
This function check if incoming element is a list,
and if not, creates last one
"""
def to_list(element):
    if hasattr(element, '__iter__'):
        return element
    else:
        return [element]


# Start Transaction
TransactionManager.Instance.EnsureInTransaction(doc)
# Regenerate
TransactionManager.Instance.ForceCloseTransaction()

try:
    errorReport = None

except:
    # if error occurs anywhere in the process catch it
    import traceback

    errorReport = traceback.format_exc()

# End Transaction
TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable
if None == errorReport:
    OUT = 0
else:
    OUT = errorReport
