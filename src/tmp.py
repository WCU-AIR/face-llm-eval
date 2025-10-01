def frogger_game(n, s, m, board):
    visited = set()
    current_position = s
    hop_count = 0

    while True:
        if current_position in visited:
            print("cycle")
            print(hop_count)
            return
        visited.add(current_position)

        square_value = board[current_position - 1]
        
        if square_value == m:
            print("magic")
            print(hop_count)
            return
        elif square_value > 0:
            current_position += square_value
        else:
            current_position -= abs(square_value)
            
        hop_count += 1
        
        if current_position < 1 or current_position > n:
            if current_position < 1:
                print("left")
            else:
                print("right")
            print(hop_count)
            return

# Input reading
n, s, m = map(int, input().split())
board = list(map(int, input().split()))

frogger_game(n, s, m, board)