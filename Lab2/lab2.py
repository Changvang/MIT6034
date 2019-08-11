# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
   agenda = []
   agenda.append(list(start))
   if start == goal: # check if goal == start
    return start
   while not agenda == []:
      Parent = agenda.pop(0)
      ParentCopy = Parent[:]
      try:
        Children_F = graph.get_connected_nodes(ParentCopy.pop())
      except:
        print("Fail in list Parent ")
      Children_T = []
      for Child in Children_F:
        if(Child not in Parent):
          Children_T.append(Child)
      if Children_T == []:
        continue
      else:
        for Child in Children_T:
          New_Parent = Parent[:]
          New_Parent.append(Child)
          if (Child == goal):
            return ''.join(New_Parent)
          else:
            agenda.append(New_Parent)
   return agenda
   #graph.get_connected_nodes(node)



## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
   agenda = []
   agenda.append(list(start))
   if start == goal: # check if goal == start
    return start
   while not agenda == []:
      Parent = agenda.pop()
      ParentCopy = Parent[:]
      try:
        Children_F = graph.get_connected_nodes(ParentCopy.pop())
      except:
        print("Fail in list Parent ")
      Children_T = []
      for Child in Children_F:
        if(Child not in Parent):
          Children_T.append(Child)
      if Children_T == []:
        continue
      else:
        for Child in Children_T:
          New_Parent = Parent[:]
          New_Parent.append(Child)
          if (Child == goal):
            return ''.join(New_Parent)
          else:
            agenda.append(New_Parent)
   return agenda


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
  # a Fail in test 23 for Fail test Hill climbing
   agenda = []
   agenda.append(list(start))
   if start == goal: # check if goal == start
    return start
   #loop for finding Path
   count = 0
   while not agenda == [] :
      #print(agenda,count)
      count = count + 1
      if count > 100:
        break
      Parent = agenda.pop()
      ParentCopy = Parent[:]
      try:
        Children_F = graph.get_connected_nodes(ParentCopy.pop())
      except:
        break
      Children_T = []
      for Child in Children_F:
        if(Child not in Parent):
          Children_T.append(Child)
      if Children_T == []:
        continue
      else:
        #sort by heuristic 
        Children_N = [] # new list Children_N 
        for Child in Children_T:
          L = [Child, graph.get_heuristic(Child,goal)] # create List L[Node, Heristic of Node to Goal]
          Children_N.append(L) # append List to List
        Children_N = sorted(Children_N, key = lambda x:x[1], reverse = True) # sort List with value of hueristic from max to min
        Children_T = [Child[0] for Child in Children_N] # give Node for CHildren_T
        #Check path if T return else add new path and continue
        for Child in Children_T:
          New_Parent = Parent[:]
          New_Parent.append(Child)
          if (Child == goal):
            return New_Parent
          else:
            agenda.append(New_Parent)
   return agenda # you return a string of a part if the string not "ABC", I begin with "123" so you can controll the number

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
   agenda = []
   agenda.append(list(start))
   if start == goal: # check if goal == start
    return start
   while not agenda == []:
      agenda_1 = agenda[:]
      agenda_2 = []
      while agenda_1 != []:
        Parent = agenda_1.pop(0)
        ParentCopy = Parent[:]
        try:
          Children_F = graph.get_connected_nodes(ParentCopy.pop())
        except:
          print("Fail in list Parent ")
        Children_T = []
        for Child in Children_F:
          if(Child not in Parent):
            Children_T.append(Child)
        if Children_T == []:
          continue
        else:
          for Child in Children_T:
            New_Parent = Parent[:]
            New_Parent.append(Child)
            if (Child == goal):
              return New_Parent
            else:
              agenda_2.append(New_Parent)
      #now agenda_1 = [], agenda_2 have all path node for layyer n
      #we will sort agenda_2 by heuristic value of last node and add with <= beam_width to agenda
      #sort by heuristic 
      Children_N = [] # new list Children_N 
      for Child in agenda_2:
        L = [Child, graph.get_heuristic(Child[-1],goal)] # create List L[Node, Heristic of Node to Goal]
        Children_N.append(L) # append List to List
      Children_N = sorted(Children_N, key = lambda x:x[1]) # sort List with value of hueristic from min to max
      agenda_2 = [Child[0] for Child in Children_N] # give Node for CHildren_T
      if len(agenda_2) <= beam_width:
        agenda = agenda_2
      else:
        agenda = agenda_2[:beam_width]
   return agenda

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    LENGTH = 0
    #return 0 if length of path < 2
    if len(node_names) < 2:
    	return 0
    for i in range(len(node_names)-1):
    	if(node_names[i] == node_names[i+1]):
    		continue
    	else:
    		LENGTH = LENGTH + graph.get_edge(node_names[i], node_names[i+1]).length
    return LENGTH



def branch_and_bound(graph, start, goal):
   agenda = []
   agenda.append([list(start), path_length(graph,list(start))])
   if start == goal: # check if goal == start
    return start
   while not agenda == []:
      Parent = agenda.pop(0)[0]
      ParentCopy = Parent[:]
      try:
        Children_F = graph.get_connected_nodes(ParentCopy.pop())
      except:
        print("Fail in list Parent ")
      Children_T = []
      for Child in Children_F:
        if(Child not in Parent):
          Children_T.append(Child)
      if Children_T == []:
        continue
      else:
        for Child in Children_T:
          New_Parent = Parent[:]
          New_Parent.append(Child)
          if (Child == goal):
            return New_Parent
          else:
            agenda.append([New_Parent, path_length(graph,New_Parent)])
            agenda = sorted(agenda, key = lambda x:x[1])
   return agenda



def a_star(graph, start, goal):
   agenda = []
   agenda.append([list(start), path_length(graph,list(start))])
   ExList = [] #extended list for all past through nodes
   ExList.append(start)
   if start == goal: # check if goal == start
    return start
   while not agenda == []:
      Parent = agenda.pop(0)[0]
      ParentCopy = Parent[:]
      try:
        Children_F = graph.get_connected_nodes(ParentCopy.pop())
      except:
        print("Fail in list Parent ")
      Children_T = []
      for Child in Children_F:
        if(Child not in Parent and Child not in ExList):
          Children_T.append(Child)
          ExList.append(Child)
      if Children_T == []:
        continue
      else:
        for Child in Children_T:
          New_Parent = Parent[:]
          New_Parent.append(Child)
          if (Child == goal):
            return New_Parent
          else:
            agenda.append([New_Parent, path_length(graph,New_Parent) + graph.get_heuristic(New_Parent[-1],goal)])
            agenda = sorted(agenda, key = lambda x:x[1])
   return agenda


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
  for node in graph.nodes:
    if(graph.get_heuristic(node,goal) > path_length(graph,branch_and_bound(graph,node,goal))):
       return False
  return True

def is_consistent(graph, goal):
  for edge in graph.edges:
    if abs(graph.get_heuristic(edge.node1, goal) - graph.get_heuristic(edge.node2, goal)) > edge.length:
      return False
  return True


HOW_MANY_HOURS_THIS_PSET_TOOK = 'I dont know maybe two much'
WHAT_I_FOUND_INTERESTING = 'NOt found'
WHAT_I_FOUND_BORING = '++!'
