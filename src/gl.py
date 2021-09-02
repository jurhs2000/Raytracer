# Graphics Library

from src.glTypes import V3, dword, newColor, word
from src.glMath import divide, cross, inv, norm, substract, top

BLACK = newColor(0, 0, 0)
WHITE = newColor(1, 1, 1)

class Raytracer(object):
  # Constructor
  def __init__(self, width, height):
    self.curr_color = WHITE
    self.clear_color = BLACK
    self.glLookAt(V3(0,0,0), V3(0,0,-10))
    self.glCreateWindow(width, height)
    self.camPosition = V3(0,0,0)
    self.fov = 60
    self.background = None
    self.scene = []

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

  def glLookAt(self, eye, camPosition = V3(0,0,0), worldUp=V3(0,1,0)):
    forward = substract(camPosition, eye)
    forward = divide(forward, norm(forward))

    right = cross(worldUp, forward)
    right = divide(right, norm(right))

    up = cross(forward, right)
    up = divide(up, norm(up))

    self.camMatrix = [[right[0],up[0],forward[0],camPosition.x],
                      [right[1],up[1],forward[1],camPosition.y],
                      [right[2],up[2],forward[2],camPosition.z],
                      [0,0,0,1]]

    self.viewMatrix = inv(self.camMatrix)

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
        t = top(self.fov, 2)
        r = t * self.width / self.height
        Px *= r
        Py *= t
        direction = V3(Px, Py, -1) # Camera always sees to -Z
        direction = divide(direction, norm(direction))
        self.glPoint(x, y, self.castRay(self.camPosition, direction))

  def castRay(self, origin, direction):
    material = self.sceneIntersect(origin, direction)
    if material == None:
      return self.clear_color
    else:
      return material.diffuse

  def sceneIntersect(self, origin, direction):
    depth = float('inf')
    material = None
    for obj in self.scene:
      intersect = obj.ray_intersect(origin, direction)
      if intersect != None:
        if intersect.distance < depth:
          depth = intersect.distance
          material = obj.material
    return material

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
