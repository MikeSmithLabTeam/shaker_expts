###===================================================================================================
### Dimple Pattern Script
### This script needs to be inserted into the Fusion 360 Script Editor and then can be loaded 
### from within Fusion360 to create a dimple pattern of dots on a surface.
### Saving the Fusion360 pattern the workshop can load this and use it pattern the surface.
### On my system this folder is located here: C:\Users\ppzmis\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\Scripts
###===================================================================================================
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math




def run(context):
    ui = None
    L_D = 1.2
    ball_diam = 4.0
    n_side=10 # This is the number of particles on the side of the outermost hexagonal ring

       
        
    class Vector:
        def __init__(self, x,y):
            self.x = x
            self.y = y
        
        def __add__(self, other):
            return Vector(self.x + other.x, self.y + other.y)
        
        def __sub__(self, other):
            return Vector(self.x - other.x, self.y - other.y)
        
        def __mul__(self, other):
            return Vector(self.x * other, self.y * other)
        
        def __rmul__(self, other):
            return Vector(self.x * other, self.y * other)
        
        def __truediv__(self, other):
            return Vector(self.x / other, self.y / other)

    #Vectors for dimple-lattice
    vec_dimple_A = Vector(L_D*ball_diam, 0) # unit vec in x direction (increasing)
    vec_dimple_B = Vector(L_D*ball_diam / 2, math.sqrt(3)*L_D*ball_diam/2)# Up and to the right 
    vec_dimple_C = vec_dimple_B-vec_dimple_A
   
        
    try:
        def create_grid(sketch, n_upper, n_lower):
            create_dot(sketch, Vector(0,0))
            for i in range(n_lower, n_upper):
                hexagon(sketch, i)
        

        def hexagon(sketch, n):
            for i in range(n):
                create_dot(sketch, vec_dimple_A*n + vec_dimple_C*i)#From left of centre upwards to the right
                create_dot(sketch, vec_dimple_A*-n - vec_dimple_C*i)#From right of centre downwards to the left
                create_dot(sketch, vec_dimple_B*-n + vec_dimple_A*i)#Along the bottom edge horizontally
                create_dot(sketch, vec_dimple_B*n - vec_dimple_A*i)#Along the top edge horizontally
                create_dot(sketch, vec_dimple_C*-n + vec_dimple_B*i)
                create_dot(sketch, vec_dimple_C*n - vec_dimple_B*i)
            

        def create_dot(sketch, pos, rad=0.5):
            sketch.sketchPoints.add(adsk.core.Point3D.create(pos.x,pos.y,0))


        app = adsk.core.Application.get()
        

        design = adsk.fusion.Design.cast(app.activeProduct)
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        vec=Vector(0,0)

        

        create_grid(sketch, 26, 0)
        
        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))