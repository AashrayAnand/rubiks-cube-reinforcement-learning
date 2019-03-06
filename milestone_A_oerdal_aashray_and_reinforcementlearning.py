#!/usr/bin/python3
'''Milestone_A_who_and_what.py
This runnable file will provide a representation of
answers to key questions about your project in CSE 415.

'''

# DO NOT EDIT THE BOILERPLATE PART OF THIS FILE HERE:

CATEGORIES=['Baroque Chess Agent','Feature-Based Reinforcement Learning for the Rubik Cube Puzzle',\
  'Hidden Markov Models: Algorithms and Applications']

class Partner():
  def __init__(self, lastname, firstname, uwnetid):
    self.uwnetid=uwnetid
    self.lastname=lastname
    self.firstname=firstname

  def __lt__(self, other):
    return (self.lastname+","+self.firstname).__lt__(other.lastname+","+other.firstname)

  def __str__(self):
    return self.lastname+", "+self.firstname+" ("+self.uwnetid+")"

class Who_and_what():
  def __init__(self, team, option, title, approach, workload_distribution, references):
    self.team=team
    self.option=option
    self.title=title
    self.approach = approach
    self.workload_distribution = workload_distribution
    self.references = references

  def report(self):
    rpt = 80*"#"+"\n"
    rpt += '''The Who and What for This Submission

Project in CSE 415, University of Washington, Winter, 2019
Milestone A

Team: 
'''
    team_sorted = sorted(self.team)
    # Note that the partner whose name comes first alphabetically
    # must do the turn-in.
    # The other partner(s) should NOT turn anything in.
    rpt += "    "+ str(team_sorted[0])+" (the partner who must turn in all files in Catalyst)\n"
    for p in team_sorted[1:]:
      rpt += "    "+str(p) + " (partner who should NOT turn anything in)\n\n"

    rpt += "Option: "+str(self.option)+"\n\n"
    rpt += "Title: "+self.title + "\n\n"
    rpt += "Approach: "+self.approach + "\n\n"
    rpt += "Workload Distribution: "+self.workload_distribution+"\n\n"
    rpt += "References: \n"
    for i in range(len(self.references)):
      rpt += "  Ref. "+str(i+1)+": "+self.references[i] + "\n"

    rpt += "\n\nThe information here indicates that the following file will need\n"+\
     "to be submitted (in addition to code and possible data files):\n"
    rpt += "    "+\
     {'1':"Baroque_Chess_Agent_Report",'2':"Rubik_Cube_Solver_Report",\
      '3':"Hidden_Markov_Models_Report"}\
        [self.option]+".pdf\n"

    rpt += "\n"+80*"#"+"\n"
    return rpt

# END OF BOILERPLATE.

# Change the following to represent your own information:

aashray = Partner("Anand", "Aashray", "aashray")
ozan = Partner("Erdal", "Ozan", "oerdal")
team = [aashray, ozan]

OPTION = '2'
# Legal options are 1, 2, and 3.

title = "A Complex Cube Crusher"

approach = '''Our approach will be to first go through Korf\'s optimal solutions paper.
  We will then spend the bulk of the initial time designing and implementing our state
  representation of the cube, using feature-based state representation to simplify
  this step. After this, we will primarily focus on the implementation of value iteration,
  while considering ways to optimize the Q-learning steps'''

workload_distribution = '''Ozan will have the primary priority of designing the state and
  state transformation functions for the game, while Aashray will be tasked with creating
  a client to display the state representation, and implementing the Q-learning stages. We
  will both work on the various optimizations we plan to add.'''

reference1 = '''Medium article on using reinforcement learning to solve various
  AI problems, including the Rubiks Cube, at: https://medium.com/datadriveninvestor/reinforcement-learning-to-solve-rubiks-cube-and-other-complex-problems-106424cf26ff'''

reference2 = '''""Solving the Rubik's cube without human knowledge" by Stephen McAleer
  https://arxiv.org/pdf/1805.07470.pdf'''

our_submission = Who_and_what([aashray, ozan], OPTION, title, approach, workload_distribution, [reference1, reference2])

# You can run this file from the command line by typing:
# python3 who_and_what.py

# Running this file by itself should produce a report that seems correct to you.
if __name__ == '__main__':
  print(our_submission.report())