from src.glTypes import V3
from src.glModels import Material, Intersect
from src.glMath import cross, divide, dot, norm, substract, sum, mult, arccos, arctan2, PI

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

    u = 1 - ((arctan2(normal[2], normal[0]) / (2 * PI)) + 0.5)
    v = arccos(-normal[1]) / PI
    uvs = (u,v)
    return Intersect(distance=t0, point=hit, normal=normal, textCoords=uvs, sceneObject=self)

class Plane(object):
  def __init__(self, position, normal, material = Material()):
    self.position = position
    self.normal = normal
    self.material = material
  
  def ray_intersect(self, origin, direction):
    denom = dot(self.normal, direction)
    if abs(denom) > 1e-6: #0.0001
      num = dot(substract(self.position, origin), self.normal)
      t = num / denom
      if t > 0:
        hit = sum(origin, mult(direction, t))
        return Intersect(distance=t, point=hit, normal=self.normal, textCoords=None, sceneObject=self)
    return None

class AABB(object):
  def __init__(self, position, size, material = Material()):
    self.position = position
    self.size = size
    self.material = material
    self.planes = []
    self.boundsMin = [0,0,0]
    self.boundsMax = [0,0,0]
    halfSixeX = size[0] / 2
    halfSixeY = size[1] / 2
    halfSixeZ = size[2] / 2
    self.planes.append(Plane(sum(position, V3(halfSixeX,0,0)), V3(1,0,0), material))
    self.planes.append(Plane(sum(position, V3(-halfSixeX,0,0)), V3(-1,0,0), material))
    self.planes.append(Plane(sum(position, V3(0,halfSixeY,0)), V3(0,1,0), material))
    self.planes.append(Plane(sum(position, V3(0,-halfSixeY,0)), V3(0,-1,0), material))
    self.planes.append(Plane(sum(position, V3(0,0,halfSixeZ)), V3(0,0,1), material))
    self.planes.append(Plane(sum(position, V3(0,0,-halfSixeZ)), V3(0,0,-1), material))

    # Bounds
    epsilon = 1e-6 # 0.001
    for i in range(3):
      self.boundsMin[i] = position[i] - (epsilon + size[i] / 2)
      self.boundsMax[i] = position[i] + (epsilon + size[i] / 2)

  def ray_intersect(self, origin, direction):
    intersect = None
    t = float('inf')
    uvs = None
    for plane in self.planes:
      planeIntersect = plane.ray_intersect(origin, direction)
      if planeIntersect:
        if planeIntersect.point[0] >= self.boundsMin[0] and planeIntersect.point[0] <= self.boundsMax[0]:
          if planeIntersect.point[1] >= self.boundsMin[1] and planeIntersect.point[1] <= self.boundsMax[1]:
            if planeIntersect.point[2] >= self.boundsMin[2] and planeIntersect.point[2] <= self.boundsMax[2]:
              if planeIntersect.distance < t:
                t = planeIntersect.distance
                intersect = planeIntersect
                u, v = 0, 0
                if abs(plane.normal[0]) > 0:
                  # Map for X axis using Y and Z coords
                  u = (planeIntersect.point[1] - self.boundsMin[1]) / (self.boundsMax[1] - self.boundsMin[1])
                  v = (planeIntersect.point[2] - self.boundsMin[2]) / (self.boundsMax[2] - self.boundsMin[2])
                elif abs(plane.normal[1]) > 0:
                  # Map for Y axis using X and Z coords
                  u = (planeIntersect.point[0] - self.boundsMin[0]) / (self.boundsMax[0] - self.boundsMin[0])
                  v = (planeIntersect.point[2] - self.boundsMin[2]) / (self.boundsMax[2] - self.boundsMin[2])
                elif abs(plane.normal[2]) > 0:
                  # Map for Z axis using X and Y coords
                  u = (planeIntersect.point[0] - self.boundsMin[0]) / (self.boundsMax[0] - self.boundsMin[0])
                  v = (planeIntersect.point[1] - self.boundsMin[1]) / (self.boundsMax[1] - self.boundsMin[1])
                uvs = (u, v)

    if intersect is None:
      return None

    return Intersect(distance = intersect.distance, point = intersect.point, normal = intersect.normal, textCoords=uvs, sceneObject = self)

class Triangle(object):
  def __init__(self, v0, v1, v2, material = Material()):
    self.v0 = v0
    self.v1 = v1
    self.v2 = v2
    self.material = material

  def ray_intersect(self, origin, direction):
    e1 = substract(self.v1, self.v0)
    e2 = substract(self.v2, self.v0)
    N = cross(e1, e2)

    NdotRayDirection = dot(N, direction)
    if abs(NdotRayDirection) < 1e-6:
      return None # ray is parallel to triangle plane

    D = dot(N, self.v0)
    t = (dot(N, origin) + D) / NdotRayDirection

    if t < 0:
      return None # Intersection is behind origin

    P = sum(origin, mult(direction, t))

    edge0 = substract(self.v1, self.v0)
    vp0 = substract(P, self.v0)
    C = cross(edge0, vp0)
    if dot(N, C) < 0:
      return None # P is on the right side

    edge1 = substract(self.v2, self.v1)
    vp1 = substract(P, self.v1)
    C = cross(edge1, vp1)
    if dot(N, C) < 0:
      return None # P is on the right side

    edge2 = substract(self.v0, self.v2)
    vp2 = substract(P, self.v2)
    C = cross(edge2, vp2)
    if dot(N, C) < 0:
      return None # P is on the right side

    return Intersect(distance = t, point = P, normal = N, textCoords=None, sceneObject = self)