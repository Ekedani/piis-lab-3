import chessGame
import sys
import getopt


def main(argv):
    # Player is white and controlled by user by default
    player = 'console'
    p_color = 1

    ai = None
    ai_depth = None

    opts, args = getopt.getopt(argv, "a:d:")
    for opt, arg in opts:
        if opt == '-a':
            ai = arg
        if opt == '-d':
            ai_depth = arg

    game = chessGame.Game(player, ai, p_color, ai_depth)
    game.printGameConfig()

    while not game.isFinished():
        print(game.gameState)
        game.nextMove()
        print('===============')
    print(game.gameState)
    print(game.gameState.outcome())


if __name__ == "__main__":
    main(sys.argv[1:])
