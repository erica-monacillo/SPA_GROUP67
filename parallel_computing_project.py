import random
import time
from multiprocessing import Process, Queue

#Dataset Generation

def generate_dataset(size, sorted_type=None):
    """
    Generates a list of random integers of a specified size.
    Optionally generates an already sorted or reverse sorted list.
    """
    data = [random.randint(1, 1000000) for _ in range(size)]
    if sorted_type == "sorted":
        data.sort()
    elif sorted_type == "reverse_sorted":
        data.sort(reverse=True)
    return data

#Sequential Sorting (Merge Sort) 

def merge_sort_sequential(arr):
    """
    Implements the sequential Merge Sort algorithm.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = merge_sort_sequential(left_half)
    right_half = merge_sort_sequential(right_half)

    return merge(left_half, right_half)

def merge(left, right):
    """
    Merges two sorted lists into a single sorted list.
    """
    merged = []
    left_idx, right_idx = 0, 0

    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            merged.append(left[left_idx])
            left_idx += 1
        else:
            merged.append(right[right_idx])
            right_idx += 1

    merged.extend(left[left_idx:])
    merged.extend(right[right_idx:])
    return merged

#Parallel Sorting (Parallel Merge Sort) 

def merge_sort_parallel_worker(arr, q):
    """
    Worker function for parallel merge sort. Sorts a chunk and puts it into a queue.
    """
    sorted_chunk = merge_sort_sequential(arr)
    q.put(sorted_chunk)

def merge_sort_parallel(data):
    """
    Implements the parallel Merge Sort algorithm using multiprocessing.
    Divides data into 4 chunks, sorts them in parallel, and merges the results.
    """
    chunk_size = len(data) // 4
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    if len(data) % 4 != 0:
        chunks[-1].extend(data[len(chunks) * chunk_size:])

    q = Queue()
    processes = []

    for chunk in chunks:
        p = Process(target=merge_sort_parallel_worker, args=(chunk, q))
        processes.append(p)
        p.start()
    sorted_chunks = []
    for _ in processes:
        sorted_chunks.append(q.get())

    for p in processes:
        p.join()

    final_sorted_list = []
    if sorted_chunks:
        final_sorted_list = sorted_chunks[0]
        for i in range(1, len(sorted_chunks)):
            final_sorted_list = merge(final_sorted_list, sorted_chunks[i])

    return final_sorted_list

#Sequential Searching (Linear Search)

def linear_search_sequential(arr, target):
    """
    Implements the sequential Linear Search algorithm.
    Returns the index of the target if found, otherwise -1.
    """
    for i, element in enumerate(arr):
        if element == target:
            return i
    return -1

#Parallel Searching (Parallel Linear Search)

def linear_search_parallel_worker(sub_data, target, q, offset):
    """
    Worker function for parallel linear search. Searches a sub-chunk and puts the global index into a queue.
    """
    for i, element in enumerate(sub_data):
        if element == target:
            q.put(offset + i)
            return
    q.put(-1)


def linear_search_parallel(data, target):
    """
    Implements the parallel Linear Search algorithm using multiprocessing.
    Divides data into 4 chunks, searches them in parallel, and returns the global index.
    """
    chunk_size = len(data) // 4
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

    if len(data) % 4 != 0:
        chunks[-1].extend(data[len(chunks) * chunk_size:])

    q = Queue()
    processes = []
    current_offset = 0

    for chunk in chunks:
        p = Process(target=linear_search_parallel_worker, args=(chunk, target, q, current_offset))
        processes.append(p)
        p.start()
        current_offset += len(chunk)

    results = []
    for _ in processes:
        results.append(q.get())

    for p in processes:
        p.join()

    for res in results:
        if res != -1:
            return res

    return -1

#Performance Testing 

def run_performance_test():
    """
    Runs performance tests for all algorithms across different dataset sizes and types.
    """
    dataset_sizes = {"Small": 1000, "Medium": 100000, "Large": 1000000}
    sorted_types = {"Random": None, "Sorted": "sorted", "Reverse Sorted": "reverse_sorted"}


    print("Performance Evaluation")


    for size_name, size in dataset_sizes.items():
        for sorted_type_name, sorted_type in sorted_types.items():
            print(f"\nDataset Size: {size_name} ({size} elements), Type: {sorted_type_name}")
            data = generate_dataset(size, sorted_type)

            #Sorting Tests
            print("  Sorting Algorithms:")

            #Sequential Merge Sort
            start_time = time.time()
            sorted_data_seq = merge_sort_sequential(list(data)) 
            end_time = time.time()
            print(f"    Sequential Merge Sort: {end_time - start_time:.6f} seconds")
    
            #Parallel Merge Sort
            start_time = time.time()
            sorted_data_par = merge_sort_parallel(list(data)) 
            end_time = time.time()
            print(f"    Parallel Merge Sort:   {end_time - start_time:.6f} seconds")
    
            #Searching Tests 
            print("  Searching Algorithms:")
            target_found = data[random.randint(0, size - 1)] if size > 0 else 1
            target_not_found = 1000001 


            #Sequential Linear Search (Target Found)
            start_time = time.time()
            index_seq_found = linear_search_sequential(data, target_found)
            end_time = time.time()
            print(f"    Sequential Linear Search (Found {target_found}): Index = {index_seq_found}, Time = {end_time - start_time:.6f} seconds")


            #Parallel Linear Search(Target Found)
            start_time = time.time()
            index_par_found = linear_search_parallel(data, target_found)
            end_time = time.time()
            print(f"    Parallel Linear Search (Found {target_found}): Index = {index_par_found}, Time = {end_time - start_time:.6f} seconds")


            #Sequential Linear Search (Target Not Found)
            start_time = time.time()
            index_seq_not_found = linear_search_sequential(data, target_not_found)
            end_time = time.time()
            print(f"    Sequential Linear Search (Not Found {target_not_found}): Index = {index_seq_not_found}, Time = {end_time - start_time:.6f} seconds")


            #Parallel Linear Search (Target Not Found)
            start_time = time.time()
            index_par_not_found = linear_search_parallel(data, target_not_found)
            end_time = time.time()
            print(f"    Parallel Linear Search (Not Found {target_not_found}): Index = {index_par_not_found}, Time = {end_time - start_time:.6f} seconds")


if __name__ == "__main__":
    run_performance_test()
