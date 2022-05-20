import math
import numpy as np

def vec_add(x1,x2):
  return tuple(np.array(x1) + np.array(x2))

def val_add(x1,x2):
  return math.fsum([x1, x2])

def vec_x_add(x1,x2):
  vec_x = (x2[0],0)
  return tuple(np.array(x1) + np.array(vec_x))

def vec_y_add(x1,x2):
  vec_x = (0,x2[1])
  return tuple(np.array(x1) + np.array(vec_x))

def val_x_add(x1,x2):
  return (math.fsum([x1[0],x2]), x1[1])

def val_y_add(x1,x2):
  return (x1[0], math.fsum([x1[1],x2]))

def vec_mult(x1,x2):
  return tuple(np.multiply(np.array(x1), np.array(x2)))

def val_mult(x1,x2):
  return x1*x2

def vec_avg(x1,x2):
  return tuple((np.array(x1) + np.array(x2))/2.)

def val_avg(x1, x2):
  return (x1+x2)/2.

def val_replace(x1,x2):
  if x2 is not None:
    return x2
  else:
    return x1

def vec_replace(x1,x2):
  if x2 is not None:
    return x2
  else:
    return x1