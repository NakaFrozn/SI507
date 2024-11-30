# you may use pandas only for IO reason
# Using it to do sort will impact your grade
import csv
import random
import timeit
import unittest


def timeFunc(method):
    """
    Define the main body of the decorator that decorates a method.

    Returns
    -------
    Callable
        A wrapper that defines the behavior of the decorated method
    """

    def wrapper(*args, **kwargs):
        """
        Define the behavior of the decorated method
        Parameters:
            Same as the parameters used in the methods to be decorated

        Returns:
            Same as the objects returned by the methods to be decorated
        """
        start = timeit.default_timer()
        result = method(*args, **kwargs)
        # record the time consumption of executing the method
        time = timeit.default_timer() - start

        # send metadata to standard output
        print(f"Method: {method.__name__}")
        print(f"Result: {result}")
        print(f"Elapsed time of 10000 times: {time*10000} seconds")
        return result

    return wrapper


class MusicLibrary:
    def __init__(self):
        """
        Initialize the MusicLibrary object with default values.
        self.data the collect of music library
        self.rows: the row number
        self.cols: the col number
        self.nameIndex: the number represent the index of name in each element of self.data
        self.albumIndex: the number represent the index of album in each element of self.data
        self.trackIndex: the number represent the index of track in each element of self.data
        """
        self.data = []
        self.rows = 0
        self.cols = 0
        self.nameIndex = 0
        self.albumIndex = 1
        self.trackIndex = 2

    def readFile(self, fileName):
        """
        Read music data from a CSV file and store it in the self.data attribute.
        The self.rows and self.cols should be updated accordingly.
        The self.data should be [[name, albums count, tract count],...]
        You could assume the file is in the same directory with your code.
        Please research about the correct encoding for the given data set,
        as it is not UTF-8.
        You are allowed to use pandas or csv reader,
        but self.data should be in the described form above.

        Parameters
        ----------
        fileName : str
            The file name of the CSV file to be read.
        """
        with open(fileName, "r", encoding="ISO-8859-1") as file:
            reader = csv.reader(file)
            for row in reader:
                self.cols = len(row)
                row[1] = int(row[1])
                row[2] = int(row[2])
                self.data.append(row)
                self.rows += 1

    def printData(self):
        """
        Print the data attribute stored in the library instance in a formatted manner.
        """
        print("Artist Name, Album Count, Track Count")
        for row in self.data:
            print(f"{row[self.nameIndex]}, {row[self.albumIndex]}, {row[self.trackIndex]}")

    def shuffleData(self):
        """
        Shuffle the data stored in the library.
        refer to the random package
        """
        random.seed(42)
        random.shuffle(self.data)

    @timeFunc
    def binarySearch(self, key, keyIndex):
        """
        Perform a binary search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        low = 0
        high = len(self.data) - 1

        while low <= high:
            mid = (low + high) // 2
            if self.data[mid][keyIndex] == key:
                return mid
            elif self.data[mid][keyIndex] < key:
                low = mid + 1
            else:
                high = mid - 1

        return -1

    @timeFunc
    def seqSearch(self, key, keyIndex):
        """
        Perform a sequential search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        for i in range(len(self.data)):
            if self.data[i][keyIndex] == key:
                return i
        return -1

    @timeFunc
    def bubbleSort(self, keyIndex):
        """
        Sort the data using the bubble sort algorithm based on a specific column index.
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        n = len(self.data)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.data[j][keyIndex] > self.data[j + 1][keyIndex]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]

    def merge(self, L, R, keyIndex):
        """
        Merge two sorted sublists into a single sorted list.
        This is the helper function for merge sort.
        You may change the name of this function or even not have it.


        Parameters
        ----------
        L, R : list
            The left and right sublists to merge.
        keyIndex : int
            The column index to sort by.

        Returns
        -------
        list
            The merged and sorted list.
        """
        merged = []
        i = j = 0
        while i < len(L) and j < len(R):
            if L[i][keyIndex] < R[j][keyIndex]:
                merged.append(L[i])
                i += 1
            else:
                merged.append(R[j])
                j += 1
        while i < len(L):
            merged.append(L[i])
            i += 1
        while j < len(R):
            merged.append(R[j])
            j += 1
        return merged

    @timeFunc
    def mergeSort(self, keyIndex):
        """
        Sort the data using the merge sort algorithm.
        This is the main mergeSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        arr = self.data
        self.data = self._mergeSort(arr, keyIndex)

    def _mergeSort(self, arr, keyIndex):

        # This is the helper function for merge sort.
        # You may change the name of this function or even not have it.
        # This is a helper method for mergeSort
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self._mergeSort(arr[:mid], keyIndex)
        right = self._mergeSort(arr[mid:], keyIndex)
        return self.merge(left, right, keyIndex)

    @timeFunc
    def quickSort(self, keyIndex):
        """
        Sort the data using the quick sort algorithm.
        This is the main quickSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        # Implementation details...
        self.data = self._quickSort(self.data, keyIndex)

    def _quickSort(self, arr, keyIndex):
        # This is a helper method for quickSort
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2][keyIndex]
        left = [x for x in arr if x[keyIndex] < pivot]
        middle = [x for x in arr if x[keyIndex] == pivot]
        right = [x for x in arr if x[keyIndex] > pivot]
        return self._quickSort(left, keyIndex) + middle + self._quickSort(right, keyIndex)

    def comment(self):
        """
        Based on the result you find about the run time of calling different function,
        Write a small paragraph (more than 50 words) about time complexity, and print it.
        """
        comment = """
        The time complexity of sequential search is O(n) because it iterates the whole list to find the match. 
        The time complexity of binary search is O(log n) because it halves the list every time to find the match. 
        In the case of finding the match at the beginning of the list, e.g. finding "30 Seconds To Mars", the sequential sort is sometimes faster.
        So that sometimes you can't really say binary search is always faster than sequential search. It depends on the data and the key you are going to sort. But on average cases, binary search is faster and more efficient.
        The time complexity of bubble sort is O(n^2) because it has two iterates and both iterate the list nearly to n times. If the data is already sorted, the time complexity of bubble sort decreases to O(n).
        The time complexity of merge sort and quick sort are all O(n log n). Merge sort divides the list into half iteratively each time and merges the list. Quick sort divides the list into two parts and sorts them separately.
        Though both methods have the same time complexity, quick sort is faster than merge sort. Merge sort requires more time when merging two sorted lists than partitioning in the quick sort."""
        print(comment)

# create instance and call the following instance method
# using decroator to decroate each instance method
        
class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.myLibrary = MusicLibrary()
        filePath = "music.csv"
        self.myLibrary.readFile(filePath)
        self.myLibrary.shuffleData()
        data = self.myLibrary.data
    def test_quickSort0(self):
        self.myLibrary.quickSort(keyIndex=0)
        self.assertEqual(self.myLibrary.data, sorted(self.myLibrary.data, key=lambda x: x[0]))
    def test_quickSort1(self):
        self.myLibrary.quickSort(keyIndex=1)
        self.assertEqual(self.myLibrary.data, sorted(self.myLibrary.data, key=lambda x: x[1]))
    def test_quickSort2(self):
        self.myLibrary.quickSort(keyIndex=2)
        self.assertEqual(self.myLibrary.data, sorted(self.myLibrary.data, key=lambda x: x[2]))

def main():
    random.seed(42)
    myLibrary = MusicLibrary()
    filePath = "music.csv"
    myLibrary.readFile(filePath)
    myLibrary.shuffleData()

    idx = 0
    myLibrary.data.sort(key=lambda data: data[idx])
    myLibrary.seqSearch(key="30 Seconds To Mars", keyIndex=idx)
    myLibrary.binarySearch(key="30 Seconds To Mars", keyIndex=idx)

    myLibrary.seqSearch(key="Oasis", keyIndex=idx)
    myLibrary.binarySearch(key="Oasis", keyIndex=idx)

    idx = 2
    myLibrary.shuffleData()
    myLibrary.bubbleSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.quickSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.mergeSort(keyIndex=idx)
    myLibrary.printData()
    myLibrary.comment()

    myLibrary.quickSort(keyIndex=1)
    myLibrary.printData()

if __name__ == "__main__":
    #unittest.main()
    main()
