# coding=utf-8
import clr
from math import *

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

DPoint = Autodesk.DesignScript.Geometry.Point
DPolyCurve = Autodesk.DesignScript.Geometry.PolyCurve
DCurve = Autodesk.DesignScript.Geometry.Curve
DSurface = Autodesk.DesignScript.Geometry.Surface
DGeometry = Autodesk.DesignScript.Geometry.Geometry
DSolid = Autodesk.DesignScript.Geometry.Solid
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
from System.Collections.Generic import *

links = FilteredElementCollector(doc).OfClass(Autodesk.Revit.DB.RevitLinkInstance).ToElements()
linkdocs = []
for i in links:
    linkdocs.append(i.GetLinkDocument())
linkids = []
linkwindows = []
linkdoors = []
linkwalls = []
linkfloors = []
linkroofs = []
i = 0
for linkdoc in linkdocs:
    linkids.append(str(links[i].Id))
    linkwindows.append(FilteredElementCollector(linkdoc).OfCategory(
        BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements())
    linkdoors.append(FilteredElementCollector(linkdoc).OfCategory(
        BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements())
    linkwalls.append(FilteredElementCollector(linkdoc).OfCategory(
        BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements())
    linkfloors.append(FilteredElementCollector(linkdoc).OfCategory(
        BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements())
    linkroofs.append(FilteredElementCollector(linkdoc).OfCategory(
        BuiltInCategory.OST_Roofs).WhereElementIsNotElementType().ToElements())
    i = i + 1
# ---------------------Методы для расчёта
options = Autodesk.Revit.DB.Analysis.EnergyAnalysisDetailModelOptions()
options.Tier = Autodesk.Revit.DB.Analysis.EnergyAnalysisDetailModelTier.Final
# -------Создание аналитической модели---------------
TransactionManager.Instance.EnsureInTransaction(doc)
eadm = Autodesk.Revit.DB.Analysis.EnergyAnalysisDetailModel.Create(doc, options)
TransactionManager.Instance.TransactionTaskDone()
# -----------------------------------------------------
spaces = eadm.GetAnalyticalSpaces()

# ------------------ВХОДНЫЕ ДАННЫЕ-----------------
parSewall = IN[1]
parSedoor = IN[2]
parSewind = IN[3]
parSiwall = IN[4]
parSidoor = IN[5]
parSiwind = IN[6]
parSceil = IN[7]
parSfloor = IN[8]
parSroof = IN[9]
stte = IN[10]
stti = IN[11]
stkwall = IN[12]
stkdoor = IN[13]
stkwind = IN[14]
sthzemli = IN[15]
sthmax = IN[16]
stked = IN[17]
parte = IN[18]  # Имя параметра температуры наружнего воздуха в Информации о проекте
parti = IN[19]  # Имя параметра температуры внутреннего воздуха в помещении
park = IN[20]  # Имя параметра Коэффициента теплопередачи у Стен, Окон, Дверей, Перекрытий, Крыш
parhzemli = IN[21]  # Имя параметра отметки земли относительно 0.000
parQiwall = IN[22]
parQewall = IN[23]
parQfloor = IN[24]
parQroof = IN[25]
parQdoor = IN[26]
parQwind = IN[27]
parQall = IN[28]
stkroof = IN[30]
parked = IN[31]
par_reset = IN[32]
st_k_floor = IN[33]
par_ground = IN[34]
par_lagi = IN[35]


# -------------------------ФУНКЦИИ---------------------
def storona(angle):
    angle = round(angle, 4)
    if angle > 5.8905 or angle <= 0.3927:
        orient_s = "С"
    elif angle > 0.3927 and angle <= 1.1781:
        orient_s = "СВ"
    elif angle > 1.1781 and angle <= 1.9635:
        orient_s = "В"
    elif angle > 1.9635 and angle <= 2.7489:
        orient_s = "ЮВ"
    elif angle > 2.7489 and angle <= 3.5343:
        orient_s = "Ю"
    elif angle > 3.5343 and angle <= 4.3197:
        orient_s = "ЮЗ"
    elif angle > 4.3197 and angle <= 5.1051:
        orient_s = "З"
    elif angle > 5.1051 and angle <= 5.8905:
        orient_s = "СЗ"
    if orient_s in ["С", "В", "СВ", "СЗ"]:
        koef_s = 1.1
    elif orient_s in ["З", "ЮВ"]:
        koef_s = 1.05
    elif orient_s in ["Ю", "ЮЗ"]:
        koef_s = 1
    return koef_s


def get_type(obj):
    try:
        objtype = oobj.Symbol
    except:
        try:
            objtype = oobj.WallType
        except:
            try:
                objtype = oobj.FloorType
            except:
                try:
                    objtype = oobj.RoofType
                except:
                    objtype = None
    return objtype


def get_K(obj, stk):
    objtype = get_type(obj)
    try:
        kobj = objtype.LookupParameter(park).AsDouble()
        if kobj is None or kobj == 0:
            K = stk
        else:
            K = kobj
    except:
        K = stk
    return K


def get_obj_from_link(surface, linkwalls):
    nameobj = surface.OriginatingElementDescription
    objid = nameobj[nameobj.find("[") + 1:nameobj.find("]")]
    obj1 = None
    try:
        lk = surface.CADLinkUniqueId
        linkid1 = str(doc.GetElement(lk).Id)
        i = 0
        for linkid2 in linkids:
            if linkid1 == linkid2:
                for wall in linkwalls[i]:
                    if str(wall.Id) == objid:
                        obj1 = wall
            i = i + 1
    except:
        errors.append(type)
    return obj1


# --------------------ПУСТЫЕ СПИСКИ---------------------
list = []
list3 = []
list4 = []
list5 = []
errors = []
# --------------------ОСНОВНОЙ КОД-------------------------
info1 = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_ProjectInformation).ToElements()
info = info1[0]
infote = info.LookupParameter(parte).AsInteger()
if infote is None or infote == 0:
    t_out = stte
else:
    t_out = infote

for space in spaces:
    sp = doc.GetElement(space.CADObjectUniqueId)
    reset = sp.LookupParameter(par_reset).AsValueString()
    if space.Area > 0 and (reset == "Нет" or reset == "No"):
        surfaces = space.GetAnalyticalSurfaces()
        list.append(reset)
        Siwall = 0
        Sewall = 0
        Sfloor = 0
        Sceil = 0
        Sroof = 0
        Sewind = 0
        Sedoor = 0
        Siwind = 0
        Sidoor = 0
        Qiwall = 0
        Qewall = 0
        Qfloor = 0
        Qroof = 0
        Qwind = 0
        Qdoor = 0
        Qall = 0
        try:
            sp_ti = sp.LookupParameter(parti).AsInteger()
            if sp_ti is None or sp_ti == 0:
                t_in = stti
            else:
                t_in = sp_ti
        except:
            t_in = stti
        for surface in surfaces:
            # try:
            name = surface.SurfaceName
            type = str(surface.SurfaceType)
            list3.append(type)
            azimuth = surface.Azimuth
            koef_s = storona(azimuth)
            area = surface.get_Parameter(BuiltInParameter.RBS_GBXML_SURFACE_AREA).AsDouble() * 0.09290304
            tilt = surface.Tilt
            space1 = surface.get_Parameter(BuiltInParameter.RBS_ENERGY_ANALYSIS_SURFACE_ADJACENT_SPACE_ID1).AsString()
            space2 = surface.get_Parameter(BuiltInParameter.RBS_ENERGY_ANALYSIS_SURFACE_ADJACENT_SPACE_ID2).AsString()
            objid = surface.CADObjectUniqueId
            obj = doc.GetElement(objid)
            opens = surface.GetAnalyticalOpenings()

            # --------------РАСЧЕТ ТЕПЛОПОТЕРЬ ЧЕРЕЗ НАРУЖНЫЕ СТЕНЫ--------------

            if type == "ExteriorWall":
                Sewall = Sewall + area
                if obj is None:
                    obj = get_obj_from_link(surface, linkwalls)
                Kwall = get_K(obj, stkwall)
                for open in opens:
                    oname = open.OpeningName
                    otype = str(open.OpeningType)
                    oarea = 0
                    oobj = 0
                    oarea = open.Parameter[BuiltInParameter.RBS_GBXML_SURFACE_AREA].AsDouble() * 0.09290304
                    oobjid = open.CADObjectUniqueId
                    oobj = doc.GetElement(oobjid)
                    if otype == "Window":
                        Sewall = Sewall - oarea
                        Sewind = Sewind + oarea
                        if oobj is None:
                            oobj = get_obj_from_link(open, linkwindows)
                        K = get_K(oobj, stkwind)
                        Qwind = Qwind + K * oarea * (t_in - t_out) * koef_s
                    elif otype == "Door":
                        Sewall = Sewall - oarea
                        Sedoor = Sedoor + oarea
                        if oobj is None:
                            oobj = get_obj_from_link(open, linkdoors)
                        K = get_K(oobj, stkdoor)
                        hd = oobj.Location.Point.Z * 304.8
                        Qdoor = Qdoor + K * oarea * (t_in - t_out) * (koef_s + (sthmax - hd) / 1000 * stked)
                Qewall = Qewall + Kwall * area * (t_in - t_out) * koef_s

            # ------------РАСЧЕТ ТЕПЛОПОТЕРЬ ЧЕРЕЗ ВНУТРЕННИЕ СТЕНЫ-------

            elif type == "InteriorWall":
                Siwall = Siwall + area
                for open in opens:
                    k = dir(open)
                    oname = open.OpeningName
                    otype = str(open.OpeningType)
                    oarea = 0
                    oobj = 0
                    oarea = open.Parameter[BuiltInParameter.RBS_GBXML_SURFACE_AREA].AsDouble() * 0.09290304
                    oobj = open.Parameter[BuiltInParameter.RBS_ENERGY_ANALYSIS_SURFACE_CADOBJECTID].AsString()
                    if otype == "Window":
                        Siwall = Siwall - oarea
                        Siwind = Siwind + oarea
                    elif otype == "Door":
                        Siwall = Siwall - oarea
                        Sidoor = Sidoor + oarea
            elif type == "Ceiling":
                Sceil = Sceil + area
            elif type == "InteriorFloor":
                0
                # Sfloor = Sfloor + area
                """elif type == "ExteriorFloor":
                Sfloor = Sfloor + area
                if obj is None:
                    obj = get_obj_from_link(surface,linkfloors)
                Kfloor = get_K(obj,st_k_floor)

#---------------РАСЧЕТ ПОЛА ПО ГРУНТУ----------------------------------

                ground = obj.LookupParameter(par_ground).AsValueString()
                pcrv = surface.GetPolyloop().GetPoints()
                list11=[]
                for l1 in pcrv:
                    list11.append(DPoint.ByCoordinates(l1.X*304.8,l1.Y*304.8,l1.Z*304.8))
                pcrv1 = DPolyCurve.ByPoints(DPoint.PruneDuplicates(list11,1),1)
                surf = DSurface.ByPatch(pcrv1)
                solid1 = surf.Thicken(-1000,0)
                if ground=="Да" or ground=="Yes":
                    Lagi = 1
                    klagi = obj.LookupParameter(par_lagi).AsValueString()
                    if klagi=="Да" or klagi=="Yes":
                        Lagi = 1.18
                    TransactionManager.Instance.EnsureInTransaction(doc)
                    obj.SlabShapeEditor.Enable()
                    pts = obj.SlabShapeEditor.SlabShapeVertices
                    TransactionManager.Instance.TransactionTaskDone()
                    points = []
                    for pt in pts:
                        points.append(pt.Position)
                    list11=[]
                    for l1 in points:
                        list11.append(DPoint.ByCoordinates(l1.X*304.8,l1.Y*304.8,l1.Z*304.8))
                    pcurve1 = DPolyCurve.ByPoints(DPoint.PruneDuplicates(list11,1),1)
                    list5.append(pcurve1)
                    offset=-2000
                    list6=[]
                    listR = [0.4762,0.2326,0.1163,0.0704]
                    sumA = 0
                    for R in listR:
                        try:
                            pcurve2 = pcurve1.Offset(offset)
                            surf1 = DSurface.ByPatch(pcurve1)
                            surf2 = DSurface.ByPatch(pcurve2)
                            geom = surf1.Split(surf2)
                            pcurve1=pcurve2
                            solid2 = geom[0].Thicken(1000,0)
                            intersects = solid1.Intersect(solid2)
                            S=0
                            for intersect in intersects:
                                S = S+intersect.Volume
                            A = S/1000000000
                            sumA = sumA + A
                            Qfloor = Qfloor + (R+Kfloor)*A*(t_in-t_out)/Lagi
                        except:
                            0
                    if area > sumA:
                        Qfloor = Qfloor + Kfloor*(area-sumA)*(t_in-t_out)/Lagi	"""

            # ---------------РАСЧЕТ ТЕПЛОПОТЕРЬ ЧЕРЕЗ КРОВЛЮ------------

            elif type == "Roof":
                Sroof = Sroof + area
                if obj is None:
                    obj = get_obj_from_link(surface, linkfloors)
                if obj is None:
                    obj = get_obj_from_link(surface, linkroofs)
                K = get_K(obj, stkroof)
                Qroof = Qroof + K * area * (t_in - t_out)

            # -----------------РАСЧЕТ СТЕН ПОДВАЛА-------------

            elif type == "Underground":
                Sewall = Sewall + area
                if obj is None:
                    obj = get_obj_from_link(surface, linkfloors)
                tp = obj.Category.Name
                if tp == "Перекрытие" or "Floor":
                    0
                    # except:
                    # 0
                    # --------------------СУММИРОВАНИЕ ПОЛНЫХ ТЕПЛОПОТЕРЬ----------

        Qall = Qewall + Qwind + Qdoor + Qfloor + Qroof + Qiwall

        # -----------------ВНЕСЕНИЕ ЗНАЧЕНИЙ В ПОМЕЩЕНИЯ----------------

        if sp.Area > 0:
            TransactionManager.Instance.EnsureInTransaction(doc)
            sp.LookupParameter(parSewall).Set(Sewall)
            sp.LookupParameter(parSedoor).Set(Sedoor)
            sp.LookupParameter(parSewind).Set(Sewind)
            sp.LookupParameter(parSiwall).Set(Siwall)
            sp.LookupParameter(parSidoor).Set(Sidoor)
            sp.LookupParameter(parSiwind).Set(Siwind)
            sp.LookupParameter(parSceil).Set(Sceil)
            sp.LookupParameter(parSfloor).Set(Sfloor)
            sp.LookupParameter(parSroof).Set(Sroof)
            sp.LookupParameter(parQewall).Set(Qewall)
            sp.LookupParameter(parQdoor).Set(Qdoor)
            sp.LookupParameter(parQwind).Set(Qwind)
            sp.LookupParameter(parQroof).Set(Qroof)
            sp.LookupParameter(parQfloor).Set(Qfloor)
            sp.LookupParameter(parQall).Set(Qall)
            TransactionManager.Instance.TransactionTaskDone()
# -----Удаление модели---------------------
"""
TransactionManager.Instance.EnsureInTransaction(doc)	
doc.Delete(eadm.Id)
TransactionManager.Instance.TransactionTaskDone()
"""
# ------------------------------------------------------
geom_opt = app.Create.NewGeometryOptions()
OUT = "ok"