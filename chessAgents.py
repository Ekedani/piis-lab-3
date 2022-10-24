import chess


class ChessAgent:
    @staticmethod
    def evaluationFunction(gameState):
        # Figures num
        wp = len(gameState.pieces(chess.PAWN, chess.WHITE))
        bp = len(gameState.pieces(chess.PAWN, chess.BLACK))
        wn = len(gameState.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(gameState.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(gameState.pieces(chess.BISHOP, chess.WHITE))
        bb = len(gameState.pieces(chess.BISHOP, chess.BLACK))
        wr = len(gameState.pieces(chess.ROOK, chess.WHITE))
        br = len(gameState.pieces(chess.ROOK, chess.BLACK))
        wq = len(gameState.pieces(chess.QUEEN, chess.WHITE))
        bq = len(gameState.pieces(chess.QUEEN, chess.BLACK))
        wk = len(gameState.pieces(chess.KING, chess.WHITE))
        bk = len(gameState.pieces(chess.KING, chess.BLACK))

        # Figures importance
        p_weight = 10
        n_weight = 100
        b_weight = 300
        r_weight = 500
        q_weight = 1000
        k_weight = 30000

        # The more important figures - the better position is
        material_score = p_weight * (wp - bp) + n_weight * (wn - bn) + b_weight * (wb - bb) + r_weight * (wr - br) \
                         + q_weight * (wq - bq) + k_weight * (wk - bk)

        # Mobility
        mobility_1 = len(gameState.legal_moves)
        gameState.push(chess.Move.null())
        mobility_2 = len(gameState.legal_moves)
        gameState.pop()
        if gameState.turn:
            # White
            mobility = mobility_2 - mobility_1
        else:
            # Black
            mobility = mobility_1 - mobility_2

        mobility_weight = 1
        mobility_score = mobility * mobility_weight

        return material_score + mobility_score

    @staticmethod
    def isDraw(gameState):
        return gameState.is_stalemate() or gameState.is_insufficient_material() or \
               gameState.is_fivefold_repetition() or gameState.is_seventyfive_moves()

    def __init__(self, index=0, depth=2):
        self.index = int(index)
        self.depth = int(depth)


class NegamaxChessAgent(ChessAgent):
    def getAction(self):
        pass

    def negamax(self):
        pass

    def recursiveNegamax(self, gameState, depth, color):
        if depth == 0:
            return color * self.evaluationFunction(gameState)

        legal_actions = gameState.legal_moves
        value = float('-inf')

        for action in legal_actions:
            next_state = gameState


class NegascoutChessAgent(ChessAgent):
    def getAction(self):
        pass

    def negascout(self):
        pass


class PvsChessAgent(ChessAgent):
    def getAction(self):
        pass

    def pvs(self):
        pass
