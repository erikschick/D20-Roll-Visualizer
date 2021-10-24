from functions import d, print_stats, _conditional_damage, against_AC, target_save_all, _DC_odds


"""
These are quite simplistic at the moment, but they get the job done.
"""


def prob_testcase(name, trial, expected):
  passed = True
  for val, prob in expected.items():
    if val not in trial or (trial[val] - (prob / 100.) > 0.001):
      passed = False
      break

  if len(expected) == 0:
    passed = False
  
  if not passed:
    print("Test {} FAILED! Expected:\n{}\nGot:".format(name, expected))
    print_stats(trial)

def DC_testcase(name, trial, expected):
  if trial != expected:
    print("Test {} FAILED!\n\tExpected {} got {}".format(name, expected, trial))




def run_tests():
  print("--- STARTING TESTS ---")

  """
  PROBABILITY TESTCASES
  """
  prob_testcase(
    "1d4",
    d(4),
    {1: 25, 2: 25, 3: 25, 4: 25}
  )
  prob_testcase(
    "1d4 + 3",
    d(4) + 3,
    {4: 25, 5: 25, 6: 25, 7: 25}
  )
  prob_testcase(
    "2d4",
    2 * d(4),
    {2: 6.2, 5: 25, 8: 6.2}
  )
  prob_testcase(
    "2x (1d4 + 3)",
    2 * (d(4) + 3),
    {8: 6.2, 11: 25}
  )
  prob_testcase(
    "50% chance for 1d4 damage",
    _conditional_damage(0.5, d(4)),
    {0: 50, 1: 12.5, 2: 12.5, 3: 12.5, 4: 12.5}
  )
  prob_testcase(
    "70% chance for 1d4 damage",
    _conditional_damage(0.7, d(4)),
    {0: 30, 1: 17.5, 2: 17.5, 3: 17.5, 4: 17.5}
  )
  prob_testcase(
    "1d20 against AC 15 for 1d4 damage",
    against_AC(d(20), 15, d(4)),
    {0: 70, 1: 7.5, 2: 7.5, 3: 7.5, 4: 7.5}
  )
  prob_testcase(
    "1d4 damage with 1d20 target save all against DC 15",
    target_save_all(d(20), 15, d(4)),
    {0: 30, 1: 17.5, 2: 17.5, 3: 17.5, 4: 17.5}
  )


  """
  DC TESTCASES
  """
  DC_testcase(
    "1d20 against DC 11",
    _DC_odds(d(20), 11),
    0.5
  )
  DC_testcase(
    "1d20+2 against DC 13",
    _DC_odds(d(20) + 2, 13),
    0.5
  )
  DC_testcase(
    "1d20-2 against DC 9",
    _DC_odds(d(20) - 2, 9),
    0.5
  )
  DC_testcase(
    "1d20 against DC 15",
    _DC_odds(d(20), 15),
    0.3
  )
  DC_testcase(
    "1d20-2 against DC 13",
    _DC_odds(d(20) - 2, 13),
    0.3
  )

  """
  RANDOM OTHER TESTCASES
  """
  def assert_equal(test_name, trial, expected):
    if trial != expected:
      print("Test {} failed! Expected {} got {}.".format(test_name, expected, trial))
  assert_equal("Simple average", d(20).average(), 10.5)
  assert_equal("Catan average", (2 * d(6)).average(), 7)

  print("--- TESTS COMPLETE ---")