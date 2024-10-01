def sum_of_list(numbers:list) -> int:
    '''
        This function takes in a list of numbers and return the sum of the numbers in the list
    '''
    sum = 0
    for i in numbers:
        sum += i
    return sum

def fibanacci(n:int) -> int:
    '''
        This function takes in a number n and returns the nth number in the fibanacci sequence
    '''
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibanacci(n-1) + fibanacci(n-2)


if __name__ == "__main__":
    list_f = [fibanacci(f) for f in range(10)]
    print(list_f)