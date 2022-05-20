import numpy as np
import math


class SigmoidTranslator:
  def __init__(self, modifier):
    self.modifier = modifier

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    return 1./(1. + math.exp(-next(self.modifier)))


class BufferAverageTranslator:
  def __init__(self, modifier):
    self.modifier = modifier

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    return np.mean(np.array(next(self.modifier)))


class BufferMinTranslator:
  def __init__(self, modifier):
    self.modifier = modifier

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    return np.min(np.array(next(self.modifier)))


class BufferMaxTranslator:
  def __init__(self, modifier):
    self.modifier = modifier

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    return np.max(np.array(next(self.modifier)))


class BufferRangeTranslator:
  def __init__(self, modifier):
    self.modifier = modifier

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    n = np.array(next(self.modifier))
    return np.max(n) - np.min(n)


class AbsTranslator:
  def __init__(self, modifier):
    self.modifier = modifier

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    return np.abs(np.array(next(self.modifier)))


class LinearTranslator:
  def __init__(self, modifier, mn, mx, c=0, r=1):
    self.modifier = modifier
    self.range = mx-mn
    self.min = mn
    self.max = mx
    self.radius = self.range/2.
    self.center = self.min + self.radius
    self.c = c
    self.r = r
    
  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    return (np.array(next(self.modifier)) - self.center)/(self.range/self.r) + self.c


class TriggerTranslator:
  def __init__(self, modifier, threshold):
    self.modifier = modifier
    self.threshold = threshold

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    val = next(self.modifier)
    if val >= self.threshold:
      return 1
    else:
      return 0


class SwitchTranslator:
  def __init__(self, modifier, threshold):
    self.modifier = modifier
    self.threshold = threshold
    self.prev = 0

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    n = next(self.modifier)
    if self.prev < self.threshold and n >= self.threshold:
      self.prev = n
      return 1
    else:
      self.prev = n
      return 0


class PathTranslator:
  def __init__(self, path, attribute):
    self.path = path
    if hasattr(self.path, attribute):
      self.attribute = attribute
    else:
      print(f"{self.path} has no attribute {attribute}")
      raise Exception

  def __iter__(self):
    iter(self.path)
    return self

  def __next__(self):
    next(self.path)
    return getattr(self.path, self.attribute)


class EnvTranslator:
  def __init__(self, env, trigger):
    self.env = env
    self.trigger = trigger

  def __iter__(self):
    iter(self.env)
    iter(self.trigger)
    self._t = 0
    self._start = 0
    self._end = 1
    self._release = 0
    return self

  def __next__(self):
    self._t = next(self.trigger)
    if self._end:
      if self._t:
        self._start = 1
        self._end = 0
      else:
        return 0
    if self._start:
      if self._t:
        return next(self.env)
      else:
        self.env.trigger_release()
        self._release = 1
        self._start = 0
    if self._release:
      if self._t:
        self._start = 1
        self._release = 0
        self.env.stepper = self.env.get_ads_stepper()
        self.env.ended = False
        return next(self.env)
      else:
        if self.env.ended:
          self._release = 0
          self._end = 1
          iter(self.env)
          return 0
        else:
          return next(self.env)
    

class ChooseTranslator:
  def __init__(self, mod1, mod2, prob=0.5):
    self._mod1 = mod1
    self._mod2 = mod2
    self._prob = prob
    # Will Change
    self._p = self._prob

  @property
  def prob(self):
    return self._p

  @prob.setter
  def prob(self, value):
    self._p = value

  def __iter__(self):
    iter(self._mod1)
    iter(self._mod2)
    self.prob = self._prob
    return self

  def __next__(self):
    v1 = next(self._mod1)
    v2 = next(self._mod2)
    c = np.random.choice([0,1], p=[1-self.prob, self.prob])
    if c:
      return v1
    else:
      return v2


class Random2DTranslator:
  def __init__(self, modifier, s_modifier, point=(0,0), r=1):
    self.mx, self.my = point
    self.s = s_modifier
    self.r = r
    self.modifier = modifier
    self.val = point

  def __iter__(self):
    iter(self.modifier)
    iter(self.s)
    return self

  def __next__(self):
    val = next(self.modifier)
    s = next(self.s)
    if self.r is not None:
      if val == self.r:
        self.val = (np.random.normal(self.mx, s), np.random.normal(self.my, s))
      else:
        self.val = (self.mx, self.my)
    else:
      self.val = (np.random.normal(self.mx, s), np.random.normal(self.my, s))
    return self.val


class RemoveTranslator:
  def __init__(self, modifier, remove):
    self.modifier = modifier
    self.remove = remove

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    val = next(self.modifier)
    if val == self.remove:
      return None
    else:
      return val


class RemoveVecTranslator:
  def __init__(self, modifier, remove):
    self.modifier = modifier
    self.remove = remove

  def __iter__(self):
    iter(self.modifier)
    return self

  def __next__(self):
    val = next(self.modifier)
    if tuple(val) == tuple(self.remove):
      return None
    else:
      return val


class MultiplyTranslator:
  def __init__(self, mod1, mod2):
    self._mod1 = mod1
    self._mod2 = mod2

  def __iter__(self):
    iter(self._mod1)
    iter(self._mod2)
    return self

  def __next__(self):
    val1 = next(self._mod1)
    val2 = next(self._mod2)
    return np.multiply(val1, val2)


class AddTranslator:
  def __init__(self, mod1, mod2):
    self._mod1 = mod1
    self._mod2 = mod2

  def __iter__(self):
    iter(self._mod1)
    iter(self._mod2)
    return self

  def __next__(self):
    val1 = next(self._mod1)
    val2 = next(self._mod2)
    return np.add(val1, val2)


class CMultiplyTranslator:
  def __init__(self, mod1, c):
    self._mod1 = mod1
    self._c = c

  def __iter__(self):
    iter(self._mod1)
    return self

  def __next__(self):
    val1 = next(self._mod1)
    return np.multiply(val1, self._c)    