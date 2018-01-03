import math

from OCC.gp import *
from OCC.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.GCE2d import GCE2d_MakeSegment
from OCC.Geom import Geom_Plane, Geom_CylindricalSurface, Handle_Geom_Plane, Handle_Geom_Surface
from OCC.Geom2d import Geom2d_Ellipse, Geom2d_TrimmedCurve, Handle_Geom2d_Ellipse, Handle_Geom2d_Curve
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, \
    BRepBuilderAPI_Transform
from OCC.BRepPrimAPI import BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCC.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.BRepOffsetAPI import BRepOffsetAPI_MakeThickSolid, BRepOffsetAPI_ThruSections
from OCC.BRepLib import breplib
from OCC.BRep import BRep_Tool_Surface, BRep_Builder
from OCC.TopoDS import topods, TopoDS_Edge, TopoDS_Compound
from OCC.TopExp import TopExp_Explorer
from OCC.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.TopTools import TopTools_ListOfShape

from OCC.Display.SimpleGui import *

H = 6
w1 = 5
k = 4.5
h1 = 4
height = 20



def face_is_plane(face):
    """
    Returns True if the TopoDS_Shape is a plane, False otherwise
    """
    hs = BRep_Tool_Surface(face)
    downcast_result = Handle_Geom_Plane.DownCast(hs)
    # The handle is null if downcast failed or is not possible, that is to say the face is not a plane
    if downcast_result.IsNull():
        return False
    else:
        return True


def geom_plane_from_face(aFace):
    """
    Returns the geometric plane entity from a planar surface
    """
    return Handle_Geom_Plane.DownCast(BRep_Tool_Surface(aFace)).GetObject()
    
display, start_display, add_menu, add_function_to_menu = init_display()

class sliderails():

    # fill the gp_Pnt() Point to connect  
    def makeSegment(self, Pnta, Pntb):
        Segment = GC_MakeSegment(Pnta, Pntb)
        return Segment
    
    def buildEdge(self, segment):
        Edge = BRepBuilderAPI_MakeEdge(segment.Value())
        return Edge
        
    
#qmake silde rails point 
aPnt1 = gp_Pnt(0, 0, 0)
aPnt2 = gp_Pnt(0, w1 / 2.0, 0)
aPnt3 = gp_Pnt(0, w1 / 2.0, H-k)
aPnt4 = gp_Pnt(0, w1 / 2.5, H-k)
aPnt5 = gp_Pnt(0, w1 / 2.5, H-k+0.5)
aPnt6 = gp_Pnt(0, w1 / 2.0 , H-k+0.5)
aPnt7 = gp_Pnt(0, w1/2, h1)
aPnt8 = gp_Pnt(0, 0, h1)

a = sliderails() 
b = a.makeSegment(aPnt1, aPnt2)
print(type(b))

aSegment1 = GC_MakeSegment(aPnt1, aPnt2)
aSegment2 = GC_MakeSegment(aPnt2, aPnt3)
aSegment3 = GC_MakeSegment(aPnt3, aPnt4)
aSegment4 = GC_MakeSegment(aPnt4, aPnt5)
aSegment5 = GC_MakeSegment(aPnt5, aPnt6)
aSegment6 = GC_MakeSegment(aPnt6, aPnt7)
aSegment7 = GC_MakeSegment(aPnt7, aPnt8)
aSegment8 = GC_MakeSegment(aPnt8, aPnt1)


aEdge1 = BRepBuilderAPI_MakeEdge(aSegment1.Value())  #curve
aEdge2 = BRepBuilderAPI_MakeEdge(aSegment2.Value())
aEdge3 = BRepBuilderAPI_MakeEdge(aSegment3.Value())
aEdge4 = BRepBuilderAPI_MakeEdge(aSegment4.Value())
aEdge5 = BRepBuilderAPI_MakeEdge(aSegment5.Value())
aEdge6 = BRepBuilderAPI_MakeEdge(aSegment6.Value())
aEdge7 = BRepBuilderAPI_MakeEdge(aSegment7.Value())
aEdge8 = BRepBuilderAPI_MakeEdge(aSegment8.Value())


#aWire = BRepBuilderAPI_MakeWire(aEdge1.Edge(), aEdge2.Edge(), aEdge3.Edge())

mkWire = BRepBuilderAPI_MakeWire()
#mkWire.Add(aWire.Wire())
mkWire.Add(aEdge1.Edge())
mkWire.Add(aEdge2.Edge())
mkWire.Add(aEdge3.Edge())
mkWire.Add(aEdge4.Edge())
mkWire.Add(aEdge5.Edge())
mkWire.Add(aEdge6.Edge())
mkWire.Add(aEdge7.Edge())
#mkWire.Add(aEdge8.Edge())



zAxis = gp_OZ()

aTrsf = gp_Trsf()
aTrsf.SetMirror(zAxis)

aBRespTrsf = BRepBuilderAPI_Transform(mkWire.Wire(), aTrsf)

aMirroredShape = aBRespTrsf.Shape()
aMirroredWire = topods.Wire(aMirroredShape)

mkWire1 = BRepBuilderAPI_MakeWire()
mkWire1.Add(mkWire.Wire())
mkWire1.Add(aMirroredWire)
myWireProfile = mkWire1.Wire()



# The face that we'll sweep to make the prism
myFaceProfile = BRepBuilderAPI_MakeFace(myWireProfile)


aPrismVec = gp_Vec(height, 0, 0)

myBody = BRepPrimAPI_MakePrism(myFaceProfile.Face(), aPrismVec)

mkFillet = BRepFilletAPI_MakeFillet(myBody.Shape())
anEdgeExplorer = TopExp_Explorer(myBody.Shape(), TopAbs_EDGE)



display.DisplayShape(myBody.Shape(), update=True)
start_display()
