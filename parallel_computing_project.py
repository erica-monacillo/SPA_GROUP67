import random
import time
from multiprocessing import Process, Queue

# --- 1. Dataset Generation ---

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

# --- 2. Sequential Sorting (Merge Sort) ---

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

