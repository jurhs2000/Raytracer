# Universidad del Valle de Guatemala
# Graficas por computadora - CC3044 - Seccion 20
# Julio Roberto Herrera Saban - 19402
# Proyecto 2 - 

from src.glMath import createObjectMatrix, transformV3
from src.objLoader import EnvironmentMap, Obj, Texture
from src.gl import Raytracer
from src.glModels import REFLECTIVE, TRANSPARENT, AmbientLight, DirectionalLight, PointLight, Material
from src.glTypes import V3, newColor
from src.figures import AABB, Sphere, Triangle

width = 240
height = 240

white = Material(newColor(1, 1, 1))
brick = Material(newColor(0.8, 0.25, 0.25), specularity=32)
stone = Material(newColor(0.4, 0.4, 0.4), specularity=64)
green = Material(newColor(0.4, 1, 0), specularity=128)
mirror = Material(specularity=128, type=REFLECTIVE)
gold = Material(newColor(1, 0.8, 0), specularity=32, type=REFLECTIVE)
glass = Material(specularity=64, ior=1.5, type=TRANSPARENT)
water = Material(specularity=64, ior=1.33, type=TRANSPARENT)
diamond = Material(specularity = 64, ior = 2.417, type = TRANSPARENT)
earth = Material(texture=Texture('textures/earthDay.bmp'))
box = Material(texture=Texture('textures/box.jpg'))

rt = Raytracer(width, height)
rt.environmentMap = EnvironmentMap('textures/envmap_playa.bmp')

rt.pointLights.append(PointLight(position=V3(0, 2, 0), intensity=0.5))
rt.ambientLight = AmbientLight(strength=0.1)
rt.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)

#rt.scene.append(Sphere(V3(0, 0, -8), 2.2, earth))
#rt.scene.append(AABB(position=V3(0, -3, -10), size=V3(5, 0.2, 5), material=box))

#'''
model = Obj('models/face/face.obj')
translate=V3(0, 0, -3.8)
scale=V3(0.8,0.8,0.8)
rotate=V3(0,45,0)
modelMatrix = createObjectMatrix(translate, scale, rotate)
count = 0

for face in model.faces:
  print(f'{count}/{len(model.faces)}')
  A = V3(model.vertices[face[0][0] - 1][0], model.vertices[face[0][0] - 1][1], model.vertices[face[0][0] - 1][2])
  B = V3(model.vertices[face[1][0] - 1][0], model.vertices[face[1][0] - 1][1], model.vertices[face[1][0] - 1][2])
  C = V3(model.vertices[face[2][0] - 1][0], model.vertices[face[2][0] - 1][1], model.vertices[face[2][0] - 1][2])
  A = transformV3(A, modelMatrix)
  B = transformV3(B, modelMatrix)
  C = transformV3(C, modelMatrix)
  rt.scene.append(Triangle(A, B, C, material=mirror))
  count += 1
#'''
#'''
rt.scene.append(Triangle(V3(-2, -2, -10), V3(2, -2, -10), V3(0, 2, -10), glass))
rt.scene.append(Triangle(V3(-2, -8, -15), V3(2, -4, -10), V3(0, -1, -20), glass))
rt.scene.append(Sphere(V3(0, 0, -8), 1, glass))
#'''
rt.glRender()
rt.glFinish("outputs/P2.bmp")
