# SPA_GROUP67 GROUP ACTIVITY

# Parallel and Distributed Computing Project: Sequential vs Parallel Algorithms

This project compares the performance of sequential and parallel algorithms for sorting and searching using Python's `multiprocessing` module.

## Project Overview

The goal of this project is to explore the fundamental differences between sequential and parallel execution models. We implemented Merge Sort and Linear Search in both sequential and parallel forms and evaluated their performance across various dataset sizes.

### Team Members
- **ERICA MONACILLO** (Lead Developer + Documentation)
- **SHENE SUELO** (Algorithm Specialist)
- **RODRIGO ARRIBA** (Performance Analyst)
- **JOHN LUKE RODRIGO PANA** (Performance Check)

## Implementation Details

### 1. Sorting Algorithms
- **Sequential Merge Sort**: A standard recursive implementation of the merge sort algorithm.
- **Parallel Merge Sort**: The dataset is divided into 4 chunks. Each chunk is sorted independently in a separate process using the sequential merge sort. The sorted chunks are then merged sequentially to produce the final sorted list.

### 2. Searching Algorithms
- **Sequential Linear Search**: A simple iteration through the list to find the target element.
- **Parallel Linear Search**: The dataset is divided into 4 chunks. Each chunk is searched independently in a separate process. If a process finds the target, it returns the global index (calculated using an offset).

## Performance Evaluation

We tested the algorithms with three dataset sizes:
- **Small**: 1,000 elements
- **Medium**: 100,000 elements
- **Large**: 1,000,000 elements

We also included special cases for already sorted and reverse-sorted data.

### Key Observations
- **Sorting**: Parallel Merge Sort consistently outperformed Sequential Merge Sort for medium and large datasets. For small datasets, the overhead of process creation made the sequential version faster.
- **Searching**: Sequential Linear Search was often faster or comparable to Parallel Linear Search. This is because linear search is a very simple operation, and the overhead of managing multiple processes often outweighs the benefits of parallel execution for this specific task.

## Individual Reflections

### ERICA
The transition from sequential to parallel thinking was the most significant challenge. Implementing the parallel merge sort required careful handling of data partitioning and merging. I observed that while parallelism offers great potential for speedup, the overhead of process management is a critical factor, especially for smaller workloads.

### SHENE
Focusing on the "from scratch" implementation of Merge Sort was a great exercise. Ensuring the correctness of the merge logic was crucial before moving to the parallel version. I learned that parallelizing an algorithm isn't just about running things at the same time; it's about how you divide the work and combine the results efficiently.

### RODRIGO
Analyzing the performance data was eye-opening. The "Large" dataset clearly showed the benefits of parallel sorting, where the execution time was reduced by nearly 3x. However, the searching results reminded me that not every problem benefits from parallelism, as the overhead can sometimes make it slower than a simple sequential approach.

### LUKE
Testing the special cases (sorted and reverse-sorted) provided interesting insights. Merge sort's performance remained relatively stable regardless of the initial order, which is a key characteristic of the algorithm. I also focused on ensuring the global index was correctly calculated in the parallel search, which required careful offset management.

## How to Run
1. Ensure you have Python 3 installed.
2. Run the script:
   ```bash
   python3 parallel_computing_project.py
   ```
