# Graphics Library

from src.glTypes import V3, dword, newColor, word
from src.glMath import divide, dot, linearMult, negative, norm, reflectVector, substract, top

BLACK = newColor(0, 0, 0)
WHITE = newColor(1, 1, 1)

class Raytracer(object):
  # Constructor
  def __init__(self, width, height):
    self.curr_color = WHITE
    self.clear_color = BLACK
    self.glCreateWindow(width, height)
    self.camPosition = V3(0,0,0)
    self.fov = 60
    self.background = None
    self.scene = []
    self.pointLights = []
    self.ambientLight = None
    self.directionalLight = None

  def glCreateWindow(self, width, height):
    self.width = width
    self.height = height
    self.glClear()
    self.glViewPort(0, 0, width, height)

  def glViewPort(self, x, y, width, height):
    self.vpX = int(x) if x <= self.width else Exception('x is outside the window')
    self.vpY = int(y) if y <= self.height else Exception('y is outside the window')
    self.vpWidth = (width) if x + width <= self.width else Exception('viewport is outside the window')
    self.vpHeight = (height) if y + height <= self.height else Exception('viewport is outside the window')
    self.vpWidthMax = self.vpX + self.vpWidth
    self.vpHeightMax = self.vpY + self.vpHeight

  def glViewPortClear(self, color = None):
    for x in range(self.vpX, self.vpX + self.vpWidth):
      for y in range(self.vpY, self.vpY + self.vpHeight):
        self.glPoint(x, y, color)

  def glClearColor(self, r, g, b):
    self.clear_color = newColor(r, g, b)

  def glClear(self):
    # Creates a 2D pixels list and assigns a 3 bytes color for each value
    self.pixels = [ [self.clear_color for y in range(self.height)] for x in range(self.width) ]

  def glClearBackground(self):
    if self.background:
      for x in range(self.vpX, self.vpX + self.vpWidth):
        for y in range(self.vpY, self.vpY + self.vpHeight):
          tx = (x - self.vpX) / self.vpWidth
          ty = (y - self.vpY) / self.vpHeight
          self.glPoint(x,y, self.background.getColor(tx, ty))

  def glColor(self, r, g, b):
    self.curr_color = newColor(r, g, b)

  def glPoint(self, x, y, color = None):
    # if the point is not in the viewport, don't draw it
    if (x < self.vpX) or (x >= self.vpWidthMax) or (y < self.vpY) or (y >= self.vpHeightMax):
      return
    
    if (0 <= x < self.width) and (0 <= y < self.height):
      self.pixels[int(x)][int(y)] = color or self.curr_color

  def glRender(self):
    for y in range(self.height):
      for x in range(self.width):
        # Transform window coords to NDC coords (-1 to 1)
        Px = 2 * (x + 0.5) / self.width - 1
        Py = 2 * (y + 0.5) / self.height - 1
        # vision angle, assuming that near plane is 1 unit from camera
        t = top(self.fov)
        r = t * self.width / self.height
        Px *= r
        Py *= t
        direction = V3(Px, Py, -1) # Camera always sees to -Z
        direction = divide(direction, norm(direction))
        self.glPoint(x, y, self.castRay(self.camPosition, direction))

  def castRay(self, origin, direction):
    intersect = self.sceneIntersect(origin, direction)
    if intersect == None:
      return self.clear_color

    material = intersect.sceneObject.material
    objectColor = [material.diffuse[2] / 255,
                  material.diffuse[1] / 255,
                  material.diffuse[0] / 255]
    pLightColor = [0,0,0]
    ambientColor = [0,0,0]
    dirLightColor = [0,0,0]

    # View direction
    viewDir = substract(self.camPosition, intersect.point)
    viewDir = divide(viewDir, norm(viewDir))

    if self.ambientLight:
      ambientColor = [self.ambientLight.strength * self.ambientLight.color[2] / 255,
                      self.ambientLight.strength * self.ambientLight.color[1] / 255,
                      self.ambientLight.strength * self.ambientLight.color[0] / 255]

    if self.directionalLight:
      diffuseColor = [0,0,0]
      specColor = [0,0,0]
      lightDir = negative(self.directionalLight.direction)
      intensity = max(0, dot(intersect.normal, lightDir)) * self.directionalLight.intensity
      diffuseColor = [intensity * self.directionalLight.color[2] / 255,
                      intensity * self.directionalLight.color[1] / 255,
                      intensity * self.directionalLight.color[0] / 255]
      # reflected light direction
      reflect = reflectVector(intersect.normal, lightDir)
      specIntensity = self.directionalLight.intensity * max(0, dot(viewDir, reflect)) ** material.specularity
      specColor = [specIntensity * self.directionalLight.color[2] / 255,
                  specIntensity * self.directionalLight.color[1] / 255,
                  specIntensity * self.directionalLight.color[0] / 255]
      dirLightColor = [diffuseColor[0] + specColor[0],
                      diffuseColor[1] + specColor[1],
                      diffuseColor[2] + specColor[2]]

    for pointLight in self.pointLights:
      diffuseColor = [0,0,0]
      specColor = [0,0,0]
      lightDir = substract(pointLight.position, intersect.point)
      lightDir = divide(lightDir, norm(lightDir))
      intensity = max(0, dot(intersect.normal, lightDir)) * pointLight.intensity
      diffuseColor = [intensity * pointLight.color[2] / 255,
                     intensity * pointLight.color[1] / 255,
                     intensity * pointLight.color[0] / 255]
      # reflected light direction
      reflect = reflectVector(intersect.normal, lightDir)
      specIntensity = pointLight.intensity * max(0, dot(viewDir, reflect)) ** material.specularity
      specColor = [specIntensity * pointLight.color[2] / 255,
                  specIntensity * pointLight.color[1] / 255,
                  specIntensity * pointLight.color[0] / 255]
      pLightColor = [diffuseColor[0] + specColor[0] + pLightColor[0],
                    diffuseColor[1] + specColor[1] + pLightColor[1],
                    diffuseColor[2] + specColor[2] + pLightColor[2]]

    finalColor = [pLightColor[0] + ambientColor[0] + dirLightColor[0],
                  pLightColor[1] + ambientColor[1] + dirLightColor[1],
                  pLightColor[2] + ambientColor[2] + dirLightColor[2]]
    finalColor = linearMult(finalColor, objectColor)
    r = min(1, finalColor[0])
    g = min(1, finalColor[1])
    b = min(1, finalColor[2])
    return newColor(r, g, b)

  def sceneIntersect(self, origin, direction):
    depth = float('inf')
    intersect = None
    for obj in self.scene:
      hit = obj.ray_intersect(origin, direction)
      if hit != None:
        if hit.distance < depth:
          depth = hit.distance
          intersect = hit
    return intersect

  def glFinish(self, filename):
    # Creates a BMP file and fills it with the data inside self.pixels
    with open(filename, "wb") as file:
      # HEADER
      # Signature
      file.write(bytes('B'.encode('ascii')))
      file.write(bytes('M'.encode('ascii')))
      # FileSize in bytes
      file.write(dword(14 + 40 + (self.width * self.height * 3)))
      # Reserved
      file.write(dword(0)) # 0 = unused
      # DataOffset
      file.write(dword(14 + 40)) # from beginning of file to the beginning of bitmap data

      # INFO HEADER
      # Size
      file.write(dword(40)) # 40 = size of info header
      # Width
      file.write(dword(self.width))
      # Height
      file.write(dword(self.height))
      # Planes
      file.write(word(1)) # number of planes
      # Bits per pixel
      file.write(word(24)) # 24 = 24bit RGB. NumColors = 16M
      # Compression
      file.write(dword(0)) # 0 = BI_RGB no compression
      # ImageSize
      file.write(dword(self.width * self.height * 3))
      # XpixelsPerM
      file.write(dword(0))
      # YpixelsPerM
      file.write(dword(0))
      # Colors Used
      file.write(dword(0))
      # Important Colors
      file.write(dword(0)) # 0 = all

      # COLOR TABLE
      for y in range(self.height):
        for x in range(self.width):
          file.write(self.pixels[x][y])
