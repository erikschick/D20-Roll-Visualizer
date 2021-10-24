from collections import defaultdict
from typing import Callable
import os

def _in_replit_env():
  """ Looks for replit.com envvars """
  return len([k for k in os.environ.keys() if 'REPL_' in k]) > 0

TERMINAL_WIDTH = None  # Default to something quite narrow
def set_terminal_width(width):
  # replit doesn't know how wide its terminal is
  global TERMINAL_WIDTH
  TERMINAL_WIDTH = width

def get_terminal_width():
  global TERMINAL_WIDTH
  if TERMINAL_WIDTH is None:
    if _in_replit_env():
      print("\nFATAL\nYou must set the terminal width with set_terminal_width(...) when using replit")
      exit(1)
    set_terminal_width(os.get_terminal_size().columns)
  return TERMINAL_WIDTH


class RollProbabilities(dict):
  def __init__(self, *args, **kwargs):
    """
    It's just a fancy roll_value->probabilities dict with a few convenience features
    """
    self.update(*args, **kwargs)
    
    for key in self.keys():
      assert isinstance(key, int), "{} is not an int".format(key)

  def __setitem__(self, key: int, val: float):
    assert isinstance(key, int)
    dict.__setitem__(self, key, val)

  def __add__(self, modifier: int):
    if isinstance(modifier, RollProbabilities):
      raise NotImplementedError("Adding probabilities together is TODO")
    assert isinstance(modifier, int)
    return self._alter_damage(lambda d: d + modifier)

  def __radd__(self, modifier: int):
    return self + modifier

  def __sub__(self, modifier: int):
    return self + (-1 * modifier)

  def __rsub__(self, modifier: int):
    return self - modifier

  def __mul__(self, multiplier: int):
    if isinstance(multiplier, RollProbabilities):
      raise NotImplementedError("Multiplying probabilities together is TODO")
    assert isinstance(multiplier, int)
    if multiplier != 2:
      raise NotImplementedError("The only multiplier currently implemented is 2")

    # Naively and exhaustively compute probabilities.
    # This can certainly be better but it's all I need today
    res = defaultdict(int)
    for v1, c1 in self.items():
      for v2, c2 in self.items():
        res[v1 + v2] += c1 * c2
    res = RollProbabilities(res)

    # Scale down probabilities so they sum to 100%
    scale = 1. / sum(res.values())
    scaled_res = res._alter_chances(lambda c: c * scale)
    assert round(sum(scaled_res.values()), ndigits=10) == 1.0 
    return scaled_res
  
  def __rmul__(self, multiplier: int):
    return self * multiplier

  def __str__(self) -> str:
    """
    Gives a multi-line display of the given damanges->probability map
    """
    start = "{:<3} :  {:<"
    end = "} ({:0.1f}%)"
    display_max_bars = get_terminal_width() - len(start) - len(end)
    fstring = start + str(display_max_bars) + end
    max_prob = 100. * max(self.values())
    display_scale = display_max_bars / max_prob

    lines = []
    for val, prob in sorted(self.items()):
      percent = 100. * prob
      num_bars = round(percent * display_scale)
      lines.append(fstring.format(val, '|'*num_bars, percent))
    
    return "\n".join(lines)

  def average(self) -> float:
    running_total = 0
    for val, prob in self.items():
      running_total += val * prob
    return round(running_total, ndigits=2)

  def _alter_damage(self, alter_func: Callable[[int], None]):
    """
    Returns a new RollProbabilities with alter_func applied to each damage
    """
    return RollProbabilities({
      int(alter_func(val)): chance
      for val, chance in self.items()
    })

  def _alter_chances(self, alter_func: Callable[[int], None]):
    """
    Returns a new RollProbabilities with alter_func applied to each chance
    """
    return RollProbabilities({
      val: alter_func(chance)
      for val, chance in self.items()
    })


def d(die: int) -> RollProbabilities:
  """
  A roll of a given die
  e.g. d(20) is 1d20
  """
  side_chance = 1. / die

  return RollProbabilities({
      val: side_chance
      for val in range(1, die + 1)
    })


def _DC_odds(dps: RollProbabilities, DC: int) -> RollProbabilities:
  """
  Returns the ratio [0, 1] of the odds that the given probabilities will match or beat the given DC
  """
  passes = 0.
  fails = 0.
  for val, prob in dps.items():
    if val >= DC:
      passes += prob
    else:
      # For sanity-check assert
      fails += prob
  
  assert 1. - (passes + fails) < 0.001, (passes + fails)
  return round(passes, ndigits=10)


def _conditional_damage(apply_damage_chance: float, dp: RollProbabilities) -> RollProbabilities:
  """
  Adjust chances to reflect misses, and add the probability of a miss
  """
  assert 0. <= apply_damage_chance <= 1.
  res = dp._alter_chances(lambda c: c * apply_damage_chance)
  res[0] = 1. - apply_damage_chance
  return res

def against_AC(hit_roll: RollProbabilities, AC: int, dp: RollProbabilities) -> RollProbabilities:
  """
  Returns damage probabilities given hit probabilities and AC
  """
  return _conditional_damage(
    _DC_odds(hit_roll, AC),
    dp
  )

def target_save_all(save_roll: RollProbabilities, DC: int, dp: RollProbabilities) -> RollProbabilities:
  """
  Returns damage probabilities given save probabilities and save DC
  """
  return _conditional_damage(
    1. - _DC_odds(save_roll, DC),
    dp
  )

def _print_distribution(rp: RollProbabilities):
  print("___ Exactly ___")

  print(rp)

def _print_cumulative(rp: RollProbabilities):
  print("___ At least ___")

  cumulative_counts = defaultdict(float)
  sorted_damage = sorted(set(rp.keys()) - {0})
  for val, prob in sorted(rp.items()):
    for damage in sorted_damage:
      if damage <= val:
        cumulative_counts[damage] += prob
  cumulative_counts = RollProbabilities(cumulative_counts)
  cumulative_counts[0] = rp[0]

  print(cumulative_counts)

def print_stats(rp: RollProbabilities, title: str=""):
  """
  Prints exact and inverse-cumulative distributions for the given roll
  """
  header = "_____{}______".format(title)
  divider = "_" * len(header)
  print(divider)
  print(header)
  print(divider)
  print("Average: {}\n".format(rp.average()))
  _print_distribution(rp)
  print()
  _print_cumulative(rp)
  print(divider)
  print("\n"*2)
