from src.glMath import dot, norm, substract

class Intersect(object):
  def __init__(self, distance):
    self.distance = distance

class Sphere(object):
  def __init__(self, center, radius, material):
    self.center = center
    self.radius = radius
    self.material = material
  
  def ray_intersect(self, origin, direction):
    # P = O + t * d
    L = substract(self.center, origin)
    tca = dot(L, direction)
    l = norm(L)
    d = (l**2 - tca**2) ** 0.5
    if d > self.radius:
      return None

    #Sphere behind de camera
    thc = (self.radius**2 - d**2) ** 0.5
    t0 = tca - thc
    t1 = tca + thc
    if t0 < 0:
      t0 = t1
    if t0 < 0:
      return None

    return Intersect(distance=t0)