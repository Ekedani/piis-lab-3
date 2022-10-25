import chess
import chessAgents


class Game:
    def __init__(self, player, ai, p_color):
        # Creating new chess board
        self.gameState = chess.Board()

        # Selecting player agent
        self.player = chessAgents.ConsoleAgent

        # Selecting AI agent
        if ai == 'ngmax':
            self.ai = chessAgents.NegamaxChessAgent
        elif ai == 'ngscout':
            self.ai = chessAgents.NegascoutChessAgent
        elif ai == 'pvs':
            self.ai = chessAgents.PvsChessAgent
        else:
            raise Exception("Nonexistent AI agent")

        self.p_color = p_color

    def nextMove(self):
        turn = self.gameState.turn
        if turn == self.p_color:
            self.makePlayerMove()
        else:
            self.makeAiMove()

    def makeAiMove(self):
        agent = self.ai()
        action = agent.getAction(self.gameState.copy())
        self.gameState.push(action)

    def makePlayerMove(self):
        agent = self.player()
        action = agent.getAction(self.gameState.copy())
        self.gameState.push(action)

    def isFinished(self):
        return self.gameState.is_stalemate() or self.gameState.is_insufficient_material() or \
               self.gameState.is_fivefold_repetition() or self.gameState.is_seventyfive_moves() or \
               self.gameState.is_checkmate()


player = 'rofl'
ai = 'ngmax'
p_color = 1

game = Game(player, ai, p_color)
print(game)

while not game.isFinished():
    print(game.gameState)
    game.nextMove()
