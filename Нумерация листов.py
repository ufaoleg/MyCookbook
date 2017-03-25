import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
from System.Collections.Generic import *

uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
from operator import itemgetter

ids = uidoc.Selection.GetElementIds()
idd = [str(i) for i in ids]
if isinstance(idd, list) == True:
    views = [doc.GetElement(ElementId(int(i))) for i in idd]
else:
    views = doc.GetElement(ElementId(int(idd)))
# Входные данные
prefix = IN[0]
start = IN[1]
suffix = IN[2]
kol = IN[4]
# Сортировка листов
list1 = []
for view in views:
    num1 = view.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString()
    num = float(num1[kol:])
    list1.append([num, view])
views = sorted(list1, key=itemgetter(0))

# Замена номеров листов
TransactionManager.Instance.EnsureInTransaction(doc)
list2 = []
for view in views:
    try:
        new = prefix + str(start) + suffix
        view[1].get_Parameter(BuiltInParameter.SHEET_NUMBER).Set(new)
        list2.append(view[1])
    except:
        a = 0
    start = start + 1
TransactionManager.Instance.TransactionTaskDone()
# Assign your output to the OUT variable
OUT = list1
