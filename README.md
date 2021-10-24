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