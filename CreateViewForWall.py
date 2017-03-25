# coding=utf-8
"""
Make Plans
Create Plans from Curtain Walls
"""
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

# The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN


def U(item):
    return UnwrapElement(item)


walls = []

if isinstance(IN[0], list):
    for wall in IN[0]:
        walls.append(U(wall))
else:
    walltypes = U(IN[0])

viewType = U(IN[1])
level = U(IN[2])
RunIt = IN[3]

bboxOffset = 1


def OffsetBBox(bbox, offset):
    bboxMinX = bbox.Min.X - offset
    bboxMinY = bbox.Min.Y - offset
    bboxMinZ = bbox.Min.Z - offset
    bboxMaxX = bbox.Max.X + offset
    bboxMaxY = bbox.Max.Y + offset
    bboxMaxZ = bbox.Max.Z + offset
    newBbox = BoundingBoxXYZ()
    newBbox.Min = XYZ(bboxMinX, bboxMinY, bboxMinZ)
    newBbox.Max = XYZ(bboxMaxX, bboxMaxY, bboxMaxZ)
    return newBbox


namePrefix = "Витраж_"
if RunIt:
    existingPlans = FilteredElementCollector(doc).OfClass(View).ToElements()
    existingPlanNames, existingPlanElements = [], []
    for existingPlan in existingPlans:
        if not existingPlan.IsTemplate:
            if existingPlan.ViewType == ViewType.FloorPlan:
                existingPlanNames.append(existingPlan.Name)
                existingPlanElements.append(existingPlan)

    # Start Transaction
    doc = DocumentManager.Instance.CurrentDBDocument
    TransactionManager.Instance.EnsureInTransaction(doc)

    floorPlans = []
    for i in walls:
        levelId = i.LevelId
        bbox = i.BoundingBox[doc.ActiveView]
        newBbox = OffsetBBox(bbox, bboxOffset)
        viewname = namePrefix + i.LookupParameter("Марка").AsString()
        if viewname in existingPlanNames:
            view = existingPlanElements[existingPlanNames.index(viewname)]
            view.CropBox = newBbox
            view.CropBoxActive = True
            view.CropBoxVisible = False
            floorPlans.append(view)
        else:
            view = ViewPlan.Create(doc, viewType.Id, level.Id)
            view.ViewName = viewname
            view.CropBox = newBbox
            view.CropBoxActive = True
            view.CropBoxVisible = False
            floorPlans.append(view)

    # End Transaction
    TransactionManager.Instance.TransactionTaskDone()

else:
    floorPlans = "RunIt set to False"

OUT = floorPlans
