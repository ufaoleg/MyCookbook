import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# ActiveView
view = doc.ActiveView
sc = view.Scale
TransactionManager.Instance.EnsureInTransaction(doc)

go = IN[0] # Boolean that allows it to run
sur = IN[1] # Boolean - only surface patterns
cut = IN[2] # Boolean - only cut patterns
name = IN[3] # Optional - category name
pen = IN[4] # Pen assignment

# We dont want to allow anything else but 0-16 values for pen assignments
if pen > 16:
  pen = 16
elif pen < 1:
  pen = 1

# Start by retrieving all Categories
a = doc.Settings.Categories

names = list()
done = list()
errors = []
gs_cut = GraphicsStyleType.Cut
gs_projection = GraphicsStyleType.Projection
try:
	for cat in a:
		if 'Штриховка разреза' in cat.Name:
			if go and cut:
				cat.SetLineWeight(pen, gs_cut)
				done.append(cat.Name)
			names.append(cat.Name)
		elif 'Штриховка поверхностей' in cat.Name:
			if go and sur:
				cat.SetLineWight(pen, gs_projection)
				done.append(cat.Name)
			names.append(cat.Name)
	
		for sub_cat in cat.SubCategories:
			if 'Штриховка разреза' in sub_cat.Name:
				if go and cut:
					sub_cat.SetLineWeight(pen, gs_cut)
					done.append(cat.Name)
				names.append(sub_cat.Name)
			elif 'Штриховка поверхностей' in sub_cat.Name:
				if go and sur:
					sub_cat.SetLineWeight(pen, gs_projection)
					done.append(cat.Name)
				names.append(sub_cat.Name)
except:
	pass

view.Scale = 1
view.Scale = sc

OUT = 'Possible categories', names, 'Done', done
