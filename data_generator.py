import random

# Number of entries you want to generate
num_entries = 200000  # adjust as needed

# Coordinate boundaries (you can adjust these ranges)
x_min, x_max = 0.0, 800.0
y_min, y_max = 0.0, 500.0

# Output to file
with open("generated_city.txt", "w") as f:
    for i in range(1, num_entries + 1):
        x = round(random.uniform(x_min, x_max), 2)
        y = round(random.uniform(y_min, y_max), 2)
        f.write(f"{i} {x} {y}\n")