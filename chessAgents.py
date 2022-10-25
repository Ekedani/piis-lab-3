import chess


class ChessAgent:
    def __init__(self, index=0, depth=2):
        self.index = int(index)
        self.depth = int(depth)

    @staticmethod
    def evaluationFunction(gameState: chess.Board):
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
        mobility_1 = gameState.legal_moves.count()
        gameState.push(chess.Move.null())
        mobility_2 = gameState.legal_moves.count()
        gameState.pop()
        if gameState.turn:
            # White
            mobility = mobility_2 - mobility_1
        else:
            # Black
            mobility = mobility_1 - mobility_2

        mobility_weight = 0.2
        mobility_score = mobility * mobility_weight

        return material_score + mobility_score

    @staticmethod
    def isDraw(gameState: chess.Board):
        return gameState.is_stalemate() or gameState.is_insufficient_material() or \
               gameState.is_fivefold_repetition() or gameState.is_seventyfive_moves()


class NegamaxChessAgent(ChessAgent):
    def getAction(self, gameState: chess.Board):
        def negamax(state: chess.Board, depth=self.depth, color=-1):
            if state.is_checkmate():
                return None

            if depth == 0 or self.isDraw(state):
                return None

            legal_actions = state.legal_moves
            best_score = float('-inf')
            best_action = None

            for action in legal_actions:
                state.push(action)
                score = -recursiveNegamax(state, depth - 1, -color)
                if score > best_score:
                    best_score = score
                    best_action = action
                state.pop()
            return best_action

        def recursiveNegamax(state: chess.Board, depth, color):
            if state.is_checkmate():
                return color * float('inf')

            if depth == 0 or self.isDraw(state):
                return color * self.evaluationFunction(state)

            legal_actions = state.legal_moves
            best_score = float('-inf')

            for action in legal_actions:
                state.push(action)
                score = -recursiveNegamax(state, depth - 1, -color)
                best_score = max(best_score, score)
                state.pop()

            return best_score

        return negamax(gameState)


class NegascoutChessAgent(ChessAgent):
    def getAction(self, gameState: chess.Board):
        pass

    def negascout(self):
        pass


class PvsChessAgent(ChessAgent):
    def getAction(self, gameState: chess.Board):
        pass

    def pvs(self):
        pass
