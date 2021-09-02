import struct
from collections import namedtuple

def char(c):
  # 1 byte
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  # 2 bytes
  return struct.pack('=h', w)

def dword(d):
  # 4 bytes
  return struct.pack('=l', d)

def newColor(r, g, b):
  # values from 0 to 1
  return bytes([ int(b*255), int(g*255), int(r*255) ])

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])
