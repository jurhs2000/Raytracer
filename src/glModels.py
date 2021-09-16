from src.glMath import divide, norm
from src.glTypes import V3, WHITE

class Material(object):
  def __init__(self, diffuse = WHITE, specularity = 1):
    self.diffuse = diffuse
    self.specularity = specularity

class Intersect(object):
  def __init__(self, distance, point, normal, sceneObject):
    self.distance = distance
    self.point = point
    self.normal = normal
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
