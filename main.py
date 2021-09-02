from src.gl import Raytracer
from src.glTypes import V3, newColor
from src.figures import Sphere
from src.glMaterials import Material

width = 960
height = 540

red = Material(newColor(1, 0, 0))
green = Material(newColor(0, 1, 0))
blue = Material(newColor(0, 0, 1))
white = Material(newColor(1, 1, 1))

rt = Raytracer(width, height)
rt.scene.append(Sphere(V3(0,0,-10), 4, red))
rt.scene.append(Sphere(V3(1,1,-2), 1, green))
rt.scene.append(Sphere(V3(-5,-1,-20), 10, blue))
rt.scene.append(Sphere(V3(1,-1,-5), 1, white))
rt.glRender()
rt.glFinish("outputs/rt.bmp")