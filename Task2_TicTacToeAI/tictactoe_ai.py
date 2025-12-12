# tictactoe_ai.py
"""
Tic-Tac-Toe with Minimax AI (Terminal)
Human = 'X' (you)
AI    = 'O' (computer)
Run: python tictactoe_ai.py
"""

import json
from datetime import datetime

LOGFILE = "game_logs.jsonl"

def make_empty_board():
    return [" "]*9

def print_board(b):
    # board indices:
    # 0 | 1 | 2
    # 3 | 4 | 5
    # 6 | 7 | 8
    print()
    print(f" {b[0]} | {b[1]} | {b[2]} ")
    print("---+---+---")
    print(f" {b[3]} | {b[4]} | {b[5]} ")
    print("---+---+---")
    print(f" {b[6]} | {b[7]} | {b[8]} ")
    print()

def available_moves(board):
    return [i for i, v in enumerate(board) if v == " "]

def is_winner(board, player):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    return any(board[a]==board[b]==board[c]==player for a,b,c in wins)

def is_board_full(board):
    return all(cell != " " for cell in board)

def evaluate(board):
    if is_winner(board, "O"):
        return 1  # AI win
    elif is_winner(board, "X"):
        return -1 # Human win
    else:
        return 0  # draw or ongoing

def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    if score != 0 or is_board_full(board):
        return score

    if is_maximizing:
        best = -999
        for move in available_moves(board):
            board[move] = "O"
            val = minimax(board, depth+1, False)
            board[move] = " "
            if val > best:
                best = val
        return best
    else:
        best = 999
        for move in available_moves(board):
            board[move] = "X"
            val = minimax(board, depth+1, True)
            board[move] = " "
            if val < best:
                best = val
        return best

def best_move(board):
    best_val = -999
    move_choice = None
    for move in available_moves(board):
        board[move] = "O"
        move_val = minimax(board, 0, False)
        board[move] = " "
        if move_val > best_val:
            best_val = move_val
            move_choice = move
    return move_choice

def log_game(history, result):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "moves": history,  # list of {"player": "X"/"O", "pos": index}
        "result": result
    }
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def human_move(board):
    while True:
        try:
            pos = input("Enter your move (1-9): ").strip()
            if pos.lower() in ("exit","quit"):
                return None
            pos = int(pos) - 1
            if pos not in range(9):
                print("Choose a number 1-9 corresponding to an empty cell.")
                continue
            if board[pos] != " ":
                print("Cell already taken. Choose another.")
                continue
            return pos
        except ValueError:
            print("Please enter a number between 1 and 9, or 'exit' to quit.")

def main():
    print("Tic-Tac-Toe — Human (X) vs AI (O)")
    print("Cells are numbered 1 to 9 like this:")
    print(" 1 | 2 | 3 ")
    print("---+---+---")
    print(" 4 | 5 | 6 ")
    print("---+---+---")
    print(" 7 | 8 | 9 ")
    print("Type 'exit' to quit anytime.\n")

    board = make_empty_board()
    history = []
    current_player = "X"  # human starts

    while True:
        print_board(board)
        if current_player == "X":
            pos = human_move(board)
            if pos is None:
                print("Game aborted by user.")
                log_game(history, "aborted")
                break
            board[pos] = "X"
            history.append({"player":"X","pos":pos})
            if is_winner(board, "X"):
                print_board(board)
                print("Congratulations — You (X) win!")
                log_game(history, "human_win")
                break
            current_player = "O"
        else:
            print("AI is thinking...")
            ai_pos = best_move(board)
            # if board is empty and best_move returns None (shouldn't), pick center or random
            if ai_pos is None:
                for fallback in (4, 0, 2, 6, 8):
                    if board[fallback] == " ":
                        ai_pos = fallback
                        break
            board[ai_pos] = "O"
            print(f"AI chose position {ai_pos+1}")
            history.append({"player":"O","pos":ai_pos})
            if is_winner(board, "O"):
                print_board(board)
                print("AI (O) wins. Better luck next time!")
                log_game(history, "ai_win")
                break
            current_player = "X"

        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            log_game(history, "draw")
            break

if __name__ == "__main__":
    main()