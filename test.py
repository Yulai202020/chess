# idk stockfish vs komodo

import chess.engine

board = chess.Board("rnbqkbnrr/ppppppppp/9/9/9/9/9/PPPPPPPPP/RNBQKBNRR w KQkq - 0 1")
engine1 = chess.engine.SimpleEngine.popen_uci("stockfish16.exe")
engine2 = chess.engine.SimpleEngine.popen_uci("komodo13.exe")

print(board)

while True:
    info1 = engine1.analyse(board, chess.engine.Limit(depth = 20))
    best_move_engine1 = board.san(info1['pv'][0])
    board.push_san(best_move_engine1)
    print()
    print("Komodo moved:", best_move_engine1)
    print("score:", info1["score"])
    print(board)

    if board.is_checkmate():
        print("Engine 1 won!")
        break
    elif board.is_stalemate():
        print("Draw by stalemate")
        break

    info2 = engine2.analyse(board, chess.engine.Limit(depth = 20))
    best_move_engine2 = board.san(info2['pv'][0])
    board.push_san(best_move_engine2)
    print()
    print("Stockfish moved:", best_move_engine2)
    print("score:", info1["score"])
    print(board)

    if board.is_checkmate():
        print("Engine 2 won!")
        break
    elif board.is_stalemate():
        print("Draw by stalemate")
        break

engine1.quit()
engine2.quit()