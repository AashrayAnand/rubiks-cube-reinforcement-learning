# Reinforcement Learning: Solving the Rubik's Cube

## The Rubik's cube is a famous logic puzzle, and a unique thought experiment in the realm of artificial intelligence

 This project is an attempt to represent and solve the classic Rubik's cube

To solve the problem of a Rubik's cube, we implemented **feature-based Q-Learning**, a powerful reinforcement learning technique, as well as **the utilization of a pattern database**, to quantify the quality of near-finished cubes

this project assumes that a Rubik's cube can *only execute 180 degree side turns*, which greatly reduces the *branching factor* of the cube's *state space tree*

this project also attempts to reach a solution for a solved cube which has had *n random moves executed on it*, this value n
currently can be up to 5 to find a goal state for each execution, or in the range of 6-10 to be somewhat successful

**puzzle.py** includes the state representation of a Rubik's Cube, **State()**, as well as a few auxillary functions
that are used elsewhere in the application

**tests.py** includes a variety of test cases that can be executed to confirm the valid implementation of the cube's state represention

**Agent.py** includes the implementation of a reinforcement learning agent, which executes iterations of Q-Learning, and additionally uses a pattern database, to build up a Q-Table, which is used to eventually try to solve the given random Rubik's cube

###Using this project
> clone the repository
> verify you have python3 installed
> python Agent.py

###References:

McAleer, Stephen. *Solving the Rubik's Cube without Human Knowledge*. https://arxiv.org/pdf/1805.07470.pdf