import numpy as np
# DIREC
# Flip to backwards
# idk some way to connect asdrs to meaningful adds in direc

# POS
# Need to come up with some idea to get randomness involved
# Layer here on HOW to interpret, list of values to merge/replace? (could be useful for getting home)

# VEL
# Reasonably straightforward but def need a way to convert 0/1 of env to something that hovers to some extent around 1


# LISTENER -> Listen to audio -> choose some value based off listening (avg, max, sum)
# ==> Send To ==>
# INTERPRETER -> What to do with this number when sending to parameters and also how to merge

## MODIFIERS ##
# Listener
# LFO
# ENV (triggered by lfo or listener)
# Switch (kinda like a listener, triggered by anything, could be listening for a parameter - moving deg/cen when rotation is complete for far right white flag pattern)

## INTERPRETERS ##
# Customize for each parameter, different methods


## IDEAS FOR PATTERNS ##
# Use a circle to move cen parameter in a circle while drawing
# Use a circle to move pos or dir parameter in circle or line

class Listener:
  def __init__(self, source, sr=44100, fr=59.94):
    self.source = source
    self.sr = sr
    self.fr = fr
    self.spf = self.sr/self.fr

  def _initialize_listener(self):
    self._i = 0
    iter(self.source)

  def __iter__(self):
    self._initialize_listener()
    return self

  def __next__(self):
    b_start = int(self._i * self.spf)
    self._i += 1
    b_end = int((self._i) * self.spf)
    b_length = b_end - b_start
    return [next(self.source) for i in range(b_length)]


class SignalGenerator:
  def __init__(self, audio):
    self.audio = audio

  def __iter__(self):
    self.g = (s for s in self.audio)
    return self

  def __next__(self):
    return next(self.g)









