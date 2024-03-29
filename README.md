# D20 Roll Visualizer

Author: Erik Schick

This is a quick weekend project because I was curious about the stats on a situation and existing online visualizers didn't seem to support everything I wanted to check.

______________________________________________________________

[Run it in replit.com](https://replit.com/@ErikSchick1/D20-Roll-Visualizer)

# How to enter a roll

`d(#)`  
The die to roll

`{roll} + #` or `{roll} - #`  
Add a static modifier to a roll

`# * {roll}`  
Multiple rolls  
*currently only supports 2x

`against_AC(hit_roll, AC, damage_roll)`  
Combine roll to hit against AC and roll for damage

`target_save_all(save_roll, DC, damage_roll)`  
Roll for damage with a chance for target to save against DC

# How to print a roll
`print_stats(roll, [title])`  
Prints the probability distribution, with optional title


# Examples
```python
print_stats(
  target_save_all(
    d(20) + 1,
    14,
    2 * d(12)
  ),
  title="2d12 damage on DC14 fail, target has a +1 to save"
)
```
```
____________________________________________________________
_____2d12 damage on DC14 fail, target has a +1 to save______
____________________________________________________________
Average: 7.8

___ Exactly ___
0   :  ||||||||||||||||||||||||||||||||||||||||||||||||||| (40.0%)
2   :  |                                                   (0.4%)
3   :  |                                                   (0.8%)
4   :  ||                                                  (1.2%)
5   :  ||                                                  (1.7%)
6   :  |||                                                 (2.1%)
7   :  |||                                                 (2.5%)
8   :  ||||                                                (2.9%)
9   :  ||||                                                (3.3%)
10  :  |||||                                               (3.8%)
11  :  |||||                                               (4.2%)
12  :  ||||||                                              (4.6%)
13  :  ||||||                                              (5.0%)
14  :  ||||||                                              (4.6%)
15  :  |||||                                               (4.2%)
16  :  |||||                                               (3.8%)
17  :  ||||                                                (3.3%)
18  :  ||||                                                (2.9%)
19  :  |||                                                 (2.5%)
20  :  |||                                                 (2.1%)
21  :  ||                                                  (1.7%)
22  :  ||                                                  (1.2%)
23  :  |                                                   (0.8%)
24  :  |                                                   (0.4%)

___ At least ___
0   :  ||||||||||||||||||||||||||||||||||                  (40.0%)
2   :  ||||||||||||||||||||||||||||||||||||||||||||||||||| (60.0%)
3   :  ||||||||||||||||||||||||||||||||||||||||||||||||||| (59.6%)
4   :  ||||||||||||||||||||||||||||||||||||||||||||||||||  (58.7%)
5   :  |||||||||||||||||||||||||||||||||||||||||||||||||   (57.5%)
6   :  |||||||||||||||||||||||||||||||||||||||||||||||     (55.8%)
7   :  ||||||||||||||||||||||||||||||||||||||||||||||      (53.7%)
8   :  ||||||||||||||||||||||||||||||||||||||||||||        (51.2%)
9   :  |||||||||||||||||||||||||||||||||||||||||           (48.3%)
10  :  ||||||||||||||||||||||||||||||||||||||              (45.0%)
11  :  |||||||||||||||||||||||||||||||||||                 (41.2%)
12  :  ||||||||||||||||||||||||||||||||                    (37.1%)
13  :  ||||||||||||||||||||||||||||                        (32.5%)
14  :  |||||||||||||||||||||||                             (27.5%)
15  :  |||||||||||||||||||                                 (22.9%)
16  :  ||||||||||||||||                                    (18.7%)
17  :  |||||||||||||                                       (15.0%)
18  :  ||||||||||                                          (11.7%)
19  :  |||||||                                             (8.7%)
20  :  |||||                                               (6.2%)
21  :  ||||                                                (4.2%)
22  :  ||                                                  (2.5%)
23  :  |                                                   (1.2%)
24  :                                                      (0.4%)
____________________________________________________________

```