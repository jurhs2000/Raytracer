# Universidad del Valle de Guatemala
# Graficas por computadora - CC3044 - Seccion 20
# Julio Roberto Herrera Saban - 19402
# RT1: Spheres and Materials

from src.gl import Raytracer
from src.glTypes import V3, newColor
from src.figures import Sphere
from src.glMaterials import Material
from src.glMath import sum

width = 1200
height = 768

snow = Material(newColor(0.9, 0.9, 0.9))
nose = Material(newColor(1,0.2509,0.1372))
brownButton = Material(newColor(0.3519,0.1529,0.1608))
blackButton = Material(newColor(0,0,0))
eyeSclera = Material(newColor(0.8,0.8,0.9))

rt = Raytracer(width, height)

snPos = V3(0, 5, -30)
rt.scene.append(Sphere(sum(snPos, V3(0,8,0)), 4, snow))
rt.scene.append(Sphere(sum(snPos, V3(0,0,0)), 6, snow))
rt.scene.append(Sphere(sum(snPos, V3(0,-9,0)), 8, snow))

rt.scene.append(Sphere(sum(snPos, V3(-1,8,4)), 0.5, eyeSclera))
rt.scene.append(Sphere(sum(snPos, V3(-1,7.7,4.5)), 0.3, blackButton))
rt.scene.append(Sphere(sum(snPos, V3(-0.8,7.4,4.8)), 0.1, snow))
rt.scene.append(Sphere(sum(snPos, V3(1,8,4)), 0.5, eyeSclera))
rt.scene.append(Sphere(sum(snPos, V3(1,7.7,4.5)), 0.3, blackButton))
rt.scene.append(Sphere(sum(snPos, V3(1.2,7.4,4.8)), 0.1, snow))

rt.scene.append(Sphere(sum(snPos, V3(0,6.5,4)), 0.85, nose))

rt.scene.append(Sphere(sum(snPos, V3(-1.3,5.24,4)), 0.25, brownButton))
rt.scene.append(Sphere(sum(snPos, V3(-0.45,4.9,4)), 0.25, brownButton))
rt.scene.append(Sphere(sum(snPos, V3(0.45,4.92,4)), 0.25, brownButton))
rt.scene.append(Sphere(sum(snPos, V3(1.3,5.27,4)), 0.25, brownButton))

rt.scene.append(Sphere(sum(snPos, V3(0,0.3,6)), 0.8, blackButton))
rt.scene.append(Sphere(sum(snPos, V3(0,-3.25,8)), 1, blackButton))
rt.scene.append(Sphere(sum(snPos, V3(0,-8,8)), 1.2, blackButton))
rt.glRender()
rt.glFinish("outputs/RT1.bmp")
