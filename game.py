import logging

# logging.getLogger().setLevel(logging.INFO)

class Mancala:
    def __init__(self):
        self.row_len = 6
        self.start_piece_num = 4
        self.board = [self.start_piece_num] * ((self.row_len + 1)*2)
        # self.board = [3, 6, 6, 6, 5, 0, 2, 5, 0, 6, 5, 5, 0, 2]
        self.player1_idx = self.row_len
        self.player2_idx = self.row_len * 2 + 1

        self.board[self.row_len] = 0
        self.board[self.row_len * 2 + 1] = 0
        self.turn = 0
    
    def get_turn(self):
        return "player_1" if self.turn % 2 == 0 else "player_2"

    def __str__(self):
        player2_score_len = len(f"{self.board[self.player2_idx]}->")
        return f"player_1: {self.board[0: self.player1_idx]}<-{self.board[self.player1_idx]}\nplayer_2: {self.board[self.player1_idx+1: self.player2_idx]}<-{self.board[self.player2_idx]}"
        # string = f"{' '*player2_score_len}{self.board[0: self.player1_idx]}<-{self.board[self.player1_idx]}\n{self.board[self.player2_idx]}->{self.board[self.player1_idx+1: self.player2_idx]}" 
        return string
    
    def is_game_over(self):
        return sum(self.board[0: self.player1_idx]) == 0 or sum(self.board[self.player1_idx+1: self.player2_idx]) == 0

    def get_legal_moves(self):
        # Returns a list of legal moves from the current state
        moves = []
        start_idx = 0 if self.get_turn() == "player_1" else self.player1_idx + 1
        end_idx = self.player1_idx if self.get_turn() == "player_1" else self.player2_idx
        # moves = [i for i in range(start_idx, end_idx) if self.board[i] > 0]
        for i in range(start_idx, end_idx):
            if self.board[i] > 0:
                moves.append(i)
        logging.info(f"moves: {moves}")
        return moves

    def move(self, choice, indexed=False, simulate=False):
        # logging.info("="*30)
        if simulate:
            original_board = self.board[:]
            original_turn = self.turn
        logging.info(self.board)
        logging.info(self)
        row_idx = self.turn % 2
        if row_idx:
            max_start = self.row_len + 1 
            max_end = self.player2_idx
            player_idx = self.player2_idx
        else:
            max_start = 0
            max_end = self.player1_idx
            player_idx = self.player1_idx
        logging.info(f"max_start: {max_start} max_end: {max_end}")
        # convert hole index
        if indexed:
            hole_idx = choice
        else:
            hole_idx = choice + max_start
        logging.info(f"hole_idx: {hole_idx}")
        if hole_idx < max_start or hole_idx > max_end:
            logging.info("Invalid move.")
            return False
        num_stones = self.board[hole_idx]
        # logging.info(f"num_stones: {num_stones}")
        self.board[hole_idx] = 0

        curr_idx = hole_idx
        while num_stones > 0:
            curr_idx = (curr_idx + 1) % len(self.board)
            self.board[curr_idx] += 1
            num_stones -= 1

        logging.info(f"curr_idx: {curr_idx}")
        # RULE: If you drop the last stone into an empty hole on your side of the board, you can capture pieces from the other side
        if curr_idx >= max_start and curr_idx < max_end and self.board[curr_idx] == 1:
            # logging.info(f"curr_idx: {curr_idx}")
            own_hole = self.board[curr_idx]
            opp_idx = len(self.board) - curr_idx - 2
            opp_hole = self.board[opp_idx]
            # [0, 6, 6, 6, 5, 0, 0, 5, 0, 6, 5, 5, 0, 0]
            #                    ^                    ^
            self.board[player_idx] += own_hole
            self.board[player_idx] += opp_hole
            self.board[curr_idx] = 0
            self.board[opp_idx] = 0
            if not simulate:
                print(f"own_hole: {own_hole} {curr_idx} opp_hole: {opp_hole} {opp_idx}")
                print(f"{self.get_turn()} captured {own_hole} pieces and {opp_hole} from the other side!")

        # RULE: If you drop the last stone into your store you get a free turn
        if curr_idx != player_idx:
            self.turn += 1
        else:
            if not simulate:
                print(f"{self.get_turn()} gets a free turn!")

        # RULE: If any of the rows are empty then the player who still has pieces on their side of the board captures everything
        if sum(self.board[0: self.player1_idx]) == 0:
            if not simulate:
                print(f"Capturing all pieces on player_2's side")
            self.board[self.player2_idx] += sum(self.board[self.player1_idx+1: self.player2_idx])
            for i in range(self.player1_idx+1, self.player2_idx):
                self.board[i] = 0
        elif sum(self.board[self.player1_idx+1: self.player2_idx]) == 0:
            if not simulate:
                print(f"Capturing all pieces on player_1's side")
            self.board[self.player1_idx] += sum(self.board[0: self.player1_idx])
            for i in range(0, self.player1_idx):
                self.board[i] = 0
        # logging.info("="*30)

        if simulate:
            return original_board, original_turn
    
    def undo_move(self, original_board, original_turn):
        self.board = original_board
        self.turn = original_turn

    def eval_board(self):
        # return self.board[self.player1_idx] - self.board[self.player2_idx]
        return self.board[self.player2_idx] - self.board[self.player1_idx]
        
    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over():
            return None, self.eval_board()

        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_legal_moves():
                board, turn = self.move(move, indexed=True, simulate=True)
                _, eval = self.minimax(depth-1, alpha, beta, False)
                self.undo_move(board, turn)

                if eval > max_eval:
                    best_move = move
                    max_eval = eval

                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    break
            return best_move, max_eval

        else:
            min_eval = float('inf')
            for move in self.get_legal_moves():
                board, turn = self.move(move, indexed=True, simulate=True)
                _, eval = self.minimax(depth-1, alpha, beta, True)
                self.undo_move(board, turn)

                if eval < min_eval:
                    best_move = move
                    min_eval = eval

                beta = min(beta, min_eval)
                if alpha >= beta:
                    break
            return best_move, min_eval
        