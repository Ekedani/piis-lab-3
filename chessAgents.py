import chess


class Agent:
    @staticmethod
    def evaluationFunction(gameState):
        return 1

    def __init__(self, index=0, depth=2):
        self.index = int(index)
        self.depth = int(depth)


class NegamaxAgent(Agent):
    def getAction(self):
        pass


class NegascoutAgent(Agent):
    def getAction(self):
        pass


class PvsAgent(Agent):
    def getAction(self):
        pass
