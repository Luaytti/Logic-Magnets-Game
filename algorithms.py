from collections import deque
import heapq

def valid_move(board, current_row, current_col, next_row, next_col):
    """Check if the next position is valid and empty"""
    if 0 <= next_row < len(board) and 0 <= next_col < len(board[0]):
        return board[next_row][next_col] == 'E'
    return False

def get_valid_moves(board, row, col):
    moves = []
    for r, c in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
        if valid_move(board, row, col, r, c):
            moves.append((r, c))
    return moves

def repulsion(board, current_row, current_col, next_row, next_col):
    if not valid_move(board, current_row, current_col, next_row, next_col):
        return False
    board[current_row][current_col] = 'E'
    board[next_row][next_col] = 'P'
    return True

def attraction(board, current_row, current_col, next_row, next_col):
    if not valid_move(board, current_row, current_col, next_row, next_col):
        return False
    board[current_row][current_col] = 'E'
    board[next_row][next_col] = 'R'
    return True

def is_goal_state(board):
    for row in board:
        for cell in row:
            if cell == 'E':  
                return False
    return True

def solve_with_bfs(board):
    queue = deque([(board, [])])
    visited = set()

    while queue:
        current_state, moves = queue.popleft()

        if is_goal_state(current_state):
            return moves

        for row in range(len(board)):
            for col in range(len(board[0])):
                piece = current_state[row][col]
                if piece in ('P', 'R'):
                    valid_moves = get_valid_moves(current_state, row, col)
                    for move in valid_moves:
                        new_state = [row[:] for row in current_state]
                        if piece == 'P':
                            repulsion(new_state, row, col, move[0], move[1])
                        elif piece == 'R':
                            attraction(new_state, row, col, move[0], move[1])

                        if new_state not in visited:
                            visited.add(new_state)
                            queue.append((new_state, moves + [move]))

    return [] 


def solve_with_dfs(board):
    stack = [(board, [])]
    visited = set()

    while stack:
        current_state, moves = stack.pop()

        if is_goal_state(current_state):
            return moves

        for row in range(len(board)):
            for col in range(len(board[0])):
                piece = current_state[row][col]
                if piece in ('P', 'R'):
                    valid_moves = get_valid_moves(current_state, row, col)
                    for move in valid_moves:
                        new_state = [row[:] for row in current_state]
                        if piece == 'P':
                            repulsion(new_state, row, col, move[0], move[1])
                        elif piece == 'R':
                            attraction(new_state, row, col, move[0], move[1])

                        if new_state not in visited:
                            visited.add(new_state)
                            stack.append((new_state, moves + [move]))

    return [] 

def solve_with_ucs(board):
    priority_queue = []
    heapq.heappush(priority_queue, (0, board, []))
    visited = set()

    while priority_queue:
        cost, current_state, moves = heapq.heappop(priority_queue)

        if is_goal_state(current_state):
            return moves

        for row in range(len(board)):
            for col in range(len(board[0])):
                piece = current_state[row][col]
                if piece in ('P', 'R'):
                    valid_moves = get_valid_moves(current_state, row, col)
                    for move in valid_moves:
                        new_state = [row[:] for row in current_state]
                        if piece == 'P':
                            repulsion(new_state, row, col, move[0], move[1])
                        elif piece == 'R':
                            attraction(new_state, row, col, move[0], move[1])

                        new_state_tuple = tuple(tuple(row) for row in new_state)
                        if new_state_tuple not in visited:
                            visited.add(new_state_tuple)
                            heapq.heappush(priority_queue, (cost + 1, new_state, moves + [move]))
    return []
