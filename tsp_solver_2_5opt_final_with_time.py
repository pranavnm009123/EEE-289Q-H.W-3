import sys
import math
import time
import random
import os

def read_graph(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    try:
        N = int(lines[0].strip())
    except ValueError:
        N = 1000 

    dist_matrix = [[0.0] * (N + 1) for _ in range(N + 1)]
    
    start_idx = 1
    if "Node1" in lines[1]:
        start_idx = 2
        
    for line in lines[start_idx:]:
        parts = line.strip().split()
        if len(parts) != 3:
            continue
        u, v, d = int(parts[0]), int(parts[1]), float(parts[2])
        dist_matrix[u][v] = d
        dist_matrix[v][u] = d
        
    return N, dist_matrix

def calculate_cost(path, dist_matrix):
    cost = 0.0
    for i in range(len(path) - 1):
        cost += dist_matrix[path[i]][path[i+1]]
    return cost

def nearest_neighbor(N, dist_matrix, start_node=1):
    unvisited = set(range(1, N + 1))
    unvisited.remove(start_node)
    path = [start_node]
    current = start_node
    
    while unvisited:
        nearest = None
        min_dist = float('inf')
        for neighbor in unvisited:
            d = dist_matrix[current][neighbor]
            if d < min_dist:
                min_dist = d
                nearest = neighbor
        current = nearest
        path.append(current)
        unvisited.remove(current)
    path.append(start_node)
    return path

def two_point_five_opt(path, dist_matrix, time_limit_seconds=29):
    best_path = path[:]
    best_cost = calculate_cost(best_path, dist_matrix)
    improved = True
    start_time = time.time()
    
    evaluated_cycles = 0
    N = len(path) - 1
    
    while improved:
        improved = False
        if time.time() - start_time > time_limit_seconds:
            break
            
        for i in range(1, N - 1):
            if time.time() - start_time > time_limit_seconds: break
            for j in range(i + 1, N):
                if time.time() - start_time > time_limit_seconds: break
                
                evaluated_cycles += 1
                
                A = best_path[i-1]
                B = best_path[i]
                C = best_path[j]
                D = best_path[j+1]
                
                d0 = dist_matrix[A][B] + dist_matrix[C][D]
                d1 = dist_matrix[A][C] + dist_matrix[B][D]
                
                if d1 < d0:
                    
                    best_path[i:j+1] = reversed(best_path[i:j+1])
                    best_cost -= (d0 - d1)
                    improved = True
                    break 
            if improved: break
        
        if improved: continue 
        
        for i in range(1, N):
            if time.time() - start_time > time_limit_seconds: break
            for j in range(1, N):
                if i == j or i == j + 1: continue
                
                evaluated_cycles += 1
                
                I_node = best_path[i]
                Pre_I = best_path[i-1]
                Post_I = best_path[i+1]
                
                J_node = best_path[j]
                Post_J = best_path[j+1]
                
                removed = dist_matrix[Pre_I][I_node] + dist_matrix[I_node][Post_I] + dist_matrix[J_node][Post_J]
                
                added = dist_matrix[Pre_I][Post_I] + dist_matrix[J_node][I_node] + dist_matrix[I_node][Post_J]
                
                if added < removed:
                    node = best_path.pop(i)
                    
                    if j < i:
                        best_path.insert(j+1, node)
                    else:
                        best_path.insert(j, node)
                        

                    best_cost = calculate_cost(best_path, dist_matrix)
                    improved = True
                    break
            if improved: break
            
    return best_path, best_cost, evaluated_cycles

def solve(filepath, time_budget=29):
    print(f"Processing {filepath}...")
    N, dist_matrix = read_graph(filepath)
    
    global_start_time = time.time()
    
    best_path = None
    best_cost = float('inf')
    total_evaluations = 0
    
    start_nodes = list(range(1, N + 1))
    random.shuffle(start_nodes)
    
    iteration = 0
    
    for start_node in start_nodes:
        if time.time() - global_start_time > time_budget:
            break
            
        iteration += 1
        

        path = nearest_neighbor(N, dist_matrix, start_node=start_node)
        
        remaining_time = time_budget - (time.time() - global_start_time)
        if remaining_time <= 0: break
        
        current_path, current_cost, evals = two_point_five_opt(path, dist_matrix, time_limit_seconds=remaining_time)
        total_evaluations += evals
        
        if current_cost < best_cost:
            best_cost = current_cost
            best_path = current_path
            print(f"  New Best Cost: {best_cost:.2f} (Iter {iteration}, Start Node {start_node})")
            
        current_elapsed = time.time() - global_start_time
        print(f"    -> Iter {iteration} done. Cost: {current_cost:.2f}. Total Time: {current_elapsed:.2f}s")
            
    elapsed = time.time() - global_start_time
    print(f"Final Cost: {best_cost:.2f}")
    print(f"Total Evaluated Cycles: {total_evaluations:.1e}")
    print(f"Time Taken: {elapsed:.2f} seconds")
    print(f"Iterations Completed: {iteration}")
    
    return best_path, best_cost, total_evaluations

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_A = os.path.join(base_dir, "TSP_1000_euclidianDistance.txt")
    file_B = os.path.join(base_dir, "TSP_1000_randomDistance.txt")
    
    print(f"Using input files:\n{file_A}\n{file_B}")

    print("--- Solving Graph A (2.5-opt) ---")
    path_A, cost_A, evals_A = solve(file_A, time_budget=60)
    
    print("\n--- Solving Graph B (2.5-opt) ---")
    path_B, cost_B, evals_B = solve(file_B, time_budget=60)
    

    final_sol_path = os.path.join(base_dir, "solution_925631538.txt")
    with open(final_sol_path, 'w') as f:
        if path_A:
            f.write(",".join(map(str, path_A)) + "\n")
        else:
            f.write("\n")
        if path_B:
            f.write(",".join(map(str, path_B)) + "\n")
        else:
            f.write("\n")
            
    print(f"\nDone{final_sol_path}")
    print(f"Graph A - Cost: {cost_A:.2f}, Cycles: {evals_A:.1e}")
    print(f"Graph B - Cost: {cost_B:.2f}, Cycles: {evals_B:.1e}")
