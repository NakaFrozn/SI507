def fib(n):
    fib_seq = [0, 1]
    for i in range(2, n):
        fib_seq.append(fib_seq[i - 2] + fib_seq[i - 1])
    return fib_seq[-1]

print (fib(200000)) # start with 100000 and increase until it's annoying