# You can analysis with stockfish

from stockfish import Stockfish
import chess

fen = "8/2b1kp2/p1p3p1/Pp1p1nPp/1P1PpP1P/2P1P2R/2K5/6R1 w -- 0 1"; depth = 20; top_moves = 5; engine_path = "./stockfish16_popcnt"
# starting position fen - rbbnknqr/pppppppp/8/8/8/8/PPPPPPPP/RBBNKNQR w KQkq - 0 1

def coord(board, move, peace):
    if move == "exit":
        quit()

    legal_moves_lst1 = [board.san(i) for i in board.legal_moves]
    legal_moves_lst2 = [str(board.parse_san(str(i))) for i in board.legal_moves]

    while not(move in legal_moves_lst1 or move in legal_moves_lst2):
        print("Your move isn't legit, try again!")
        move = input(f"Enter your move for {peace}: ")

        if move == "exit":
            quit()

    return board.parse_san(move)

def get_position(engine):
    return engine.get_fen_position()

def print_position(board, engine):
    best_move = engine.get_top_moves(top_moves)

    for i in best_move:
        if i["Centipawn"] is not None:
            i["Centipawn"] /= 100
    
    print(engine.get_board_visual())

    for i in range(len(best_move)):
        move = chess.Move.from_uci(best_move[i]["Move"])
        print(f"{i+1}st line", board.san(move), "Evaluation", best_move[i]["Centipawn"], "Mate in", best_move[i]["Mate"])

# create engine class
# You can change ELO stockfish.set_elo_rating(rating), or skill set_skill_level(skill)

stockfish = Stockfish(engine_path, depth = depth, parameters = {"Hash": 2048, "Threads": 2, "Minimum Thinking Time": 30, "UCI_Chess960": "true"})
stockfish.set_fen_position(fen)

board = chess.Board(get_position(stockfish))

while True:
    # for white

    print_position(board, stockfish)

    print("\nEnter exit for exit")
    move_white = coord(board, input("Enter your move for WHITE: "), "WHITE")

    stockfish.make_moves_from_current_position([move_white])
    board.set_fen(get_position(stockfish))

    if board.is_checkmate():
        print("Black lost, white won.")
        break

    elif board.is_stalemate():
        print("Draw by stalemate.")
        break  

    # for black

    print_position(board, stockfish)

    print("\nEnter exit for exit")
    move_black = coord(board, input("Enter your move for BLACK: "), "BLACK")

    stockfish.make_moves_from_current_position([move_black])
    board.set_fen(get_position(stockfish))

    if board.is_checkmate():
        print("White lost, black won.")
        break

    elif board.is_stalemate():
        print("Draw by stalemate.")
        break        
