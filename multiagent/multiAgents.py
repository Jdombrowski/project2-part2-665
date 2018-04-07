# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        foodList = newFood.asList()
        capList = successorGameState.getCapsules()
        nearest_ghost_distance = 99999
        nearest_food_distance = 99999
        scaredGhostMod = 0
        actionMod = 0
        nearest_cap_dist = 999


        for ghost in newGhostStates:
            temp_distance = util.manhattanDistance(newPos, ghost.configuration.pos)
            nearest_ghost_distance = min(nearest_ghost_distance, temp_distance)

        for current_food in foodList:
            temp_distance = util.manhattanDistance(newPos, current_food)
            nearest_food_distance = min(nearest_food_distance, temp_distance)


        # add penalty for mot moving
        if action == 'Stop':
            actionMod = -10

        for cap in capList:
            temp_distance = util.manhattanDistance(newPos, cap)
            nearest_cap_dist = min(nearest_cap_dist, temp_distance)

        #  avg 1255.0
        #  total_value = successorGameState.getScore() + nearest_ghost_distance/nearest_food_distance + actionMod + scaredGhostMod


        #  avg 1336.7
        if nearest_ghost_distance < newScaredTimes[0]:
            #  go towards the ghost
            scaredGhostMod = 100
            total_value = successorGameState.getScore() - nearest_ghost_distance / nearest_food_distance + actionMod + scaredGhostMod
        else:
            total_value = successorGameState.getScore() + nearest_ghost_distance / nearest_food_distance + actionMod + scaredGhostMod

        if capList:
            total_value = total_value + nearest_ghost_distance/nearest_cap_dist


        # print total_value
        return total_value


def findClosestFood(current_location, current_list):
    closest_goal = 99999
    for goal in current_list:
        temp_distance = util.manhattanDistance(current_location, goal)
        closest_goal = min(temp_distance, closest_goal)



def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # todo

        # Initialize the lists needed for the steps3
        # currentSuccessors = gameState.generateSuccessor(agentIndex, legalActions[0])
        # numAgents = gameState.getNumAgents()
        return self.findValues(0, gameState, 0)[0]


    def findValues(self, pindex, gameState, pdepth):
        current_index = pindex
        current_depth = pdepth

        if current_index == gameState.getNumAgents():
            current_depth += 1
            current_index = 0

        legalActions = gameState.getLegalActions(current_index)
        if (len(legalActions) == 0) or (current_depth == self.depth):
            return '', self.evaluationFunction(gameState)

        if current_index == 0:
            return self.maxValue(current_index, gameState, current_depth)
        else:
            return self.minValue(current_index, gameState, current_depth)

    def maxValue(self, pindex, current_game_state, current_depth):
        current_index = pindex
        currentValue = -float('inf')
        best_action = ''

        for possible_move in current_game_state.getLegalActions(current_index):
            successor = current_game_state.generateSuccessor(current_index, possible_move)

            _, this_value = self.findValues(current_index+1, successor, current_depth)

            if this_value > currentValue:
                currentValue = this_value
                best_action = possible_move

        return best_action, currentValue

    def minValue(self, current_index, current_gameState, current_depth):
        currentValue = float('inf')
        best_action = ''

        for possible_move in current_gameState.getLegalActions(current_index):
            successor = current_gameState.generateSuccessor(current_index, possible_move)

            _, this_value = self.findValues(current_index+1, successor, current_depth)

            if this_value < currentValue:
                currentValue = this_value
                best_action = possible_move

        return best_action, currentValue




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float('inf')
        beta = float('inf')
        return (self.alphaBetaPrune(gameState, 0, 0, alpha, beta))[0]


    def alphaBetaPrune(self, gameState, pindex, pdepth, alpha, beta):
        current_index = pindex
        current_depth = pdepth

        if current_index == gameState.getNumAgents():
            current_depth += 1
            current_index = 0

        legalActions = gameState.getLegalActions(current_index)
        if (len(legalActions) == 0) or (current_depth == self.depth):
            return '', self.evaluationFunction(gameState)

        if current_index == 0:
            return self.maxValue(gameState, current_index, current_depth, alpha, beta)
        else:
            return self.minValue(gameState, current_index, current_depth, alpha, beta)

    def maxValue(self, gameState, pindex, pdepth, alpha, beta):
        current_index = pindex
        best_max_action = ''
        current_value = -float('inf')

        for possible_move in gameState.getLegalActions(current_index):
            successor = gameState.generateSuccessor(current_index, possible_move)

            temp_move, temp_value = self.alphaBetaPrune(successor, current_index + 1, pdepth, alpha, beta)

            current_value = max(current_value, temp_value)

            if current_value > beta:
                best_max_action = possible_move
                return best_max_action, current_value
            # alpha = max(alpha, current_value)
            if current_value > alpha:
                alpha = current_value
                best_max_action = possible_move

        return best_max_action, current_value

    def minValue(self, gameState, pindex, pdepth, alpha, beta):
        current_index = pindex
        best_min_action = ''
        current_value = float('inf')

        for possible_move in gameState.getLegalActions(current_index):
            successor = gameState.generateSuccessor(pindex, possible_move)

            temp_move, temp_value = self.alphaBetaPrune(successor, current_index + 1, pdepth, alpha, beta)

            current_value = min(current_value, temp_value)

            if current_value < alpha:
                best_min_action = possible_move
                return best_min_action, current_value
            # beta = min(beta, current_value)
            if current_value < beta:
                beta = current_value
                best_min_action = possible_move

        return best_min_action, current_value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(0, gameState, 0)[0]

    def expectimax(self, pindex, gameState, pdepth):
        current_index = pindex
        current_depth = pdepth

        if current_index == gameState.getNumAgents():
            current_depth += 1
            current_index = 0

        legalActions = gameState.getLegalActions(current_index)
        if (len(legalActions) == 0) or (current_depth == self.depth):
            return '', self.evaluationFunction(gameState)

        if current_index == 0:
            return self.maxValue(current_index, gameState, current_depth)
        else:
            return self.minValue(current_index, gameState, current_depth)

    def maxValue(self, pindex, current_game_state, current_depth):
        current_index = pindex
        currentValue = -float('inf')
        best_action = ''

        for possible_move in current_game_state.getLegalActions(current_index):
            successor = current_game_state.generateSuccessor(current_index, possible_move)

            _, this_value = self.expectimax(current_index + 1, successor, current_depth)

            if this_value > currentValue:
                currentValue = this_value
                best_action = possible_move

        return best_action, currentValue

    def minValue(self, current_index, current_gameState, current_depth):
        current_sum = 0
        count = 0
        best_action = ''

        for possible_move in current_gameState.getLegalActions(current_index):
            successor = current_gameState.generateSuccessor(current_index, possible_move)

            _, this_value = self.expectimax(current_index + 1, successor, current_depth)

            current_sum += this_value
            count += 1

        return best_action, current_sum/count

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    pacman_pos = currentGameState.data.agentStates[0]
    newFood = currentGameState.data.food.asList()
    newGhostStates = currentGameState.data.agentStates[1]
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"

    foodList = newFood.asList()
    capList = currentGameState.data.capsules.aslist()
    nearest_ghost_distance = 99999
    nearest_food_distance = 99999
    scaredGhostMod = 0
    actionMod = 0
    nearest_cap_dist = 999

    for ghost in newGhostStates:
        temp_distance = util.manhattanDistance(pacman_pos, ghost.configuration.pos)
        nearest_ghost_distance = min(nearest_ghost_distance, temp_distance)

    for current_food in foodList:
        temp_distance = util.manhattanDistance(pacman_pos, current_food)
        nearest_food_distance = min(nearest_food_distance, temp_distance)

    # add penalty for mot moving
    # if action == 'Stop':
    #     actionMod = -10

    for cap in capList:
        temp_distance = util.manhattanDistance(pacman_pos, cap)
        nearest_cap_dist = min(nearest_cap_dist, temp_distance)

    #  avg 1255.0
    #  total_value = successorGameState.getScore() + nearest_ghost_distance/nearest_food_distance + actionMod + scaredGhostMod

    #  avg 1336.7
    if nearest_ghost_distance < newScaredTimes[0]:
        #  go towards the ghost
        scaredGhostMod = 100
        total_value = currentGameState.getScore() - nearest_ghost_distance / nearest_food_distance + actionMod + scaredGhostMod
    else:
        total_value = currentGameState.getScore() + nearest_ghost_distance / nearest_food_distance + actionMod + scaredGhostMod

    if capList:
        total_value = total_value + nearest_ghost_distance / nearest_cap_dist

    # print total_value
    return total_value

# Abbreviation
better = betterEvaluationFunction

