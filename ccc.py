import chess
import chess.pgn
import chess.engine

import io, time, math, random
from datetime import datetime

WHITE = "White"
BLACK = "Black"

def pgn_to_string(pgn):
    pgn_io = io.StringIO()
    print(pgn, file=pgn_io)
    pgn_string = pgn_io.getvalue()

    return pgn_string

def generate_pgn(board):
    game = chess.pgn.Game()
    node = game
    for move in board.move_stack:
        node = node.add_variation(move)

    return game

def play_game(engine1_path, engine2_path, clock = 180, addiction = 0):
    board = chess.Board()
    
    total_time = {WHITE: clock, BLACK: clock}

    engines_path = {WHITE: engine1_path, BLACK: engine2_path}

    engine1 = chess.engine.SimpleEngine.popen_uci(engines_path[WHITE])
    engine2 = chess.engine.SimpleEngine.popen_uci(engines_path[BLACK])

    engines = {WHITE: engine1, BLACK: engine2}

    while not board.is_game_over():
        print(board)

        color = WHITE if board.turn else BLACK
        engine = engines[color]
        
        if total_time[color] <= 0:
            print(f"{color} loses on time!")
            return board, "1-0" if color == BLACK else "0-1"

        start_time = time.time()

        result = engine.play(board, chess.engine.Limit(white_clock=total_time[WHITE], black_clock=total_time[BLACK]))
        board.push(result.move)

        end_time = time.time()

        delta = end_time - start_time
        move_time = math.ceil(delta * 10) / 10
        total_time[color] -= move_time
        total_time[color] += addiction

        print(f"{engines_path[color]} as {color} moved in {move_time} seconds (Remaining time: {total_time[color]}s)")
    
    engine1.quit()
    engine2.quit()

    print(board)

    return board, board.result()

def main():
    clock = 60 # in seconds
    addiction = 1
    count_of_games = 10

    # change to engines what u have
    engine_paths = ["./stockfish17", "./komodo-14"]
    engine_score = [0, 0]

    random.shuffle(engine_paths) # make who will be white

    for i in range(1, count_of_games + 1):
        output_pgn_filename = f"game-{i}.pgn"

        # play game
        if i % 2 == 0:
            board, result = play_game(engine_paths[1], engine_paths[0], clock, addiction)
        else:
            board, result = play_game(engine_paths[0], engine_paths[1], clock, addiction)

        # create pgn file
        with open(output_pgn_filename, "w") as f:
            pgn = generate_pgn(board)

            pgn.headers["Event"] = "CCC"
            pgn.headers["Site"] = "Online"
            pgn.headers["Date"] = datetime.now().strftime("%Y.%m.%d")
            pgn.headers["Round"] = i
            pgn.headers["White"] = engine_paths[0] if i % 2 != 0 else engine_paths[1]
            pgn.headers["Black"] = engine_paths[0] if i % 2 == 0 else engine_paths[1]
            pgn.headers["Result"] = result

            pgn_string = pgn_to_string(pgn)
            f.write(pgn_string)

        # print result
        if result == "1-0":
            print(f"{engine_paths[0]} won!")
            engine_score[0] += 1

        elif result == "0-1":
            print(f"{engine_paths[1]} won!")
            engine_score[1] += 1

        elif result == "1/2-1/2":
            print("Draw.")
            engine_score[0] += 0.5
            engine_score[1] += 0.5

        else:
            print(f"Unknown result.")
    
    print(f"{engine_paths[0]} {engine_score[0]}")
    print(f"{engine_paths[1]} {engine_score[1]}")


if __name__ == "__main__":
    main()
