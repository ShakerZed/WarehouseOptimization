# Define categories and genders
import random

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

# Define layout rules for alternate layout
layout_rules_alternate = [
    {"range": range(0, 7), "category": "Lifestyle", "gender": "Men"},
    {"range": range(7, 14), "category": "RoadRunners", "gender": "Men"},
    {"range": range(14, 21), "category": "TrailRunners", "gender": "Men"},
    {"range": range(21, 28), "category": "LowHikers", "gender": "Men"},
    {"range": range(28, 35), "category": "MidHikers", "gender": "Men"},
    {"range": range(0, 7), "category": "MidHikers", "gender": "Women"},
    {"range": range(7, 14), "category": "LowHikers", "gender": "Women"},
    {"range": range(14, 21), "category": "TrailRunners", "gender": "Women"},
    {"range": range(21, 28), "category": "RoadRunners", "gender": "Women"},
    {"range": range(28, 35), "category": "Lifestyle", "gender": "Women"}
]

# Function to populate the warehouse grid
def populate_warehouse(layout_rules, sales_weights=None):
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
                "weight": sales_weights.get(category, 1) if sales_weights else 1,
                "requires_ladder": c > 2
            }
            row.append(bay)
        warehouse.append(row)
    return warehouse

# Define an Employee class
class Employee:
    def __init__(self, name, warehouse):
        self.name = name
        self.capacity = 4  # Maximum number of boxes the employee can carry
        self.current_load = []  # Current boxes the employee is holding
        self.trips = 0  # Number of trips made
        self.warehouse = warehouse

    def fetch_footwear(self, footwear_list):
        self.trips = 0
        for footwear in footwear_list:
            position = self.find_footwear(footwear)
            if position is not None:
                row, col = position
                if len(self.current_load) < self.capacity:
                    self.current_load.append(footwear)
                else:
                    self.trips += 1
                    self.current_load = [footwear]
        if self.current_load:
            self.trips += 1
        return self.trips

    def find_footwear(self, footwear):
        min_distance = float('inf')
        best_position = None
        for r, row in enumerate(self.warehouse):
            for c, bay in enumerate(row):
                if bay["type"] == footwear:
                    for entry_index, entry in enumerate(entry_points):
                        distance = abs(entry[0] - r) + abs(entry[1] - c)
                        if entry_index == 0:  # Apply 15% penalty for Entry Point 0
                            distance *= 1.15
                        if bay["requires_ladder"]:
                            distance += 5  # Penalty for using a ladder
                        if distance < min_distance:
                            min_distance = distance
                            best_position = (r, c)
        # If no exact match is found, assume a default position (e.g., first bay)
        if best_position is None:
            best_position = (0, 0)
        return best_position

# Simulate employee workflow and compare layouts
def simulate_and_compare(num_simulations=10000):
    random.seed(42)  # Set a fixed seed for consistent results
    sales_weights = {
        "Lifestyle": 3,
        "RoadRunners": 5,
        "TrailRunners": 4,
        "LowHikers": 2,
        "MidHikers": 1
    }

    total_trips_current = 0
    total_trips_alternate = 0

    for sim in range(num_simulations):
        footwear_list = [random.choice(categories) for _ in range(10)]  # Randomized footwear list

        # Simulate current layout
        warehouse_current = populate_warehouse(layout_rules_current, sales_weights)
        employee_current = Employee("John", warehouse_current)
        trips_current = employee_current.fetch_footwear(footwear_list)
        total_trips_current += trips_current

        # Simulate alternate layout
        warehouse_alternate = populate_warehouse(layout_rules_alternate, sales_weights)
        employee_alternate = Employee("John", warehouse_alternate)
        trips_alternate = employee_alternate.fetch_footwear(footwear_list)
        total_trips_alternate += trips_alternate

    avg_trips_current = total_trips_current / num_simulations
    avg_trips_alternate = total_trips_alternate / num_simulations

    print(f"Average trips for current layout: {avg_trips_current:.2f}")
    print(f"Average trips for alternate layout: {avg_trips_alternate:.2f}")

# Execute the simulation for 10,000 runs
simulate_and_compare(10000)
