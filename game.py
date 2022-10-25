import chess
import chessAgents


class Game:
    def __init__(self, player, ai, color):
        # Creating new chess board
        self.gameState = chess.Board()

        self.player = player

        # Selecting AI agent
        if ai == 'ngmax':
            self.ai = chessAgents.NegamaxChessAgent
        elif ai == 'ngscout':
            self.ai = chessAgents.NegascoutChessAgent
        elif ai == 'pvs':
            self.ai = chessAgents.PvsChessAgent
        else:
            raise Exception("Nonexistent AI agent")

        self.color = color

    def makeAiMove(self):
        ai = self.ai()
        action = ai.getAction(self.gameState.copy())
        self.gameState.push(action)

    def makePlayerMove(self):
        player = self.player()
        action = player.getAction(self.gameState.copy())
        self.gameState.push(action)

    def makeMove(self):
        pass

    def isFinished(self):
        return self.gameState.is_stalemate() or self.gameState.is_insufficient_material() or \
               self.gameState.is_fivefold_repetition() or self.gameState.is_seventyfive_moves() or \
               self.gameState.is_checkmate()


player = 'rofl'
ai = 'ngmax'
color = 1

game = Game(player, ai, color)
print(game)

while not game.isFinished():
    game.makeMove()
