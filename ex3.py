"""
In lines 43-95, this C function list_resize is part of the Python C API and is used to resize a Python list 
object. The function takes two parameters, a pointer to the list to be resized and the new size for the list.
The strategy used to grow arrays when full, is to over-allocate the memory. This is done to reduce the number
of reallocations. When analyzing the line of code on line 70 (new_allocated = ((size_t)newsize + (newsize >> 3) + 6) & ~(size_t)3;), 
the function calculates the new allocation size plus one eighth of the new size this is determined by >>3, so newsize/8 
and add the existing size 1. Therefore the growth factor is approxiately 1.125. 

"""
import timeit
import sys
import matplotlib.pyplot as plt

def list_capacity(lst):
    """Get capacity of list."""
    return (sys.getsizeof(lst) - 40) // 8

# Find the size S that causes the list to expand
lst = []
last_capacity = 0
S = 0
for i in range(64):
    lst.append(i)
    capacity = list_capacity(lst)
    if capacity != last_capacity:
        S = i
        last_capacity = capacity

# Measure the time it takes to append an element to a list of size S
times_S = timeit.repeat(stmt='lst.append(None)', setup='lst = [None] * S', repeat=1000, number=1, globals=globals())

# Measure the time it takes to append an element to a list of size S-1
times_S_minus_1 = timeit.repeat(stmt='lst.append(None)', setup='lst = [None] * (S-1)', repeat=1000, number=1, globals=globals())

# Plot the distribution of the timings
plt.hist(times_S, bins=30, alpha=0.5, label='Size S to S+1', edgecolor='black')
plt.hist(times_S_minus_1, bins=30, alpha=0.5, label='Size S-1 to S', edgecolor='black')
plt.title('Distribution of timings to grow a list')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency')
plt.legend(loc='upper right')
plt.show()

'''
When growing the array from S to S+1, essesntially we are adding a new element to the array. This will require new memory allocation,
then copyig all the elements from the old array to the new array, then adding the new element. When growing an array from S-1 to S,
we are adding a new element to the end of the array, which does not require new memeory to be allocated. Therefore the difference
is due to the time that it takes to allocate the new memeory and copy the existing elements when growing from S to S+1. 
'''
