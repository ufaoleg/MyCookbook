# python nodes in dynamo 1.0
# proposed by Julien Benoit @jbenoit44
# http://aecuandme.wordpress.com/
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import ToDSType(bool) extension method
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
from System.Collections.Generic import *

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
import itertools
import operator

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
activeV = doc.ActiveView

host = []
finst = []
finstID = []
for i in IN[0]:
    host.append(UnwrapElement(i))
for i in IN[1]:
    finst.append(UnwrapElement(i))
for i in IN[1]:
    finstID.append(UnwrapElement(i).Id)

superset = []
hloop = []

for h in host:
    collection = List[ElementId](finstID)
    collector = FilteredElementCollector(doc, collection)
    a = h.BoundingBox[activeV]
    c = Outline(a.Min, a.Max)
    d = BoundingBoxIntersectsFilter(c, float(IN[2]))
    e = collector.WherePasses(d).ToElements()
    setlist = []
    hostlist = []
    hostlist.append(h)
    setlist.append(e)
    all_lists = [hostlist, setlist]
    c = reduce(operator.add, all_lists)
    superset.append(c)

OUT = superset