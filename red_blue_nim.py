import argparse
import math

def start_game(red, blue, depth, first_player, version):
    """Main game loop to alternate between human and computer turns."""
    while True:
        if is_game_over(red, blue):
            declare_winner(red, blue, first_player, version)
            break

        print(f"Red marbles: {red}\tBlue marbles: {blue}\n")

        if first_player == 1:
            red, blue = human_turn(red, blue)
        else:
            red, blue = computer_turn(red, blue, depth, version)

        first_player = 3 - first_player  # Toggle turn between human and computer

def is_game_over(red, blue):
    """Check if the game is over when one pile is empty."""
    return red == 0 or blue == 0

def declare_winner(red, blue, first_player, version):
    """Declare the winner based on game version and the final state."""
    score = eval_function(red, blue, True)
    if version == "standard":
        winner = "Computer" if first_player == 1 else "Human"
    else:  # Misère version
        winner = "Human" if first_player == 1 else "Computer"
    print(f"Game over! {winner} wins with {abs(score)} points.")

def human_turn(red, blue):
    """Prompt the human player to choose a valid move."""
    while True:
        try:
            choice = input("Choose a pile (r/b): ").strip().lower()
            count = int(input("How many marbles to remove? (1 or 2): "))

            if count not in [1, 2]:
                raise ValueError("Invalid number of marbles.")

            if choice == 'r' and red >= count:
                red -= count
                break
            elif choice == 'b' and blue >= count:
                blue -= count
                break
            else:
                raise ValueError("Invalid move! Not enough marbles.")
        except ValueError as e:
            print(e)

    return red, blue

def computer_turn(red, blue, depth, version):
    """Make the computer's move using minimax with alpha-beta pruning."""
    print("Computer's Turn")
    choice, _ = minimax(red, blue, depth, True, -math.inf, math.inf, version)
    print(f"Computer picks {'Red' if choice == 'r' else 'Blue'}")

    if choice == 'r':
        red -= 1
    elif choice == 'b':
        blue -= 1

    return red, blue

def eval_function(red, blue, is_max):
    """Calculate the evaluation score based on remaining marbles."""
    score = (2 * red) + (3 * blue)
    return score if is_max else -score

def minimax(red, blue, depth, is_max, alpha, beta, version):
    """Perform the minimax algorithm with alpha-beta pruning."""
    if depth == 0 or is_game_over(red, blue):
        return None, eval_function(red, blue, is_max)

    best_score = -math.inf if is_max else math.inf
    best_option = None

    moves = (
        [('r', 2), ('b', 2), ('r', 1), ('b', 1)]
        if version == "standard"
        else [('b', 1), ('r', 1), ('b', 2), ('r', 2)]
    )

    for choice, count in moves:
        new_red = red - count if choice == 'r' and red >= count else red
        new_blue = blue - count if choice == 'b' and blue >= count else blue

        if new_red == red and new_blue == blue:
            continue  # Skip invalid moves

        _, score = minimax(new_red, new_blue, depth - 1, not is_max, alpha, beta, version)

        if is_max:
            if score > best_score:
                best_score = score
                best_option = choice
            alpha = max(alpha, score)
        else:
            if score < best_score:
                best_score = score
                best_option = choice
            beta = min(beta, score)

        if beta <= alpha:
            break  # Alpha-beta pruning

    return best_option, best_score

def parse_arguments():
    """Parse command-line arguments for the game."""
    parser = argparse.ArgumentParser(description="Play Red-Blue Nim.")
    parser.add_argument('red', type=int, help="Number of red marbles")
    parser.add_argument('blue', type=int, help="Number of blue marbles")
    parser.add_argument(
        '-v', '--version', choices=["standard", "misere"], default="standard",
        help="Game version (default: standard)"
    )
    parser.add_argument(
        '-p', '--first_player', choices=["computer", "human"], default="computer",
        help="First player (default: computer)"
    )
    parser.add_argument(
        '-d', '--depth', type=int, default=0, help="Depth for minimax search (default: full depth)"
    )
    return parser.parse_args()

def main():
    """Main function to start the game with user inputs."""
    args = parse_arguments()

    # Convert first player to numeric value
    first_player = 2 if args.first_player == "computer" else 1

    # Set full search depth if not specified
    depth = args.depth if args.depth > 0 else args.red + args.blue

    # Start the game
    start_game(args.red, args.blue, depth, first_player, args.version)

if __name__ == "__main__":
    main()
