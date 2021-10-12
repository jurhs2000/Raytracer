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

width = 1600
height = 800

white = Material(newColor(1, 1, 1))
red = Material(newColor(1, 0.2, 0.2))
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
earth = Material(texture=Texture('models/face/face.bmp'))
brickTexture = Material(texture=Texture('textures/brick.jpg'))
brickTexture2 = Material(texture=Texture('textures/brick2.jpg'))
floor = Material(texture=Texture('textures/floor.png'))
floorReflective = Material(texture=Texture('textures/floor2.jpg'), specularity=80, type=REFLECTIVE)
roof = Material(texture=Texture('textures/roof.jpg'))
ds = Material(texture=Texture('textures/deathStar.jpg', 250, 20))

rt = Raytracer(width, height)
rt.environmentMap = EnvironmentMap('textures/dikhololo_night.jpg')

rt.pointLights.append(PointLight(position=V3(5, 5, -38), intensity=0.5))
rt.pointLights.append(PointLight(position=V3(-10, -5, -28), intensity=0.2, color=newColor(1, 0.2, 0.2)))
rt.pointLights.append(PointLight(position=V3(-10, -5, -10), intensity=0.1, color=newColor(1, 1, 1)))
rt.ambientLight = AmbientLight(strength=0.2)
rt.directionalLight = DirectionalLight(direction=V3(-5, 0, 10), intensity=0.5)

#rt.scene.append(Sphere(V3(0, 0, -8), 2.2, earth))
#rt.scene.append(AABB(position=V3(0, -3, -10), size=V3(5, 0.2, 5), material=box))

#'''
model = Obj('models/face/face.obj')
translate=V3(3, 0, -4)
scale=V3(0.8,0.8,0.8)
rotate=V3(0,-45,0)
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
  rt.scene.append(Triangle(A, B, C, material=white))
  count += 1
#'''

#'''
rt.scene.append(AABB(V3(-10,-7,-30), V3(30,12,1), material=brickTexture))
rt.scene.append(AABB(V3(-10,10,-30), V3(30,6,1), material=brickTexture))
rt.scene.append(AABB(V3(-23,3,-30), V3(4,8,1), material=brickTexture))
rt.scene.append(AABB(V3(-13,3,-30), V3(1,8,1), material=brickTexture))
rt.scene.append(AABB(V3(3,3,-30), V3(4,8,1), material=brickTexture))
rt.scene.append(AABB(V3(-26,0,-20), V3(2,26,20), material=brickTexture2))
rt.scene.append(AABB(V3(-10,-13,-20), V3(30,1,20), material=floorReflective))
rt.scene.append(AABB(V3(-10,13,-20), V3(30,1,20), material=roof))
#'''

rt.scene.append(Sphere(V3(200, 150, -400), 30, ds))
rt.scene.append(Sphere(V3(-10, -5, -26), 1, red))

rt.scene.append(Sphere(V3(-23, 10, -28), 1, mirror))
rt.scene.append(Sphere(V3(-23, 10, -26), 1, mirror))
rt.scene.append(Sphere(V3(-23, 10, -24), 1, mirror))
rt.scene.append(Sphere(V3(-23, 10, -22), 1, mirror))
rt.scene.append(Sphere(V3(-23, 10, -20), 1, mirror))

rt.scene.append(Triangle(V3(240, 150, -360), V3(200, 110, -360), V3(250, 110, -410), glass))
rt.scene.append(Triangle(V3(130, 140, -360), V3(140, 110, -360), V3(200, 110, -410), glass))

rt.scene.append(Sphere(V3(7, 5, -10), 0.5, water))
rt.scene.append(Sphere(V3(4, -10, -18), 0.5, water))
rt.scene.append(Sphere(V3(5, 3, -22), 0.5, water))
rt.scene.append(Sphere(V3(6, -4, -14), 0.5, water))
rt.scene.append(Sphere(V3(8, 9, -25), 0.5, water))
rt.scene.append(Sphere(V3(10, 8, -33), 0.5, water))
rt.scene.append(Sphere(V3(9, -8, -35), 0.5, water))

rt.scene.append(Sphere(V3(12, 6, -28), 0.5, water))
rt.scene.append(Sphere(V3(14, -6, -18), 0.5, water))
rt.scene.append(Sphere(V3(13, -4, -34), 0.5, water))
rt.scene.append(Sphere(V3(15, 3, -26), 0.5, water))
rt.scene.append(Sphere(V3(16, -2, -30), 0.5, water))

rt.scene.append(Sphere(V3(13, 8, -14), 0.5, water))
rt.scene.append(Sphere(V3(15, -9, -34), 0.5, water))
rt.scene.append(Sphere(V3(18, 1, -18), 0.5, water))
rt.scene.append(Sphere(V3(20, -13, -24), 0.5, water))
rt.scene.append(Sphere(V3(21, 7, -29), 0.5, water))
rt.scene.append(Sphere(V3(24, 10, -30), 0.5, water))
rt.scene.append(Sphere(V3(28, -4, -35), 0.5, water))

rt.scene.append(Sphere(V3(-3, 4, -33), 0.5, water))
rt.scene.append(Sphere(V3(-7, -1, -35), 0.5, water))
rt.scene.append(Sphere(V3(-20, 8, -38), 0.5, water))
rt.scene.append(Sphere(V3(-16, 4, -36), 0.5, water))
rt.scene.append(Sphere(V3(-18, 1, -34), 0.5, water))
rt.scene.append(Sphere(V3(-8, 5, -39), 0.5, water))
rt.scene.append(Sphere(V3(-11, 4, -40), 0.5, water))
rt.scene.append(Sphere(V3(-22, 6, -41), 0.5, water))

'''
rt.scene.append(Triangle(V3(-2, -2, -10), V3(2, -2, -10), V3(0, 2, -10), mirror))
rt.scene.append(Triangle(V3(-2, -8, -15), V3(2, -4, -10), V3(0, -1, -20), green))
rt.scene.append(Sphere(V3(0, 2, -5), 1, mirror))
'''
rt.glRender()
rt.glFinish("outputs/P2.bmp")
