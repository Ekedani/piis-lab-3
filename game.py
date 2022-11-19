import chess
import chessAgents


class Game:
    def __init__(self, player, ai, p_color):
        # Creating new chess board
        self.gameState = chess.Board()

        # Selecting player agent
        if player == 'negamax':
            self.player = chessAgents.NegamaxChessAgent
        elif player == 'negascout':
            self.player = chessAgents.NegascoutChessAgent
        elif player == 'pvs':
            self.player = chessAgents.PvsChessAgent
        elif player == 'console':
            self.player = chessAgents.ConsoleAgent
        else:
            self.player = chessAgents.ConsoleAgent

        # Selecting AI agent
        if ai == 'negamax':
            self.ai = chessAgents.NegamaxChessAgent
        elif ai == 'negascout':
            self.ai = chessAgents.NegascoutChessAgent
        elif ai == 'pvs':
            self.ai = chessAgents.PvsChessAgent
        else:
            self.ai = chessAgents.NegamaxChessAgent

        self.p_color = p_color

    def nextMove(self):
        turn = self.gameState.turn
        if turn == self.p_color:
            self.makePlayerMove()
        else:
            self.makeAiMove()

    def makeAiMove(self):
        agent = self.ai(2)
        action = agent.getAction(self.gameState.copy())
        self.gameState.push(action)

    def makePlayerMove(self):
        agent = self.player(1)
        action = agent.getAction(self.gameState.copy())
        self.gameState.push(action)

    def isFinished(self):
        return self.gameState.outcome() is not None


player = 'console'
ai = 'negamax'
p_color = 1

game = Game(player, ai, p_color)
while not game.isFinished():
    print(game.gameState)
    game.nextMove()
    print('===============')
print(game.gameState)
print(game.gameState.outcome())
