import os

def read_map(file_path):
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def print_map(grid):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in grid:
        print(''.join(row))

def get_neighbors(grid, x, y):
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    count = 0
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 'X':
            count += 1
    return count

def next_generation(grid, survival_rules):
    new_grid = []
    for x in range(len(grid)):
        new_row = []
        for y in range(len(grid[0])):
            alive_neighbors = get_neighbors(grid, x, y)
            if grid[x][y] == 'X':
                if alive_neighbors in survival_rules['stay_alive']:
                    new_row.append('X')
                else:
                    new_row.append('.')
            else:
                if alive_neighbors in survival_rules['become_alive']:
                    new_row.append('X')
                else:
                    new_row.append('.')
        new_grid.append(new_row)
    return new_grid

def has_live_cells(grid):
    for row in grid:
        if 'X' in row:
            return True
    return False

def main():
    print("Choose survival rules:")
    print("1. Weak cells")
    print("2. Toughth cells")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        survival_rules = {
            'stay_alive': [3, 4],
            'become_alive': [3]
        }
    elif choice == '2':
        survival_rules = {
            'stay_alive': [2, 3],
            'become_alive': [3]
        }
    else:
        print("Invalid choice. Exiting.")
        return

    file_path = input("Enter the relative path to the map file: ")
    try:
        grid = read_map(file_path)
    except FileNotFoundError:
        print("Error: File not found.")
        return

    print("Press ENTER to advance to the next generation. Press CTRL+C to exit.")

    while True:
        print_map(grid)
        if not has_live_cells(grid):
            print("GAME OVER: No live cells remain.")
            break
        try:
            input("Press ENTER to continue...")
            grid = next_generation(grid, survival_rules)
        except KeyboardInterrupt:
            print("\nExiting the Game of Life.")
            break

if __name__ == "__main__":
    main()
