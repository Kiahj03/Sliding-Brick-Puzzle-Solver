import sys
import random

# loads game state
def load_state(filename):
    # reads file, separates each line
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
    # extracts width and height from first line of file
    x = lines[0].split(',')
    width = int(x[0])
    height = int(x[1])
    # puts game state within the matrix
    matrix = []
    for l in lines[1:-1]:
        matrix.append(list(map(int, filter(None, l.split(',')))))
    return width, height, matrix


# prints game state
def print_state(width, height, matrix):
    print(f"{width},{height},")
    for l in matrix:
        print(','.join(map(str, l)))


# clones a state
def clone_state(width, height, matrix):
    newMatrix = [r[:] for r in matrix]
    return width, height, newMatrix


# checks if game state matches goal state
def goal_state(matrix):
    # checks if there are any -1 within the matrix
    for r in matrix:
        if -1 in r:
            return False
    return True


# defines individual moves for each piece
def individual_moves(piece, x, y, width, height, matrix):
    MOVES = []
    # each checks if cell within direction is empty and if moving it in direction wont go out of bounds
    if x > 0 and matrix[x - 1][y] == 0:
        MOVES.append((piece, "up"))
    if x < height - 1 and matrix[x + 1][y] == 0:
        MOVES.append((piece, "down"))
    if y > 0 and matrix[x][y - 1] == 0:
        MOVES.append((piece, "left"))
    if y < width - 1 and matrix[x][y + 1] == 0:
        MOVES.append((piece, "right"))
    return MOVES


# finds all available moves for each state
def available_moves(width, height, matrix):
    MOVES = []
    # loops through entire matrix
    for x in range(height):
        for y in range(width):
            # skips goal, wall, empty cells, and master brick
            if matrix[x][y] >= 2:
                # new list containing all moves possible for given piece
                MOVES.extend(individual_moves(matrix[x][y], x, y, width, height, matrix))
    return MOVES


# applies the move inputted
def apply_move(move_string, width, height, matrix):
    move = move_string[1:-1].split(',')
    piece = int(move[0])
    direction = move[1].strip(' ').strip("''")
    # clones the original state
    clone = clone_state(width, height, matrix)
    w, h, cloneM = clone
    # loops through entire matrix
    for x in range(h):
        for y in range(w):
            # making sure the piece and loop matches
            if matrix[x][y] == piece:
                newX, newY = x, y
                # calculates new position of piece based on direction
                if direction == "up":
                    newX -= 1
                elif direction == "down":
                    newX += 1
                elif direction == "left":
                    newY -= 1
                elif direction == "right":
                    newY += 1
                # swapping the elements to make the move
                cloneM[x][y], cloneM[newX][newY] = cloneM[newX][newY], cloneM[x][y]
    # print new state with piece moved
    print_state(w, h, cloneM)


# compares the two states
def compare_states(matrix1, matrix2):
    # compares if they are equal to each other
    return matrix1 == matrix2


# normalizing a state
def normalize_state(width, height, matrix):
    nextIdx = 3
    for x in range(height):
        for y in range(width):
            if matrix[x][y] == nextIdx:
                nextIdx += 1
            elif matrix[x][y] > nextIdx:
                swap_idx(nextIdx, matrix[x][y], width, height, matrix)
                nextIdx += 1


# swapping indexes
def swap_idx(idx1, idx2, width, height, matrix):
    for x in range(height):
        for y in range(width):
            if matrix[x][y] == idx1:
                matrix[x][y] = idx2
            elif matrix[x][y] == idx2:
                matrix[x][y] = idx1


# random walk
def random_walk(width, height, matrix, N):
    for x in range(N):
        moves = available_moves(width, height, matrix)
        if not moves:
            break
        randoMove = str(random.choice(moves))
        x = randoMove.strip(" ").strip("()").split(",")
        p = x[0]
        d = x[1].strip(" ").strip("''")
        print(f"({p}, {d})")
        apply_move(randoMove, width, height, matrix)
        normalize_state(width, height, matrix)
        print()


# main function
if __name__ == "__main__":
    # checking if input is greater than 3
    if len(sys.argv) < 3:
        print("Error with input")
        sys.exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]
    width, height, matrix = load_state(filename)

    if command == "print":
        print_state(width, height, matrix)
    if command == "done":
        print(goal_state(matrix))
    if command == "availableMoves":
        moves = available_moves(width, height, matrix)
        for m in moves:
            x = str(m).strip("()").split(",")
            p = x[0]
            d = x[1].strip(" ").strip("''")
            print(f"({p}, {d})")
    if command == "applyMove":
        if len(sys.argv) < 4:
            print("Need more inputs for this function")
            sys.exit(1)
        move_string = sys.argv[3]
        apply_move(move_string, width, height, matrix)
    if command == "compare":
        if len(sys.argv) != 4:
            print("Error with inputs for this function")
            sys.exit(1)
        width2, height2, matrix2 = load_state(sys.argv[3])
        print(compare_states(matrix, matrix2))
    if command == "norm":
        normalize_state(width, height, matrix)
        print_state(width, height, matrix)
    if command == "random":
        if len(sys.argv) != 4:
            print("Error with inputs for this function")
            sys.exit(1)
        N = int(sys.argv[3])
        print_state(width, height, matrix)
        print()
        random_walk(width, height, matrix, N)
