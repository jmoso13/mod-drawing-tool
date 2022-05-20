class ModulatedPath:
  def __init__(self, path, *modifiers):
    self.path = path
    self.modulators = tuple([m[0] for m in modifiers])
    self.receivers = tuple([m[1] for m in modifiers])
    self.patches = tuple([m[2] for m in modifiers])
    self._modifiers_count = len(modifiers)

  def __iter__(self):
    iter(self.path)
    [iter(modulator) for modulator in self.modulators]
    return self

  def append_modifier(self, modifier):
    mod, rec, patch = modifier
    iter(mod)
    self.modulators.append(mod)
    self.receivers.append(rec)
    self.patches.append(patch)
    self._modifiers_count += 1

  def _connect(self, mod_val, receiver, patch):
    if hasattr(self.path, patch):
      path_val = getattr(self.path, patch)
      new_val = receiver(path_val, mod_val)
      return new_val
    else:
      print(f"Path has no attribute {patch}, patch skipped")
      return None

  def _modulate(self, mod_vals, receivers, patches):
    assert len(mod_vals) == len(receivers) == len(patches)
    for i in range(len(mod_vals)):
      new_val = self._connect(mod_vals[i], receivers[i], patches[i])
      if new_val is not None:
        setattr(self.path, patches[i], new_val)

  def __next__(self):
    mod_vals = [next(modulator) for modulator in self.modulators]
    self._modulate(mod_vals, self.receivers, self.patches)
    return next(self.path)
      
