# Universidad del Valle de Guatemala
# Graficas por computadora - CC3044 - Seccion 20
# Julio Roberto Herrera Saban - 19402
# RT1: Spheres and Materials

from src.gl import Raytracer
from src.glModels import AmbientLight, DirectionalLight, PointLight, Material
from src.glTypes import V3, newColor
from src.figures import Sphere

width = 768
height = 768

brick = Material(newColor(0.8, 0.25, 0.25), specularity=32)
stone = Material(newColor(0.4, 0.4, 0.4), specularity=64)
green = Material(newColor(0.4, 1, 0), specularity=128)

rt = Raytracer(width, height)

#rt.pointLights.append(PointLight(position=V3(5, -7, 0)))
rt.pointLights.append(PointLight(position=V3(-10, 2, 0)))
rt.ambientLight = AmbientLight(strength=0.1)
rt.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)

rt.scene.append(Sphere(V3(0, 0, -8), 2, green))
rt.scene.append(Sphere(V3(-1,1,-5), 0.5, stone))
rt.scene.append(Sphere(V3(0.5,0.5,-5), 0.5, brick))

rt.glRender()
rt.glFinish("outputs/light.bmp")
