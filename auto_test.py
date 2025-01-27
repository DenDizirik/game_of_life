import unittest
from unittest.mock import patch
import os

# Ваши функции, которые мы тестируем.
def read_map(file_path):
    with open(file_path, 'r') as f:
        return [list(line.strip()) for line in f.readlines()]

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

def adjust_camera(grid, camera_x, camera_y, focus_x, focus_y, width, height):
    top = camera_x
    bottom = camera_x + height
    left = camera_y
    right = camera_y + width

    out_of_top = focus_x < top
    out_of_bottom = focus_x >= bottom
    out_of_left = focus_y < left
    out_of_right = focus_y >= right

    out_of_bounds_count = sum([out_of_top, out_of_bottom, out_of_left, out_of_right])

    if out_of_bounds_count == 1:
        if out_of_top:
            camera_x = max(0, focus_x)
        elif out_of_bottom:
            camera_x = min(len(grid) - height, focus_x - height + 1)

        if out_of_left:
            camera_y = max(0, focus_y)
        elif out_of_right:
            camera_y = min(len(grid[0]) - width, focus_y - width + 1)

    return camera_x, camera_y

class TestGameOfLife(unittest.TestCase):

    def test_read_map(self):
        test_file = 'test_map.txt'
        with open(test_file, 'w') as f:
            f.write("X.\n.X\n")

        expected_result = [['X', '.'], ['.', 'X']]
        self.assertEqual(read_map(test_file), expected_result)
        os.remove(test_file)

        with self.assertRaises(FileNotFoundError):
            read_map('non_existent_file.txt')

    def test_get_neighbors(self):
        grid = [
            ['.', 'X', '.'],
            ['X', 'X', '.'],
            ['.', '.', 'X']
        ]
        self.assertEqual(get_neighbors(grid, 1, 1), 3)  # Положительный случай
        self.assertEqual(get_neighbors(grid, 0, 0), 0)  # Отрицательный случай

    def test_next_generation(self):
        grid = [
            ['.', 'X', '.'],
            ['X', 'X', '.'],
            ['.', '.', 'X']
        ]
        survival_rules = {
            'stay_alive': [2, 3],
            'become_alive': [3]
        }
        expected_result = [
            ['X', 'X', '.'],
            ['X', 'X', '.'],
            ['.', '.', '.']
        ]
        self.assertEqual(next_generation(grid, survival_rules), expected_result)  # Положительный случай

        grid_invalid = []  # Отрицательный случай: пустая карта
        self.assertEqual(next_generation(grid_invalid, survival_rules), [])

    def test_has_live_cells(self):
        self.assertTrue(has_live_cells([['.', 'X'], ['.', '.']]))  # Положительный случай
        self.assertFalse(has_live_cells([['.', '.'], ['.', '.']]))  # Отрицательный случай

    def test_adjust_camera(self):
        grid = [
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.'],
            ['.', '.', '.', '.']
        ]
        self.assertEqual(adjust_camera(grid, 0, 0, 3, 3, 2, 2), (2, 2))  # Положительный случай
        self.assertEqual(adjust_camera(grid, 0, 0, 0, 0, 2, 2), (0, 0))  # Отрицательный случай

if __name__ == "__main__":
    unittest.main()
