# You can analysis with any engine

import chess
import chess.engine

engine_path = "./stockfish16-linux-popcnt"; depth = 20

board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
engine = chess.engine.SimpleEngine.popen_uci(engine_path)

def get_best_move(board, engine):
    info = engine.analyse(board, chess.engine.Limit(depth = depth))
    best_move_engine = board.san(info['pv'][0])

    return best_move_engine, info["score"].white().score()/100

while True:
    print(board)
    best_move, score = get_best_move(board, engine)

    print("Best move", best_move, "Evaluation", score)

    print("\nEnter exit for exit.")

    move = input("Enter your move: ")
    if move == "exit":
        break
    
    legal_moves_lst1 = [str(board.parse_san(str(i))) for i in board.legal_moves]
    legal_moves_lst2 = [board.san(i) for i in board.legal_moves]

    while not (move in legal_moves_lst1 or move in legal_moves_lst2):
        print("Your move isnt legit, try again!")
        move = input("Enter your move: ")

        if move == "exit":
            engine.quit(); quit()

    board.push_san(move)
    print()

engine.quit()