# Charges an OBJ file

from src.glTypes import newColor
from src.glMath import divide, norm, arccos, arctan2, pi
from PIL import Image

class Obj(object):
  def __init__(self, filename):
    with open(filename, "r") as f:
      self.lines = f.read().splitlines()

    self.vertices = []
    self.textcoords = []
    self.normals = []
    self.faces = []
    self.read()

  def read(self):
    for line in self.lines:
      if line:
        try:
          prefix, value = line.split(" ", 1)
        except:
          continue
        if prefix == "v": # Vertex
          self.vertices.append(list(map(float, value.split(" "))))
        elif prefix == "vt": # Text coordinate
          self.textcoords.append(list(map(float, value.split(" "))))
        elif prefix == "vn": # Normal vector
          self.normals.append(list(map(float, value.split(" "))))
        elif prefix == "f": # Face
          self.faces.append([ list(map(int, vertex.split("/"))) for vertex in value.split(" ") ])

# tested with jpg, png
class Texture(object):
  def __init__(self, filename):
    self.filename = filename
    self.read()

  def read(self):
    self.image = Image.open(self.filename)
    imagePixels = self.image.load()
    self.pixels = []
    for x in range(self.image.size[0]):
      self.pixels.append([])
      for y in range(self.image.size[1]):
        r = imagePixels[x,y][0] / 255
        g = imagePixels[x,y][1] / 255
        b = imagePixels[x,y][2] / 255
        self.pixels[x].append(newColor(r, g, b))

  def getColor(self, tx, ty):
    if 0 <= tx < 1 and 0 <= ty < 1:
      x = round((tx) * self.image.size[0])
      y = round((1-ty) * self.image.size[1])
      if x < self.image.size[0] and y < self.image.size[1]:
        return self.pixels[x][y]
    else:
      return newColor(0,0,0)

class EnvironmentMap(object):
  def __init__(self, filename, pos=0.5):
    self.filename = filename
    self.pos = pos
    self.read()

  def read(self):
    self.image = Image.open(self.filename)
    imagePixels = self.image.load()
    self.pixels = []
    for x in range(self.image.size[0]):
      self.pixels.append([])
      for y in range(self.image.size[1]):
        r = imagePixels[x,y][0] / 255
        g = imagePixels[x,y][1] / 255
        b = imagePixels[x,y][2] / 255
        self.pixels[x].append(newColor(r, g, b))

  def getColor(self, direction):
    direction = divide(direction, norm(direction))
    x = int(((arctan2(direction[2], direction[0]) / (2 * pi)) + self.pos) * self.image.size[0])
    y = int(arccos(direction[1]) / pi * self.image.size[1])
    if x < self.image.size[0] and y < self.image.size[1]:
      return self.pixels[x][y]
