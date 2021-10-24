from functions import d, against_AC, target_save_all, print_stats, set_terminal_width

set_terminal_width(75)

##################################

ENEMY_AC = 20
ENEMY_WIS = -1

print_stats(
  target_save_all(
    d(20) + ENEMY_WIS,
    14,
    2 * d(12)
  ),
  title="Toll the Dead: 2d12 against target {} WIS".format(ENEMY_WIS)
)

print_stats(
  2 * (
    against_AC(
      d(20) + 4,
      19,
      d(6) +14
    )
  ),
  title="2x Sharpshooter against {} AC".format(ENEMY_AC)
)

print_stats(
  2 * (
    against_AC(
      d(20) +9,
      19,
      d(6) +4
    )
  ),
  title="2x Regular against {} AC".format(ENEMY_AC)
)






#######################################
from test import run_tests
run_tests()
