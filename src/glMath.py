from src.glTypes import V3
from math import pi, tan, acos, atan2

PI = pi

def norm(x):
  xnorm = ((x.x**2) + (x.y**2) + (x.z**2))**(1/2)
  return xnorm

def divide(v3, d):
  if d != 0:
    divided = V3(v3.x / d, v3.y / d, v3.z / d)
    return divided
  else:
    print('division by zero')
    return V3(0, 0, 0)

def cross(a, b):
  axb = V3(a[1] * b[2] - a[2] * b[1],
         a[2] * b[0] - a[0] * b[2],
         a[0] * b[1] - a[1] * b[0])
  return axb

def substract(x, y):
  return V3(x.x - y.x, x.y - y.y, x.z - y.z)

def dot(x, y):
  xdy = (x.x * y.x) + (x.y * y.y) + (x.z * y.z)
  return xdy

def mult(v3, m):
  product = V3(v3.x * m, v3.y * m, v3.z * m)
  return product

def sum(x, y):
  return V3(x.x + y.x, x.y + y.y, x.z + y.z)

def negative(x):
  return V3(-x.x, -x.y, -x.z)

def top(fov):
  return tan((fov * pi / 180) / 2)

def linearMult(v1, v2):
  return [ v1[i] * v2[i] for i in range(len(v1)) ]

def matrixMult(matrixA, matrixB):
  product = [ [] for x in range(len(matrixA)) ]
  for i in range(len(matrixA)):
    for j in range(len(matrixA)):
      element = 0
      for n in range(len(matrixA)):
        element += matrixA[i][n] * matrixB[n][j]
      product[i].append(element)
  return product

def reflectVector(normal, dirVector):
  reflect = 2 * dot(normal, dirVector)
  reflect = mult(normal, reflect)
  reflect = substract(reflect, dirVector)
  reflect = divide(reflect, norm(reflect))
  return reflect

def refractVector(normal, direction, ior):
  # Snell's law
  cosi = max(-1, min(1, dot(direction, normal)))
  etai = 1
  etat = ior
  if cosi < 0:
    cosi = -cosi
  else:
    etai, etat = etat, etai
    normal = negative(normal)
  eta = etai / etat
  k = 1 - eta**2 * (1 - cosi**2)
  if k < 0: # total internal reflection
    return None
  R = sum(mult(direction, eta), mult(normal, eta * cosi - k**0.5))
  return divide(R, norm(R))

def fresnel(normal, direction, ior):
  cosi = max(-1, min(1, dot(direction, normal)))
  etai = 1
  etat = ior

  if cosi > 0:
    etai, etat = etat, etai
    
  sint = etai / etat * (max(0, 1 - cosi**2) ** 0.5)

  if sint >= 1: # Total internal reflection
    return 1

  cost = max(0, 1 - sint**2) ** 0.5
  cosi = abs(cosi)
  Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
  Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))

  return (Rs * Rs + Rp * Rp) / 2

# determinant of matrix without numpy
# inspired by https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy
def inv(x):
  detX = det(x)
  cofactors = []
  for i in range(len(x)):
    cofactorRow = []
    for j in range(len(x)):
      minor = matrixMinor(x, i, j)
      cofactorRow.append(((-1)**(i + j)) * det(minor))
    cofactors.append(cofactorRow)
  cofactors = transpose(cofactors)
  for i in range(len(cofactors)):
    for j in range(len(cofactors)):
      cofactors[i][j] = cofactors[i][j] / detX
  return cofactors

def det(x):
  if len(x) == 2:
    return x[0][0] * x[1][1] - x[0][1] * x[1][0]
  else:
    determinant = 0
    for i in range(len(x)):
      determinant += ((-1)**i) * det(matrixMinor(x, 0, i)) * x[0][i]
    return determinant

def matrixMinor(matrix, i, j):
  return [row[:j] + row[j+1:] for row in (matrix[:i]+matrix[i+1:])]

def transpose(x):
  xt = [ [None]*len(x) for i in range(len(x[0])) ]
  for i in range(len(x[0])):
    for j in range(len(x)):
      xt[i][j] = x[j][i]
  return xt

def arccos(x):
  return acos(x)

def arctan2(x, y):
  return atan2(x, y)