# Universidad del Valle de Guatemala
# Graficas por computadora - CC3044 - Seccion 20
# Julio Roberto Herrera Saban - 19402
# RT1: Spheres and Materials

from src.objLoader import EnvironmentMap, Texture
from src.gl import Raytracer
from src.glModels import OPAQUE, REFLECTIVE, TRANSPARENT, AmbientLight, DirectionalLight, PointLight, Material
from src.glTypes import V3, newColor
from src.figures import AABB, Plane, Sphere

width = 2160
height = 768

orange = Material(newColor(1,0.3686,0.0745), specularity = 1, ior = 1, type = OPAQUE)
violet = Material(newColor(0.525, 0.451, 0.631), specularity = 1, ior = 1, type = OPAQUE)
mirror = Material(newColor(1,1,1), specularity=128, ior=1, type=REFLECTIVE)
christmasBall = Material(newColor(1, 0.2, 0), specularity=32, type=REFLECTIVE)
water = Material(newColor(0.8,0.8,1), specularity=64, ior=1.33, type=TRANSPARENT)
germanium = Material(specularity = 128, ior = 4.1, type = TRANSPARENT)

rt = Raytracer(width, height)
rt.environmentMap = EnvironmentMap('textures/outdoor_umbrellas.jpg', -0.25)

rt.ambientLight = AmbientLight(strength=0.1)
rt.pointLights.append(PointLight(position=V3(0, 2, -8), intensity=0.5))
rt.directionalLight = DirectionalLight(direction=V3(1, -1, -2), intensity=0.5)

rt.scene.append(Sphere(center=V3(-8, 2, -8), radius=1.2, material=orange))
rt.scene.append(AABB(position=V3(-4, 2, -8), size=V3(2, 2, 2), material=violet))
rt.scene.append(Sphere(center=V3(4, 2, -8), radius=1.2, material=christmasBall))
rt.scene.append(AABB(position=V3(8, 2, -8), size=V3(2, 2, 2), material=mirror))
rt.scene.append(Sphere(center=V3(-2, -2, -8), radius=1.2, material=water))
rt.scene.append(AABB(position=V3(2, -2, -8), size=V3(2, 2, 2), material=germanium))

#rt.scene.append(Sphere(center=V3(-2, -2, -8), radius=1.2, material=orange))
#rt.scene.append(AABB(position=V3(-2, -2, -8), size=V3(2, 2, 2), material=violet))
#rt.scene.append(Sphere(center=V3(-2, -2, -8), radius=1.2, material=christmasBall))
#rt.scene.append(AABB(position=V3(-2, -2, -8), size=V3(2, 2, 2), material=mirror))
#rt.scene.append(Sphere(center=V3(-2, -2, -8), radius=1.2, material=water))
#rt.scene.append(AABB(position=V3(-2, -2, -8), size=V3(2, 2, 2), material=germanium))

rt.glRender()
rt.glFinish("outputs/RT2.bmp")
