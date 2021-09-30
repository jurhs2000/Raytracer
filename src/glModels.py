from src.glMath import divide, norm
from src.glTypes import V3, WHITE

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

MAX_RECURSION_DEPTH = 3

class Material(object):
  def __init__(self, diffuse = WHITE, specularity = 1, ior = 1, texture = None, type = OPAQUE):
    self.diffuse = diffuse
    self.specularity = specularity
    self.ior = ior
    self.texture = texture
    self.type = type

class Intersect(object):
  def __init__(self, distance, point, normal, textCoords, sceneObject):
    self.distance = distance
    self.point = point
    self.normal = normal
    self.textCoords = textCoords
    self.sceneObject = sceneObject

class PointLight(object):
  def __init__(self, position=V3(0,0,0), intensity=1, color=WHITE):
    self.position = position
    self.intensity = intensity
    self.color = color

class AmbientLight(object):
  def __init__(self, strength=0, color=WHITE):
    self.strength = strength
    self.color = color

class DirectionalLight(object):
  def __init__(self, direction=V3(0,-1,0), intensity=1, color=WHITE):
    self.direction = divide(direction, norm(direction))
    self.intensity = intensity
    self.color = color
