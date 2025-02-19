import random
import pygame

# Define categories and genders available in the warehouse
categories = ["Lifestyle", "RoadRunners", "TrailRunners", "LowHikers", "MidHikers"]
genders = ["Men", "Women"]

# Initialize warehouse dimensions
rows, cols = 35, 5  # Warehouse has 35 rows and 5 columns
entry_points = [(0, 1), (rows - 1, 1)]  # Employee starts at the second column for accurate movement
exit_points = [(0, 1), (rows - 1, 1)]  # Employee exits through the same entry points

# Pygame visualization setup for displaying warehouse simulation
CELL_SIZE = 20  # Size of each cell representing warehouse bays
SCREEN_WIDTH = cols * CELL_SIZE
SCREEN_HEIGHT = rows * CELL_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)  # Font for displaying footwear count

# Function to generate warehouse layout based on predefined rules
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

# Function to draw the warehouse grid and visualize employee movement
def draw_grid(path, employee_position, load_count):
    screen.fill((0, 0, 0))  # Black background
    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)  # Draw warehouse bays
    
    # Highlight the employee's movement path in green
    for step in path:
        pygame.draw.rect(screen, (0, 255, 0), (step[1] * CELL_SIZE, step[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw the employee as a blue square at the current position
    pygame.draw.rect(screen, (0, 0, 255), (employee_position[1] * CELL_SIZE, employee_position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Display the number of footwear boxes the employee is carrying
    text_surface = font.render(str(load_count), True, (255, 255, 255))
    screen.blit(text_surface, (employee_position[1] * CELL_SIZE + 5, employee_position[0] * CELL_SIZE + 5))
    
    pygame.display.flip()

# Employee class representing a worker retrieving footwear
class Employee:
    def exit_warehouse(self):
        """Moves the employee to the nearest exit point to deload before re-entering."""
        exit_row, exit_col = exit_points[0]  # Default exit point
        while self.position[0] != exit_row:
            pygame.event.pump()
            if self.position[0] < exit_row:
                self.position[0] += 1
            elif self.position[0] > exit_row:
                self.position[0] -= 1
            self.path.append(tuple(self.position))
            draw_grid(self.path, self.position, 0)
            clock.tick(10)
        print(f"Employee {self.name} has exited and deloaded.")
        self.current_load = []  # Clear load after deloading
    def __init__(self, name, warehouse):
        self.name = name
        self.capacity = 4  # Employee can carry up to 4 footwear boxes at a time
        self.current_load = []  # List to track collected footwear
        self.trips = 0  # Counter for trips taken
        self.warehouse = warehouse
        self.position = list(entry_points[0])  # Start at entry point
        self.path = []  # List tracking movement path

    def fetch_footwear(self, footwear_list):
        """Processes a footwear request by moving to the correct location and picking up items."""
        print(f"New client request: {footwear_list}")
        for footwear in footwear_list:
            position = self.find_footwear(footwear)
            if position is not None:
                self.move_to(position)
                if len(self.current_load) < self.capacity:
                    self.current_load.append(footwear)
                    print(f"Employee {self.name} picked up {footwear}. Current load: {self.current_load}")
                else:
                    print(f"Employee {self.name} full. Exiting warehouse to deload.")
                    self.exit_warehouse()
                    self.current_load = [footwear]  # Start a new load
                    print(f"Employee {self.name} re-entering warehouse. Current load: {self.current_load}")
        if self.current_load:
            self.exit_warehouse()  # Ensure employee exits after final collection
            self.exit_warehouse()  # Ensure employee exits after final collection
            self.exit_warehouse()
        return self.trips

    def find_footwear(self, footwear):
        """Finds the row where the requested footwear is stored, assuming entry at column 1."""
        for r, row in enumerate(self.warehouse):
            for c, bay in enumerate(row):
                if bay["type"] == footwear:
                    return (r, 0)
        return None

    def move_to(self, destination):
        """Moves the employee step-by-step to the target bay, entering from column 1."""
        target_row, _ = destination
        target_col = 0  # Always enter from column 1

        while self.position[0] != target_row:
            pygame.event.pump()
            if self.position[0] < target_row:
                self.position[0] += 1
            elif self.position[0] > target_row:
                self.position[0] -= 1
            self.path.append(tuple(self.position))
            draw_grid(self.path, self.position, len(self.current_load))
            clock.tick(10)
        
        while self.position[1] != target_col:
            pygame.event.pump()
            self.position[1] -= 1
            self.path.append(tuple(self.position))
            draw_grid(self.path, self.position, len(self.current_load))
            clock.tick(10)

# Define layout rules for the current warehouse setup
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

# Initialize warehouse and employee
warehouse = populate_warehouse(layout_rules_current)
employee = Employee("John", warehouse)

# Run continuous client requests simulation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if random.random() < 0.02:
        footwear_list = [random.choice(categories) for _ in range(random.randint(1, 4))]
        employee.fetch_footwear(footwear_list)
    
pygame.quit()
 