import chess
import chessAgents


class Game:
    def __init__(self, player, ai, p_color, ai_depth):
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
            self.player = chessAgents.ConsoleChessAgent
        else:
            self.player = chessAgents.ConsoleChessAgent

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
        self.p_depth = 2

        if not ai_depth.isdigit() or not 0 < int(ai_depth) < 6:
            print(f'AI depth {ai_depth} is not supported. Using depth 2 instead')
            self.ai_depth = 2
        else:
            self.ai_depth = int(ai_depth)

    def nextMove(self):
        turn = self.gameState.turn
        if turn == self.p_color:
            self.makePlayerMove()
        else:
            self.makeAiMove()

    def makeAiMove(self):
        agent = self.ai(self.ai_depth)
        action = agent.getAction(self.gameState.copy())
        self.gameState.push(action)

    def makePlayerMove(self):
        agent = self.player(self.p_depth)
        action = agent.getAction(self.gameState.copy())
        self.gameState.push(action)

    def isFinished(self):
        return self.gameState.outcome() is not None

    def printConfig(self):
        print('Game configuration:',
              f'Player color: {"White" if self.p_color == 1 else "Black"}',
              f'Player agent: {self.player.__name__}',
              f'Player depth (not used in console agent): {self.p_depth}',
              f'AI agent: {self.ai.__name__}',
              f'AI depth: {self.ai_depth}',
              sep='\n')

    def printOutcome(self):
        if not self.isFinished():
            print('Game is not finished!')
        else:
            outcome = self.gameState.outcome()
            print('Game is finished:',
                  f'Reason: {outcome.termination}',
                  sep='\n')
            if hasattr(outcome, 'winner'):
                print(f'Winner: {"White" if outcome.winner == True else "Black"}', )
