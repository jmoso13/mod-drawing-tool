from abc import ABC, abstractmethod

class Path(ABC):
  def __init__(self, pos=(0,0), direc=(1,1), vel=1.0):
    self._pos = pos
    self._dir = direc
    self._vel = vel

    # Values we will change
    self._p = pos
    self._d = direc
    self._v = vel

  @property
  def init_pos(self):
    return self._pos

  @property
  def init_dir(self):
    return self._dir

  @property
  def init_vel(self):
    return self._vel

  @property
  def pos(self):
    return self._p

  @pos.setter
  def pos(self, value):
    self._p = value
    self._post_pos_set()

  @property
  def direc(self):
    return self._d

  @direc.setter
  def direc(self, value):
    self._d = value
    self._post_direc_set()

  @property
  def vel(self):
    return self._v

  @vel.setter
  def vel(self, value):
    self._v = value
    self._post_vel_set()

  def _post_pos_set(self):
    pass
  
  def _post_direc_set(self):
    pass
  
  def _post_vel_set(self):
    pass

  @abstractmethod
  def _initialize_path(self):
    pass

  @abstractmethod
  def __next__(self):
    return None

  def __iter__(self):
    self.pos = self._pos
    self.direc = self._dir
    self.vel = self._vel
    self._initialize_path()
    return self

  
  
  
  