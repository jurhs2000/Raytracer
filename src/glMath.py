from src.glTypes import V3
from math import pi, tan

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

def sum(x, y):
  return V3(x.x + y.x, x.y + y.y, x.z + y.z)

def top(fov, n):
  return tan((fov * pi / 180) / 2) * n

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
