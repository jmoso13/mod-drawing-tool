from .base_path import Path
import math
import numpy as np

class CirclePath(Path):
  def __init__(self, radius=1, center=(0,0), frames=60*15, rotations=1):
    start = 45
    deg_step = 360*rotations/frames
    pos = (radius*math.cos(math.radians(start - deg_step)) + center[0], radius*math.sin(math.radians(start - deg_step)) + center[1])
    pos1 = (radius*math.cos(math.radians(start)) + center[0], radius*math.sin(math.radians(start)) + center[1])
    direc = tuple(np.array(pos1) - np.array(pos))
    vel = 1.0
    super().__init__(pos=pos, direc=direc, vel=vel)
    self._radius = radius
    self._center = center
    self._frames = frames
    self._start_deg = start
    self._deg_step = deg_step

    # Will Change
    self._arc_length = math.radians(self._deg_step)*self._radius
    self._deg = start - deg_step
    self._r = radius
    self._c = center
    self._d_s = deg_step

  @property
  def deg(self):
    return self._deg
  
  @deg.setter
  def deg(self, value):
    self._deg = value

  @property
  def rad(self):
    return self._r

  @rad.setter
  def rad(self, value):
    self._r = value
    self._post_rad_set()

  @property
  def cen(self):
    return self._c

  @cen.setter
  def cen(self, value):
    self._c = value
    self._post_cen_set()
  
  @property
  def deg_step(self):
    return self._d_s

  @deg_step.setter
  def deg_step(self, value):
    self._d_s = value
    self._post_deg_step_set()
  
  def _post_pos_set(self):
    self.cen = (self.pos[0] - self.rad*math.cos(math.radians(self.deg)), self.pos[1] - self.rad*math.sin(math.radians(self.deg)))

  def _post_rad_set(self):
    self.deg_step = math.degrees(self._arc_length/self.rad)

  def _post_cen_set(self):
    self.deg = math.degrees(math.atan2(self.pos[1] - self.cen[1], self.pos[0] - self.cen[0]))
    self.rad = math.sqrt(math.pow(self.pos[0] - self.cen[0], 2) + math.pow(self.pos[1] - self.cen[1], 2))

  def _post_deg_step_set(self):
    self._arc_length = math.radians(self.deg_step)*self.rad

  def _initialize_path(self):
    self._i = 0
    # Will Change
    self.deg = self._start_deg - self._deg_step
    self.rad = self._radius
    self.cen = self._center
    self.deg_step = self._deg_step

  def __next__(self):
    if self._i < self._frames:
      self.pos = tuple(np.array(self.pos) + np.array(self.direc)*self.vel)
      pos1 = (self.rad*math.cos(math.radians(self.deg + self.deg_step)) + self.cen[0], self.rad*math.sin(math.radians(self.deg + self.deg_step)) + self.cen[1])
      self.direc = tuple(np.array(pos1) - np.array(self.pos))
      self.deg = self.deg + self.deg_step
      self._i = self._i + 1
      return self.pos
    else:
      raise StopIteration


class LinePath(Path):
  def __init__(self, start, stop, frames):
    direc = tuple((np.array(stop) - np.array(start))/frames)
    pos = np.array(start) - np.array(direc)
    vel = 1.0
    super().__init__(pos=pos, direc=direc, vel=vel)
    self._start = start
    self._stop = stop
    self._frames = frames
    self._i = 0

  def _post_pos_set(self):
    self.direc = tuple((np.array(self._stop) - np.array(self.pos))/(self._frames-self._i))

  def _initialize_path(self):
    self._i = 0

  def __next__(self):
    if self._i < self._frames:
      self._i = self._i + 1 
      self.pos = tuple(np.array(self.pos) + np.array(self.direc)*self.vel)
      return self.pos
    else:
      raise StopIteration 