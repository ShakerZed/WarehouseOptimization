import random
import pygame

# Define categories and genders
categories = ["Lifestyle", "RoadRunners", "TrailRunners", "LowHikers", "MidHikers"]
genders = ["Men", "Women"]

# Initialize warehouse dimensions
rows, cols = 35, 5  # Exclude 2 rows for kids
entry_points = [(0, 0), (rows - 1, 0)]  # Define entry points

# Define layout rules for current layout
layout_rules_current = [
    {"range": range(3, 9), "category": "RoadRunners", "gender": "Women"},
    {"range": range(9, 12), "category": "TrailRunners", "gender": "Women"},
    {"range": range(12, 18), "category": "RoadRunners", "gender": "Men"},
    {"range": range(18, 22), "category": "TrailRunners", "gender": "Men"},
    {"range": range(22, 25), "category": "LowHikers", "gender": "Women"},
    {"range": range(25, 29), "category": "MidHikers", "gender": "Women"},
    {"range": range(29, 30), "category": "Blundstones", "gender": "Unisex"},
    {"range": range(30, 33), "category": "LowHikers", "gender": "Men"},
    {"range": range(33, 38), "category": "MidHikers", "gender": "Men"}
]

# Define function to populate warehouse
def populate_warehouse(layout_rules):
    warehouse = []
    for r in range(rows):
        row = []
        for rule in layout_rules:
            if r in rule["range"]:
                category, gender = rule["category"], rule["gender"]
                break
        else:
            category, gender = "Uncategorized", "Unspecified"
        for c in range(cols):
            bay = {
                "type": category,
                "gender": gender,
                "bay": r * cols + c + 1,
                "requires_ladder": c > 2
            }
            row.append(bay)
        warehouse.append(row)
    return warehouse

# Pygame Visualization Setup
CELL_SIZE = 20
SCREEN_WIDTH = cols * CELL_SIZE
SCREEN_HEIGHT = rows * CELL_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Employee Class with Movement Visualization
class Employee:
    def __init__(self, name, warehouse):
        self.name = name
        self.capacity = 4
        self.current_load = []
        self.trips = 0
        self.warehouse = warehouse
        self.position = list(entry_points[0])  # Start at the first entry point
        self.path = []

    def fetch_footwear(self, footwear_list):
        self.trips = 0
        for footwear in footwear_list:
            position = self.find_footwear(footwear)
            if position is not None:
                self.move_to(position)
                if len(self.current_load) < self.capacity:
                    self.current_load.append(footwear)
                else:
                    self.trips += 1
                    self.current_load = [footwear]
        if self.current_load:
            self.trips += 1
        return self.trips

    def find_footwear(self, footwear):
        for r, row in enumerate(self.warehouse):
            for c, bay in enumerate(row):
                if bay["type"] == footwear:
                    return (r, c)
        return None

    def move_to(self, destination):
        """Move step-by-step towards destination and log path."""
        while self.position != list(destination):
            if self.position[0] < destination[0]:
                self.position[0] += 1
            elif self.position[0] > destination[0]:
                self.position[0] -= 1
            if self.position[1] < destination[1]:
                self.position[1] += 1
            elif self.position[1] > destination[1]:
                self.position[1] -= 1
            self.path.append(tuple(self.position))
            draw_grid(self.path)

# Draw the warehouse grid and employee movement
def draw_grid(path):
    screen.fill((0, 0, 0))  # Black background
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)
    
    # Draw employee path
    for step in path:
        pygame.draw.rect(screen, (0, 255, 0), (step[1] * CELL_SIZE, step[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    pygame.display.flip()
    clock.tick(10)

# Run a single test visualization
warehouse = populate_warehouse(layout_rules_current)
employee = Employee("John", warehouse)
footwear_list = [random.choice(categories) for _ in range(5)]
employee.fetch_footwear(footwear_list)

# Main loop to keep Pygame running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
