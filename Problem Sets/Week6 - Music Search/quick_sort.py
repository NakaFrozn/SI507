import random
import timeit
import unittest

def quickSort(array:list):
    """
    Sorts a list of integers using the quick sort algorithm.

    Parameters
    ----------
    array : list
        The list of integers to be sorted.
    
    Returns
    -------
    list
        The sorted list of integers.
    """
    if len(array)<=1:
        return array
    pivot = array[len(array)//2]
    left = [x for x in array if x<pivot]
    middle = [x for x in array if x==pivot]
    right = [x for x in array if x>pivot]
    return quickSort(left) + middle + quickSort(right)

def ranDom(size, count, value):
    """
    Create a list of random numbers that includes a specified number of the same values.

    Parameters
    ----------
    size : int
        The total size of the list.
    same_value_count : int
        The number of times the same value should appear in the list.
    same_value : int
        The value that should appear multiple times in the list.

    Returns
    -------
    list
        The list of random numbers.
    """
    random_numbers = [random.randint(0, 1000) for _ in range(size - count)]
    random_numbers.extend([value] * count)
    random.shuffle(random_numbers)
    return random_numbers

def comment():
    comment = """
    We tried three sorting methods: bubble sort, merge sort and quick sort. In terms of the time complexity, merge sort and quick sort.
    Bubble sort is the easiest to implement but it is not time efficient and not applicable in large-scale data. Merge sort and quick sort has time complexity of O(n log n).
    However, merge sort has more constant factors than quick sort results in slower performance in large scale data. Quick sort on average is the most time-efficient method. 
    It also requires less memory space than merge sort (O(log n) vs O(n)). However, in a worst-case scenario, like choosing the minimum or maximum as the pivot, quick sort is not stable and time consuming(O(n^2)).
    """
    print(comment)

class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.array = ranDom(size=200000, count=100000, value=370)
        self.narray = ranDom(size=200000, count=100, value=370)
    def test_quickSort(self):
        self.assertEqual(quickSort(self.array), sorted(self.array))
        self.assertEqual(quickSort(self.narray), sorted(self.narray))


def main():
    # array = ranDom(size=200000, count=100000, value=370)
    # execution_time = timeit.timeit(lambda: quickSort(array), number=1)
    # print(f"Execution time: {execution_time:.2f} seconds")
    # array = ranDom(size=200000, count=100, value=370)
    # execution_time = timeit.timeit(lambda: quickSort(array), number=1)
    # print(f"Execution time: {execution_time:.2f} seconds")
    comment()

if __name__ == "__main__":
    # unittest.main(exit=False)
    main()