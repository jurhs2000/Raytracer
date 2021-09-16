from src.glModels import Material, Intersect
from src.glMath import divide, dot, norm, substract, sum, mult

class Sphere(object):
  def __init__(self, center, radius, material = Material()):
    self.center = center
    self.radius = radius
    self.material = material
  
  def ray_intersect(self, origin, direction):
    L = substract(self.center, origin)
    tca = dot(L, direction)
    l = norm(L)
    d = (l**2 - tca**2)
    if d > self.radius ** 2:
      return None

    #Sphere behind de camera
    thc = (self.radius**2 - d) ** 0.5
    t0 = tca - thc
    t1 = tca + thc
    if t0 < 0:
      t0 = t1
    if t0 < 0:
      return None

    #intersection P = O + t * d
    hit = sum(origin, mult(direction, t0))
    normal = substract(hit, self.center)
    normal = divide(normal, norm(normal))
    return Intersect(distance=t0, point=hit, normal=normal, sceneObject=self)
