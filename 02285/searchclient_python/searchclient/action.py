from enum import Enum, unique

@unique
class ActionType(Enum):
    NoOp = 0
    Move = 1
    Push = 2
    Pull = 3

@unique
class Action(Enum):
    #   List of possible actions. Each action has the following parameters, 
    #    taken in order from left to right:
    #    1. The name of the action as a string. This is the string sent to the server
    #    when the action is executed. Note that for Pull and Push actions the syntax is
    #    "Push(X,Y)" and "Pull(X,Y)" with no spaces.
    #    2. Action type: NoOp, Move, Push or Pull (only NoOp and Move initially supported)
    #    3. agentRowDelta: the vertical displacement of the agent (-1,0,+1)
    #    4. agentColDelta: the horisontal displacement of the agent (-1,0,+1)
    #    5. boxRowDelta: the vertical displacement of the box (-1,0,+1)
    #    6. boxColDelta: the horisontal discplacement of the box (-1,0,+1) 
    #    Note: Origo (0,0) is in the upper left corner. So +1 in the vertical direction is down (S) 
    #    and +1 in the horisontal direction is right (E).
    NoOp = ("NoOp", ActionType.NoOp, 0, 0, 0, 0)

    MoveN = ("Move(N)", ActionType.Move, -1, 0, 0, 0)
    MoveS = ("Move(S)", ActionType.Move, 1, 0, 0, 0)
    MoveE = ("Move(E)", ActionType.Move, 0, 1, 0, 0)
    MoveW = ("Move(W)", ActionType.Move, 0, -1, 0, 0)
    
    PushN_N = ("Push(N,N)", ActionType.Push, -1, 0, -1, 0)
    PushW_N = ("Push(W,N)", ActionType.Push, 0, -1, -1, 0)
    PushE_N = ("Push(E,N)", ActionType.Push, 0,  1, -1, 0)
    
    PushS_S = ("Push(S,S)", ActionType.Push, 1,  0, 1, 0)
    PushW_S = ("Push(W,S)", ActionType.Push, 0, -1, 1, 0)
    PushE_S = ("Push(E,S)", ActionType.Push, 0,  1, 1, 0)
    
    PushN_W = ("Push(N,W)", ActionType.Push, -1, 0, 0, -1)
    PushS_W = ("Push(S,W)", ActionType.Push, 1,  0, 0, -1)
    PushW_W = ("Push(W,W)", ActionType.Push, 0, -1, 0, -1)
    
    PushN_E = ("Push(N,E)", ActionType.Push, -1, 0, 0, 1)
    PushS_E = ("Push(S,E)", ActionType.Push, 1,  0, 0, 1)
    PushE_E = ("Push(E,E)", ActionType.Push, 0,  1, 0, 1)
    
    
    PullN_N = ("Pull(N,N)", ActionType.Pull, -1, 0, -1, 0)
    PullW_N = ("Pull(W,N)", ActionType.Pull, 0, -1, -1, 0)
    PullE_N = ("Pull(E,N)", ActionType.Pull, 0,  1, -1, 0)
    
    PullS_S = ("Pull(S,S)", ActionType.Pull, 1,  0, 1, 0)
    PullW_S = ("Pull(W,S)", ActionType.Pull, 0, -1, 1, 0)
    PullE_S = ("Pull(E,S)", ActionType.Pull, 0,  1, 1, 0)
    
    PullN_W = ("Pull(N,W)", ActionType.Pull, -1, 0, 0, -1)
    PullS_W = ("Pull(S,W)", ActionType.Pull, 1,  0, 0, -1)
    PullW_W = ("Pull(W,W)", ActionType.Pull, 0, -1, 0, -1)
    
    PullN_E = ("Pull(N,E)", ActionType.Pull, -1, 0, 0, 1)
    PullS_E = ("Pull(S,E)", ActionType.Pull, 1,  0, 0, 1)
    PullE_E = ("Pull(E,E)", ActionType.Pull, 0,  1, 0, 1)
    
    def __init__(self, name, type, ard, acd, brd, bcd):
        self.name_ = name
        self.type = type
        self.agent_row_delta = ard # horisontal displacement agent (-1,0,+1)
        self.agent_col_delta = acd # vertical displacement agent (-1,0,+1)
        self.box_row_delta = brd # horisontal displacement box (-1,0,+1)
        self.box_col_delta = bcd # vertical displacement box (-1,0,+1)
