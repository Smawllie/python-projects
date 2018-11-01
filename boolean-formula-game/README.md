# Boolean-formula-game
A game that two players can play to achieve the goal of outputting either true or false. This program showcases:
- Recursive implementation of a Tree ADT
- Utilization of helper functions
- Computer movement of O(2^n) time due to binary tree
- Rigorous testing through unit tests

To play the game download all three files except unittests.py, then run play_formula_game.py.
<br />
Formulas consist of the lowercase alphabet a-z (variables), * (or), + (and), and "-" (not). All formulas consisting of * or + must be enclosed in brackets. The goal for player E is to end with 1 and for player A to end with 0 <br />

How the shell will prompt you:

- Step 1: "Please enter formula:"
- Step 2: "Please enter order of variables to assign:"
- Step 3: "Please enter turns of players E and A:"
- Step 4 (repeat): "Player _ please enter value for variable a[0/1/C(omputer)]:" <br />

Example 1 of play:

- Step 1: "Please enter formula:" (a+b) [a OR b]
- Step 2: "Please enter order of variables to assign:" ab
- Step 3: "Please enter turns of players E and A:" EA
- Step 4: "Player E please enter value for variable a[0/1/C(omputer)]:" 1 [notice how E ensures this win this way]
- Step 4: "Player A please enter value for variable a[0/1/C(omputer)]:" 0
- "Player E wins!" <br />

Example 2 of play:

- Step 1: "Please enter formula:" (-(a+b)*a) [(not (a OR b)) AND a]
- Step 2: "Please enter order of variables to assign:" ab
- Step 3: "Please enter turns of players E and A:" AE
- Step 4: "Player A please enter value for variable a[0/1/C(omputer)]:" 1 [A ensures this win no matter what E does]
- Step 4: "Player E please enter value for variable a[0/1/C(omputer)]:" 0
- "Player A wins"
