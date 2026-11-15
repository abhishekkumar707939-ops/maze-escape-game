"""
Maze Escape Game  (PS No. 59)
Rungta International Skills University - B.Tech CSE
Language: Python 3
Concepts: 2D Lists, Algorithms (BFS), Movement

Maze legend:  # = wall,  . = path,  P = player start,  E = exit
"""

from collections import deque

MAZE_TEMPLATE = [
    ["P", ".", ".", "#", "#"],
    ["#", "#", ".", "#", "#"],
    ["#", ".", ".", ".", "#"],
    ["#", ".", "#", "#", "#"],
    ["#", ".", ".", ".", "E"],
]

DIRECTIONS = {
    "W": (-1, 0),  # up
    "S": (1, 0),   # down
    "A": (0, -1),  # left
    "D": (0, 1),   # right
}


def find_symbol(maze, symbol):
    """Return (row, col) of the first cell holding `symbol`."""
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == symbol:
                return r, c
    return None


def inside(maze, r, c):
    return 0 <= r < len(maze) and 0 <= c < len(maze[0])


def print_maze(maze, player):
    """Print the maze with the player's current position shown as P."""
    print()
    for r, row in enumerate(maze):
        line = []
        for c, cell in enumerate(row):
            if (r, c) == player:
                line.append("P")
            elif cell == "P":
                line.append(".")  # start square is just a path once left
            else:
                line.append(cell)
        print(" ".join(line))
    print()


def bfs_shortest_path(maze, start, goal):
    """
    Breadth-First Search. Returns the shortest path as a list of
    (row, col) cells from start to goal, or None if unreachable.
    """
    queue = deque([start])
    parent = {start: None}
    while queue:
        cur = queue.popleft()
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return path[::-1]
        for dr, dc in DIRECTIONS.values():
            nr, nc = cur[0] + dr, cur[1] + dc
            nxt = (nr, nc)
            if inside(maze, nr, nc) and maze[nr][nc] != "#" and nxt not in parent:
                parent[nxt] = cur
                queue.append(nxt)
    return None


def try_move(maze, pos, key):
    """
    Attempt one move. Returns (new_pos, status) where status is one of:
    'moved', 'wall', 'outside', 'invalid'.
    """
    if key not in DIRECTIONS:
        return pos, "invalid"
    dr, dc = DIRECTIONS[key]
    nr, nc = pos[0] + dr, pos[1] + dc
    if not inside(maze, nr, nc):
        return pos, "outside"
    if maze[nr][nc] == "#":
        return pos, "wall"
    return (nr, nc), "moved"


def play(maze, scripted_keys=None):
    """
    Main game loop. If `scripted_keys` is given (a list of keys), those are
    used instead of keyboard input - handy for testing.
    Returns (final_position, moves, escaped).
    """
    start = find_symbol(maze, "P")
    exit_pos = find_symbol(maze, "E")
    pos, moves = start, 0
    keys = iter(scripted_keys) if scripted_keys is not None else None

    print_maze(maze, pos)
    while True:
        if keys is not None:
            key = next(keys, None)
            if key is None:
                break
            print(f"Move (W/A/S/D, Q to quit): {key}")
        else:
            raw = input("Move (W/A/S/D, Q to quit): ").strip().upper()
            if not raw:
                continue
            key = raw[0]
        key = key.upper()

        if key == "Q":
            print("Game ended by player.")
            break

        pos, status = try_move(maze, pos, key)

        if status == "invalid":
            print(f"Invalid key '{key}'. Use W, A, S or D only.")
            continue
        if status == "outside":
            print(f"Cannot move outside the maze. Player stays at {pos}. | Moves: {moves}")
            continue
        if status == "wall":
            print(f"Wall ahead. Move blocked. Player stays at {pos}.")
            continue

        moves += 1
        print(f"Player moved to (row {pos[0]}, col {pos[1]}) | Moves: {moves}")
        print_maze(maze, pos)

        if pos == exit_pos:
            print(f"You escaped the maze! Total moves: {moves}")
            return pos, moves, True

    print(f"Moves counted: {moves}")
    return pos, moves, False


def show_shortest_path(maze):
    start = find_symbol(maze, "P")
    goal = find_symbol(maze, "E")
    path = bfs_shortest_path(maze, start, goal)
    if path is None:
        print("No path exists from start to exit.")
        return
    print(f"Shortest path length: {len(path) - 1} steps")
    print("Path:", " -> ".join(str(p) for p in path))


def main():
    maze = [row[:] for row in MAZE_TEMPLATE]
    while True:
        print("\n===== MAZE ESCAPE GAME =====")
        print("1. Play the game")
        print("2. Show shortest path (BFS)")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            play(maze)
        elif choice == "2":
            show_shortest_path(maze)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
