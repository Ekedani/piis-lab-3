import chess


class ChessAgent:
    def __init__(self, depth=3):
        self.depth = int(depth)

    @staticmethod
    def evaluateBoard(gameState: chess.Board):
        """
        A simple chess board evaluation function based on material and mobility.
        For detailed information about it visit https://www.chessprogramming.org/Evaluation
        """
        # Material
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

        if gameState.is_checkmate():
            if gameState.outcome().winner == chess.WHITE:
                bk = 0
            else:
                wk = 0

        p_weight = 10
        n_weight = 100
        b_weight = 300
        r_weight = 500
        q_weight = 1000
        k_weight = 30000

        material_score = p_weight * (wp - bp) + n_weight * (wn - bn) + b_weight * (wb - bb) + r_weight * (wr - br) \
                         + q_weight * (wq - bq) + k_weight * (wk - bk)

        # Mobility
        mobility_1 = gameState.legal_moves.count()
        gameState.push(chess.Move.null())
        mobility_2 = gameState.legal_moves.count()
        gameState.pop()
        if gameState.turn == chess.WHITE:
            mobility = mobility_1 - mobility_2
        else:
            mobility = mobility_2 - mobility_1
        mobility_weight = 0.2
        mobility_score = mobility * mobility_weight

        return material_score + mobility_score


class NegamaxChessAgent(ChessAgent):
    """
    An implementation of chess agent based on Negamax algorithm.
    For detailed information about it (and pseudocode) visit https://www.chessprogramming.org/Negamax
    """

    def getAction(self, gameState: chess.Board):
        def negamax(state: chess.Board, color, depth=self.depth):
            if depth == 0 or state.outcome() is not None:
                return None

            legal_actions = state.legal_moves
            best_score = float('-inf')
            best_action = None

            for action in legal_actions:
                state.push(action)
                score = -recursiveNegamax(state, -color, depth - 1)
                if score > best_score:
                    best_score = score
                    best_action = action
                state.pop()
            return best_action

        def recursiveNegamax(state: chess.Board, color, depth):
            if depth == 0 or state.outcome() is not None:
                return color * self.evaluateBoard(state)

            legal_actions = state.legal_moves
            best_score = float('-inf')

            for action in legal_actions:
                state.push(action)
                score = -recursiveNegamax(state, -color, depth - 1)
                best_score = max(best_score, score)
                state.pop()

            return best_score

        color = 1 if gameState.turn else -1
        return negamax(gameState, color=color)


class NegascoutChessAgent(ChessAgent):
    def getAction(self, gameState: chess.Board):
        def negascout(state: chess.Board, color, depth=self.depth, alpha=float('-inf'), beta=float('inf')):
            if depth == 0 or state.outcome() is not None:
                return None

            legal_actions = state.legal_moves
            a = alpha
            b = beta
            is_first_move = True
            best_action = None

            for action in legal_actions:
                state.push(action)
                score = recursiveNegascout(state, -color, depth - 1, -b, -alpha)
                if a < score < b and depth <= 2 and not is_first_move:
                    a = -recursiveNegascout(state, -color, depth - 1, -beta, -score)
                state.pop()
                if score > a:
                    a = score
                    best_action = action

                if a >= beta:
                    return action
                b = a + 1
                is_first_move = False

            return best_action

        def recursiveNegascout(state: chess.Board, color, depth, alpha, beta):
            if depth == 0 or state.outcome() is not None:
                return color * self.evaluateBoard(state)

            legal_actions = state.legal_moves
            a = alpha
            b = beta
            is_first_move = True

            for action in legal_actions:
                state.push(action)
                score = recursiveNegascout(state, -color, depth - 1, -b, -alpha)
                if a < score < b and depth <= 2 and not is_first_move:
                    a = -recursiveNegascout(state, -color, depth - 1, -beta, -score)
                state.pop()
                a = max(a, score)
                if a >= beta:
                    return a
                b = a + 1
                is_first_move = False

            return a

        color = 1 if gameState.turn else -1
        return negascout(gameState, color=color)


class PvsChessAgent(ChessAgent):
    """
    An implementation of chess agent based on Principal variation search algorithm.
    For detailed information about it (and pseudocode) visit https://www.chessprogramming.org/Principal_Variation_Search
    """

    def getAction(self, gameState: chess.Board):
        def pvs(state: chess.Board, color, depth=self.depth, alpha=float('-inf'), beta=float('inf')):
            if depth == 0 or state.outcome() is not None:
                return None

            legal_actions = state.legal_moves
            best_action = None

            b_search_pv = True
            for action in legal_actions:
                state.push(action)
                if b_search_pv:
                    score = -recursivePvs(state, -color, depth - 1, -beta, -alpha)
                else:
                    score = -recursivePvs(state, -color, depth - 1, -alpha - 1, -alpha)
                    if score > alpha:
                        score = -recursivePvs(state, -color, depth - 1, -beta, -alpha)
                state.pop()
                if score >= beta:
                    return action
                if score > alpha:
                    alpha = score
                    b_search_pv = False
                    best_action = action

            return best_action

        def recursivePvs(state: chess.Board, color, depth, alpha, beta):
            if depth == 0 or state.outcome() is not None:
                return color * self.evaluateBoard(state)

            legal_actions = state.legal_moves
            b_search_pv = True

            for action in legal_actions:
                state.push(action)
                if b_search_pv:
                    score = -recursivePvs(state, -color, depth - 1, -beta, -alpha)
                else:
                    score = -recursivePvs(state, -color, depth - 1, -alpha - 1, -alpha)
                    if score > alpha:
                        score = -recursivePvs(state, -color, depth - 1, -beta, -alpha)
                state.pop()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
                    b_search_pv = False

            return alpha

        color = 1 if gameState.turn else -1
        return pvs(gameState, color=color)


class ConsoleAgent(ChessAgent):
    def getAction(self, gameState: chess.Board):
        legal_actions = gameState.legal_moves
        print('Input your move: ', legal_actions)
        action = gameState.parse_san(input())
        print(action in legal_actions)
        print(legal_actions)
        while action not in legal_actions:
            print('Invalid move. Try again:')
            action = gameState.parse_san(input())
        return action
