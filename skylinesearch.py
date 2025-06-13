from tree_node_overflow import RTree
import matplotlib.pyplot as plt
import heapq
import time

data = []
with open("datasets/generated_city.txt", 'r') as file:
    headers = ["id", "x", "y"]
    for line in file:
        items = line.strip().split(" ")
        entry = {}
        for i in range(len(headers)):
            entry[headers[i]] = float(items[i])
        
        data.append(entry)

#########################################################################################################################################
###############---------------------- SEQUENTIAL SEARCH FUNCTIONS ------------------------------------------#############################
#########################################################################################################################################

def seq_search(input):
    skyline = []

    for p1 in input:
        dominated = False

        for p2 in input:

            if p1["id"] == p2["id"]:
                continue

            if is_dominating_point(p2, p1):
                dominated = True
                break

        if dominated == False:
            skyline.append(p1)

    return skyline

#########################################################################################################################################
###############---------------------- BRANCH AND BOUND SKYLINE FUNCTIONS------------------------------------#############################
#########################################################################################################################################

def is_dominating_point(p1, p2): # Always checks if p1 is dominant of p2

    if isinstance(p1, dict) and isinstance(p2, dict): # True if p1 and p2 is a point
        return (
            p1['x'] <= p2['x'] and p1['y'] >= p2['y'] and
            (p1['x'] < p2['x'] or p1['y'] > p2['y'])
        )
    
    if not isinstance(p1, dict):    # P1 is a parent node
        # Compare if node MBR dominates P2 
        mbr_x, mbr_y = p1.MBR['x1'], p1.MBR['y2']
        
        return(
            mbr_x <= p2['x'] and mbr_y >= p2['y'] and
            (mbr_x < p2['x'] or mbr_y > p2['y'])
        )
    
    if not isinstance(p2, dict):    # P2 is a parent node
        # Compare if p1 dominates node MBR
        mbr_x, mbr_y = p2.MBR['x1'], p2.MBR['y2']

        return(
            p1['x'] <= mbr_x and p1['y'] >= mbr_y and
            (p1['x'] < mbr_x or p1['y'] > mbr_y)
        )
    
    return False

def is_dominated(node, skyline: list): # Checks if a single point in skyline dominates node (input)

    if isinstance(node, dict): # node is data point
        dominated = False

        for s_point in skyline:

            if is_dominating_point(s_point, node): # if skyline point dominates node, break & return True
                dominated = True
                break

        if not dominated:
            return False # Skyline does NOT dominate node
        
    elif node.is_leaf(): # node is a leaf

        for point in node.data_points: # Multiple points in a leaf. Checks if one point in leaf dominates skyline.
            dominated = False 

            for s_point in skyline:

                if is_dominating_point(s_point, point): # check if sky point dominates point in node, break & next iteration.
                    dominated = True
                    break
                
            if not dominated:
                return False # Skyline does NOT dominate node

    else: # node is parent node
        dominated = False

        for s_point in skyline:
            
            if is_dominating_point(s_point, node): # if sky point dominates MBR of node, break and return True
                dominated = True
                break

        if not dominated:
            return False # Skyline does NOT dominate node

    return True

def dominant_leaf_points(node, skyline): # returns the leaf points that are not dominated by the skyline
    result = []
    
    for point in node.data_points:
        dominated = False

        for s_point in skyline:

            if is_dominating_point(s_point, point):
                dominated = True
            
            if dominated == True:
                break

        if dominated == False:
            result.append(point)

    return result

def clean_skyline(skyline): # Cleans skyline of any points that are dominated
    cleaned = []

    for x in skyline:
        if not is_dominated(x, skyline):
            cleaned.append(x)

    return cleaned

def BBS_skysearch(root):
    H = [] # H is a list of nodes to check
    heapq.heappush(H, [root.priority(), root]) # priority queue, storing nodes MBR and the node.
    skyline = [] # list of skyline points

    while H: # while H is not empty
        priority, current_node = heapq.heappop(H) # next node with the highest priority

        if current_node.is_leaf(): # is a Leaf
            dom_points = dominant_leaf_points(current_node, skyline)    # find dominant points in leaf
            for point in dom_points:
                skyline.append(point)                                       # Add dom points to skyline

            skyline = clean_skyline(skyline)                                # clean skyline

            continue
        else: # is a node
            for child in current_node.child_nodes: 
                if not is_dominated(child, skyline):                    # if child is not dominated
                    heapq.heappush(H, [child.priority(), child])            # add to queue
        
    return skyline

#########################################################################################################################################
###############---------------------- DIVIDE & CONQUER FUNCTIONS -------------------------------------------#############################
#########################################################################################################################################

def split_Data(data):
    max_x = None
    min_x = None

    for point in data:              # find min and max value of x
        x = point['x']
        
        if max_x == None:
            max_x = x
        
        if min_x == None:
            min_x = x

        if x > max_x:
            max_x = x

        if x < min_x:
            min_x = x
    
    midpoint = (max_x + min_x) / 2  # find midpoint by avg of max x and min x
    left = []
    right = []

    for point in data:              # Split into left and right by uding midpoint
        x = point ['x']

        if x <= midpoint:
            left.append(point)
        else:
            right.append(point)
    
    return left, right              # Return left and right as lists
    
def divide_and_conquer_skyline(root_L, root_R):
    L_skyline = BBS_skysearch(root_L)
    R_skyline = BBS_skysearch(root_R)
    max_y_L = None

    for point in L_skyline:
        y = point['y']

        if max_y_L == None:
            max_y_L = y
        
        if y > max_y_L:
            max_y_L = y
    
    filter_R = []

    for point in R_skyline:
        y = point['y']

        if y > max_y_L:
            filter_R.append(point)

    return L_skyline + filter_R

#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################

############################################## ----- SEQ SEARCH SLYLINE----- ############################################################
start_time_SSS = time.time()
skyline = seq_search(data)
end_time_SSS = time.time()

skyline.sort(key=lambda point: point["id"])
print()
print('skyline1: ', skyline)
print()

############################################## ----- BBS ALGO ----- ######################################################################
tree = RTree() # Construct an R-tree

for point in data: # Insert each point into the root node
    tree.insert(tree.root, point)

start_time_BBS = time.time()
skyline2 = BBS_skysearch(tree.root)
end_time_BBS = time.time()

skyline2.sort(key=lambda point: point["id"])
print()
print('Skyline2: ', skyline2)
print()


############################################## ----- DIVIDE & CONQUER ALGO ----- #########################################################
left, right = split_Data(data)

L_tree = RTree() # Construct an R-tree
R_tree = RTree()

for point in left: # Insert each point into the root node
    L_tree.insert(L_tree.root, point)

for point in right: # Insert each point into the root node
    R_tree.insert(R_tree.root, point)

start_time_DC = time.time()
skylineDC = divide_and_conquer_skyline(L_tree.root, R_tree.root)
end_time_DC = time.time()

skylineDC.sort(key=lambda point: point["id"])
print()
print('skylineDC: ', skylineDC)
print()

############################################## ----- SAVE OUTPUT ----- ####################################################################

with open("Seq_Search.txt", "w") as f:
    duration = f"SEQUENTIAL SEARCH \n{end_time_SSS - start_time_SSS} seconds\n"
    f.write(duration)
    for point in skyline:
        line = f"ID: {point['id']} X: {point['x']} Y: {point['y']}\n"
        f.write(line)

with open("BBS.txt", "w") as f:
    duration = f"BBS ALGO \n{end_time_BBS - start_time_BBS} seconds\n"
    f.write(duration)
    for point in skyline2:
        line = f"ID: {point['id']} X: {point['x']} Y: {point['y']}\n"
        f.write(line)

with open("Divide and Conquer.txt", "w") as f:
    duration = f"Divide and Conquer BBS ALGO \n{end_time_DC - start_time_DC} seconds\n"
    f.write(duration)
    for point in skylineDC:
        line = f"ID: {point['id']} X: {point['x']} Y: {point['y']}\n"
        f.write(line)

print(f"SEQ SEARCH completed in {end_time_SSS - start_time_SSS:.4f} seconds")
print(f"BBS completed in {end_time_BBS - start_time_BBS:.4f} seconds")
print(f"DC completed in {end_time_DC - start_time_DC:.4f} seconds")

# Extract x and y values
all_x = [d['x'] for d in data]
all_y = [d['y'] for d in data]

sky_x = [d['x'] for d in skyline2]
sky_y = [d['y'] for d in skyline2]

sky3_x = [pt['x'] for pt in skyline]
sky3_y = [pt['y'] for pt in skyline]

# Extract x and y for skylineDC
skyDC_x = [pt['x'] for pt in skylineDC]
skyDC_y = [pt['y'] for pt in skylineDC]

# Plotting all four
plt.figure(figsize=(12, 12))  # Adjusted to fit 4 plots

# 1st plot: all data
plt.subplot(2,2,1)
plt.scatter(all_x, all_y, color='gray', alpha=0.5)
plt.title("All Data (city1.txt)")
plt.xlabel("Price (x)")
plt.ylabel("Size (y)")
plt.grid(True)

# 2nd plot: first skyline
plt.subplot(2,2,2)
plt.scatter(sky_x, sky_y, color='blue')
plt.title("Seq Search")
plt.title(f"SS Completed in {end_time_SSS - start_time_SSS:.4f} seconds")
plt.xlabel("Price (x)")
plt.ylabel("Size (y)")
plt.grid(True)

# 3rd plot: second skyline
plt.subplot(2,2,3)
plt.scatter(sky3_x, sky3_y, color='green')
plt.title("Skyline BBS")
plt.title(f"BBS completed in {end_time_BBS - start_time_BBS:.4f} seconds")
plt.xlabel("Price (x)")
plt.ylabel("Size (y)")
plt.grid(True)

# 4th plot: divide-and-conquer skyline
plt.subplot(2,2,4)
plt.scatter(skyDC_x, skyDC_y, color='red')
plt.title("Skyline DC")
plt.title(f"DC completed in {end_time_DC - start_time_DC:.4f} seconds")
plt.xlabel("Price (x)")
plt.ylabel("Size (y)")
plt.grid(True)

plt.tight_layout()
plt.show()

print("✅ Whole Script ran successfully.")