import clr

clr.AddReference('RevitApi')
from Autodesk.Revit.DB import *
from System.Collections.Generic import *

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
view = doc.ActiveView

#name = IN[0]
#category = IN[1]
#parameterrule = IN[3]
#parametervalue = IN[4]

categories = []
categories.Add(ElementId(BuiltinCategory.OST_Pipes))

collector = FilteredElementCollector(doc, uidoc.ActiveView.Id)
pipesList = collector.OfCategory(BuiltinCategory.OST_Pipes).ToElements()

rules = []
rules.Add(ParameterFilterRuleFactory.CreateEqualsRule(pipeMark.Id, "string", False))

#TransactionManager.Instance.EnsureInTransaction(doc)
#filter = ParameterFilterElement.Create(doc, 'Test', categories, rules)
#view.AddFilter(filter.Id)

#TransactionManager.Instance.TransactionTaskDone()
OUT = rules