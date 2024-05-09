from game import Mancala
import time

game = Mancala()
print(game.board)
print(game)
while not game.is_game_over():
    if game.get_turn() == "player_1":
        move = int(input(f"> "))
        res = game.move(move)
    else:
        print("Running minimax...")
        start = time.time()
        move, eval = game.minimax(10, float('-inf'), float('inf'), True)
        end = time.time()
        print(f"Evaluation finished in {end - start}s")
        print(f"Bot is playing {move-7} with expected value {eval}")
        res = game.move(move-7)
    print(game.board)
    print(game)
print("Game over!")
print(f"player_1: {game.board[game.player1_idx]} player_2: {game.board[game.player2_idx]}")