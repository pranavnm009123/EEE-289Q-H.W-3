# TSP Solver (2.5-opt)

This project implements a Traveling Salesman Problem (TSP) solver using the **2.5-opt** heuristic, which combines the standard 2-opt local search with Vertex Insertion (1-shift) to escape local optima.

## Problem Description

Our goal is to solve the Traveling Salesman Problem by finding the cheapest loop that visits every node once, optimizing for the best result possible within a strict one-minute runtime. We evaluate this approach on two 1000-node datasets:
-   **Graph A**: Nodes are 2D coordinates, where cost is the physical (Euclidean) distance between them.
-   **Graph B**: Edge costs are just random numbers selected from the range [0, 100].

## Files

-   `tsp_solver_2_5opt_final_with_time.py`: The main solver script. It reads the input files, runs the 2.5-opt algorithm, and generates the solution file.
-   `solution_925631538.txt`: The output file containing the best found paths for both graphs.
-   `TSP_1000_euclidianDistance.txt`: Input graph with Euclidean distances.
-   `TSP_1000_randomDistance.txt`: Input graph with random distances.

## Algorithm Description

We applied a unified algorithmic strategy to handle both Graph A (Euclidean geometry) and Graph B (random weights). The solution is generated in two distinct phases:

### Step 1: Building the Initial Solution
We generate the initial tour using the **Nearest Neighbor** method. Starting from an arbitrary node, the algorithm greedily selects the nearest unvisited neighbor as the next step in the path. This process repeats until every node is included, after which the last node connects back to the first to form a closed loop. Because the quality of this path depends heavily on the starting point, the code runs this procedure multiple times with different start nodes within the time limit to find the best possible baseline.

### Step 2: Improving the Tour (2.5-opt)
After the initial tour is built, we refine it using a greedy local search algorithm called **2.5-opt**. This technique combines two powerful moves to reduce the total distance:
-   **2-opt Moves**: We check if reversing a section of the path (effectively swapping two edges) will result in a shorter total distance.
-   **Node Insertion**: We check if taking a single node out and dropping it into a different spot in the tour will reduce the cost.

Critically, the algorithm is designed to be "greedy." This means it does not wait to find the best possible move; instead, it accepts the very first improvement it finds and immediately restarts the search from that new, better configuration. The process stops only when the solution cannot be improved further or the time budget runs out.

## Usage

To run the solver, execute the following command in your terminal:

```bash
python3 tsp_solver_2_5opt_final_with_time.py
```

## Output

The script will output the progress to the console, including the best cost found so far.

Upon completion, it creates `solution_925631538.txt` with the following format:
-   Line 1: Comma-separated list of node IDs for the Euclidean graph path.
-   Line 2: Comma-separated list of node IDs for the Random graph path.

## Performance Results

All experiments were run under a strict 1-minute time limit per graph.

### Graph A (Euclidean Distance)
-   **Best cycle cost found**: ~2451.81
-   **Number of checked cycles**: ~3e8
-   **Time taken**: 60.00 seconds
-   **Algorithm**: NN+2.5OPT

### Graph B (Random Distance)
-   **Best cycle cost found**: ~377.03
-   **Number of checked cycles**: ~3e8
-   **Time Taken**: 60.00 seconds
-   **Algorithm**: NN+2.5OPT

## Constraints

-   **Time Limit**: The solver is hardcoded to stop optimizing each graph after approximately **60 seconds**.
-   **Input Format**: Expects standard TSP input files where the first line is the number of nodes, followed by node coordinates or distance entries.

## Requirements

-   Python 3.x
-   Standard Python libraries: `sys`, `math`, `time`, `random`, `os`
