import os
import argparse

def read_map(file_path):
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def print_map(grid, camera_x, camera_y, width, height):
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(camera_x, min(camera_x + height, len(grid))):
        print(''.join(grid[i][camera_y:camera_y + width]))

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
    return any('X' in row for row in grid)

def adjust_camera(grid, focus_x, focus_y, width, height):
    max_camera_x = max(0, len(grid) - height)
    max_camera_y = max(0, len(grid[0]) - width)

    camera_x = max(0, min(max_camera_x, focus_x - height // 2))
    camera_y = max(0, min(max_camera_y, focus_y - width // 2))

    return camera_x, camera_y

def find_focus(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'X':
                return x, y
    return len(grid) // 2, len(grid[0]) // 2

def main():
    parser = argparse.ArgumentParser(description="Game of Life")
    parser.add_argument('map_file', type=str, help="Path to the map file")
    args = parser.parse_args()

    print("Choose survival rules:")
    print("1. Weak cells")
    print("2. Tough cells")
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

    try:
        grid = read_map(args.map_file)
    except FileNotFoundError:
        print("Error: File not found.")
        return

    camera_x, camera_y = 0, 0
    screen_width, screen_height = 150, 35  # Updated dimensions

    print("Press ENTER to advance to the next generation. Press CTRL+C to exit.")

    while True:
        print_map(grid, camera_x, camera_y, screen_width, screen_height)
        if not has_live_cells(grid):
            print("GAME OVER: No live cells remain.")
            break
        try:
            input("Press ENTER to continue...")
            grid = next_generation(grid, survival_rules)
            focus_x, focus_y = find_focus(grid)
            camera_x, camera_y = adjust_camera(grid, focus_x, focus_y, screen_width, screen_height)
        except KeyboardInterrupt:
            print("\nExiting the Game of Life.")
            break

if __name__ == "__main__":
    main()
