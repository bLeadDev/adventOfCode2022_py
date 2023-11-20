import os

class Position:
    def __init__(self, x, y, elevation):
        self.x = x
        self.y = y
        self.elevation = elevation

class GridMap:
    def __init__(self, grid):
        self.grid = grid
        self.start_pos = None
        self.dest_pos = None
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.create_map()

    def create_map(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] == 'S':
                    self.start_pos = Position(j, i, 'a')  # Assuming start is always at 'a'
                elif self.grid[i][j] == 'E':
                    self.dest_pos = Position(j, i, 'z')   # Assuming destination is always at 'z'

    def is_valid_move(self, current, next_pos):
        elevation_diff = ord(next_pos.elevation) - ord(current.elevation)
        return -1 <= elevation_diff <= 1  # Check if elevation difference is within [-1, 1]

    def find_shortest_path(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
        queue = [(self.start_pos, 0)]
        visited = set()
        
        while queue:
            current, steps = queue.pop(0)
            if current == self.dest_pos:
                return steps
            
            visited.add((current.x, current.y))
            
            for dx, dy in directions:
                new_x, new_y = current.x + dx, current.y + dy
                if 0 <= new_x < self.cols and 0 <= new_y < self.rows and (new_x, new_y) not in visited:
                    next_pos = Position(new_x, new_y, self.grid[new_y][new_x])
                    if self.is_valid_move(current, next_pos):
                        queue.append((next_pos, steps + 1))
                        visited.add((new_x, new_y))
        
        return -1  # Destination not reachable

# Example usage:
    @staticmethod
    def read_heightmap_from_file(file_name):
        current_path = os.path.dirname(__file__)
        lines = []
        try:
            with open(os.path.join(current_path, file_name), 'r') as file:
                for line in file:
                    lines.append(line.strip())  # Remove any leading or trailing whitespace
        except Exception as e:
            print(f"An error occurred: {e}")
        return lines

if __name__ == "__main__":
    file_name = 'text_input.txt'  # Update with the correct file path
    heightmap = GridMap.read_heightmap_from_file(file_name)

    grid_map = GridMap(heightmap)
    steps = grid_map.find_shortest_path()
    print(f"Fewest steps required: {steps}")  # Output the fewest steps required to reach the destination
