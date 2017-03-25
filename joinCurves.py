import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

reset = IN[0]


def iterate(src, res):
    for k, i in enumerate(src):
        vec1 = Vector.ByTwoPoints(i.EndPoint, res[-1].StartPoint).Length
        vec2 = Vector.ByTwoPoints(i.StartPoint, res[-1].EndPoint).Length
        vec3 = Vector.ByTwoPoints(i.EndPoint, res[-1].EndPoint).Length
        vec4 = Vector.ByTwoPoints(i.StartPoint, res[-1].StartPoint).Length

        gap = 0.000001

        if vec1 < gap or vec2 < gap or vec3 < gap or vec4 < gap:
            res.Add(src.pop(k))
            return iterate(src, res)

    return res


src = IN[1]
contour = []
contours = []

while len(src) > 0:
    contour.Add(src.pop(0))
    contour = iterate(src, contour)
    contours.Add(contour)
    contour = []

OUT = contours