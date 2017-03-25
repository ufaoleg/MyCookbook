import clr
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

elements = FilteredElementCollector(doc).OfClass(ViewSchedule)

name, guid, owner, creator, changeby = [], [], [], [], []

for x in elements:
    ws = WorksharingUtils.GetWorksharingTooltipInfo(doc, x.Id)
    name.append(x.Name.ToString())
    guid.append(x.UniqueId)
    owner.append(ws.Owner)
    creator.append(ws.Creator)
    changeby.append(ws.LastChangedBy)

flist = map(list, zip(*(name, guid, owner, creator, changeby)))

l1, l2 = [], []

for x in flist:
    if '<Revision Schedule> 2889' in x:
        l1.append(x)
    else:
        l2.append(x)

OUT = l1, l2