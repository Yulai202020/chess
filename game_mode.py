# You can play with stockfish (You can set skill or elo)

# set elo
# python3 game_mode.py [elo] None

# set skill
# python3 game_mode.py None [skill]

from stockfish import Stockfish
import chess, sys

depth = 20 ; engine_name = "./stockfish16-linux-popcnt"

def coord(board, move):
    if move == "exit":
        quit()

    legal_moves_lst = [board.san(i) for i in board.legal_moves]
    legal_moves_lst2 = [str(board.parse_san(str(i))) for i in board.legal_moves]

    while not(move in legal_moves_lst or move in legal_moves_lst2):
        print("Your move isn't legit, try again!")
        move = input("Enter your move : ")

        if move == "exit":
            quit()

    return board.parse_san(move)

def get_position(engine):
    return engine.get_fen_position()

stockfish = Stockfish(engine_name, depth = depth, parameters = {"Hash": 2048, "Threads": 2, "Minimum Thinking Time": 30, "UCI_Chess960": "true"})
board = chess.Board(get_position(stockfish))

if sys.argv[1] != "None":
    stockfish.set_elo_rating(int(sys.argv[1]))
elif sys.argv[2] != "None":
    stockfish.set_skill_level(int(sys.argv[2]))
else:
    pass

mode = input("Enter w\\b white or black : ")

if mode == "b":
    while True:
        best_move = stockfish.get_best_move()
        stockfish.make_moves_from_current_position([best_move])

        print(stockfish.get_board_visual(False))
        print(best_move)

        board.set_fen(get_position(stockfish))
        if board.is_checkmate():
            print("You lost!")
            break

        elif board.is_stalemate():
            print("Draw by stalemate")
            break

        move = coord(board, input("Enter your move : "))

        stockfish.make_moves_from_current_position([move])
        print(stockfish.get_board_visual(False))
        
        board.set_fen(get_position(stockfish))
        if board.is_checkmate():
            print("You won!")
            break

        elif board.is_stalemate():
            print("Draw by stalemate")
            break

elif mode == "w":
    while True:
        move = coord(board, input("Enter your move : "))

        stockfish.make_moves_from_current_position([move])
        print(stockfish.get_board_visual())

        board.set_fen(get_position(stockfish))
        if board.is_checkmate():
            print("You won!")
            break

        elif board.is_stalemate():
            print("Draw by stalemate")
            break

        best_move = stockfish.get_best_move()
        stockfish.make_moves_from_current_position([best_move])

        print(stockfish.get_board_visual())
        print(best_move)

        board.set_fen(get_position(stockfish))
        if board.is_checkmate():
            print("You lost!")
            break

        elif board.is_stalemate():
            print("Draw by stalemate")
            break