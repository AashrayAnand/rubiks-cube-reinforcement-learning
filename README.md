# Reinforcement Learning: Solving the Rubiks Cube

## The Rubiks cube is a famous thought problem, and a unique thought experiment in the realm of artificial intelligence

### This project is an attempt to represent and solve the classic rubiks cube, with a few constraints for the sake of simplicity ###

### To solve the problem of a rubiks cube, we implemented feature-based Q-Learning, a powerful reinforcement learning technique, as well as the utilization of a pattern database, to quantify the quality of near-finished cubes

this project assumes that a rubiks cube can *only execute 180 degree side turns*, which greatly reduces the *branching factor* of the cube's *state space tree*

this project also attempts to reach a solution for a solved cube which has had *n random moves executed on it*, this value n
currently can be up to 5 to find a goal state for each execution, or in the range of 6-10 to be somewhat successful

**puzzle.py** includes the state representation of a Rubiks Cube, **State()**, as well as a few auxillary functions
that are used elsewhere in the application
**tests.py** includes a variety of test cases that can be executed to confirm the valid implementation of the cube's state represention
**Agent.py** includes the QLear