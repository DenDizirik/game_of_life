import os
import argparse

def read_map(file_path):
    """
    Reads a map from a file and converts it into a grid.

    Args:
        file_path (str): The path to the map file.

    Returns:
        list[list[str]]: A 2D grid representing the map, where each cell is a character.
    """
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

def print_map(grid, camera_x, camera_y, width, height):
    """
    Prints a portion of the map based on the camera's position and dimensions.

    Args:
        grid (list[list[str]]): The 2D grid representing the map.
        camera_x (int): The vertical position of the camera.
        camera_y (int): The horizontal position of the camera.
        width (int): The width of the camera's view.
        height (int): The height of the camera's view.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(camera_x, min(camera_x + height, len(grid))):
        print(''.join(grid[i][camera_y:camera_y + width]))

def get_neighbors(grid, x, y):
    """
    Counts the number of alive neighbors around a cell.

    Args:
        grid (list[list[str]]): The 2D grid representing the map.
        x (int): The x-coordinate of the cell.
        y (int): The y-coordinate of the cell.

    Returns:
        int: The number of alive neighbors ('X') around the cell.
    """
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
    """
    Computes the next generation of the grid based on survival rules.

    Args:
        grid (list[list[str]]): The current grid state.
        survival_rules (dict): A dictionary with keys 'stay_alive' and 'become_alive',
            each containing a list of neighbor counts for respective rules.

    Returns:
        list[list[str]]: The updated grid for the next generation.
    """
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
    """
    Checks if there are any live cells ('X') in the grid.

    Args:
        grid (list[list[str]]): The current grid state.

    Returns:
        bool: True if there are live cells, False otherwise.
    """
    return any('X' in row for row in grid)

def adjust_camera(grid, focus_x, focus_y, width, height):
    """
    Adjusts the camera's position based on the focus point and screen dimensions.

    Args:
        grid (list[list[str]]): The 2D grid representing the map.
        focus_x (int): The x-coordinate of the focus point.
        focus_y (int): The y-coordinate of the focus point.
        width (int): The width of the camera's view.
        height (int): The height of the camera's view.

    Returns:
        tuple: The adjusted camera position as (camera_x, camera_y).
    """
    max_camera_x = max(0, len(grid) - height)
    max_camera_y = max(0, len(grid[0]) - width)

    camera_x = max(0, min(max_camera_x, focus_x - height // 2))
    camera_y = max(0, min(max_camera_y, focus_y - width // 2))

    return camera_x, camera_y

def find_focus(grid):
    """
    Finds the first live cell ('X') in the grid to set as the focus point.

    Args:
        grid (list[list[str]]): The 2D grid representing the map.

    Returns:
        tuple: The coordinates (x, y) of the first live cell, or the grid's center if no live cells exist.
    """
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == 'X':
                return x, y
    return len(grid) // 2, len(grid[0]) // 2

def main():
    """
    The main entry point of the Game of Life program.
    Handles user inputs, map reading, and game loop execution.
    """
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
