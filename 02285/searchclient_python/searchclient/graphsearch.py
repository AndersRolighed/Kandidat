import math
import memory
import time
import sys

from action import Action
from state import State
from frontier import Frontier

globals().update(Action.__members__)

start_time = time.perf_counter()

def search(initial_state : 'State', frontier : 'Frontier'):

    output_fixed_solution = False

    if output_fixed_solution:
        # Part 1: 
        # The agents will perform the sequence of actions returned by this method.
        # Try to solve a few levels by hand, enter the found solutions below, and run them:

        return [
            [MoveS],
            [MoveE],
            [MoveE],
            [MoveS],
        ]

    else:
        
        # Part 2:
        # Now try to implement the Graph-Search algorithm from R&N figure 3.7
        # In the case of "failure to find a solution" you should return None.
        # Some useful methods on the state class which you will need to use are:
        # state.is_goal_state() - Returns true if the state is a goal state.
        # state.extract_plan() - Returns the list of actions used to reach this state.
        # state.get_expanded_states() - Returns a list containing the states reachable from the current state.
        # You should also take a look at frontier.py to see which methods the Frontier interface exposes
        #
        # print_search_status(expanded, frontier): As you can see below, the code will print out status
        # (#expanded states, size of the frontier, #generated states, total time used) for every 1000th node
        # generated.
        # You should also make sure to print out these stats when a solution has been found, so you can keep
        # track of the exact total number of states generated!!
   

        iterations = 0

        frontier.add(initial_state)
        explored = set()

        while not frontier.is_empty():


            if memory.get_usage() > memory.max_usage:
                print_search_status(explored, frontier)
                print('Maximum memory usage exceeded.', file=sys.stderr, flush=True)
                return None

            chosen : 'State' = frontier.pop()
            explored.add(chosen)
            
            if chosen.is_goal_state():
                print_search_status(explored, frontier)
                return chosen.extract_plan()
            
            for state in chosen.get_expanded_states():
                if state not in explored and state not in frontier:
                    frontier.add(state)
                    iterations += 1
                    if iterations % 1000 == 0:
                        print_search_status(explored, frontier)

def print_search_status(explored, frontier):
    status_template = '#Expanded: {:8,}, #Frontier: {:8,}, #Generated: {:8,}, Time: {:3.3f} s\n[Alloc: {:4.2f} MB, MaxAlloc: {:4.2f} MB]\nProblem space explored: {:3.1f}%\n'
    elapsed_time = time.perf_counter() - start_time
    pct_explored = 100.0 * float(len(explored)) / (math.factorial(State.num_spaces) / math.factorial(State.num_spaces-State.num_objects))
    
    print(status_template.format(len(explored), frontier.size(), len(explored) + frontier.size(), elapsed_time, memory.get_usage(), memory.max_usage, pct_explored), file=sys.stderr, flush=True)
