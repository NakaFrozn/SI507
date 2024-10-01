import math

def change(amount:int, coins:list):
    """
    Calculate the minimum number of coins needed to make change for the given amount.

    Parameters:
    amount: int
        the amount of money to make change for
    coins: list
        the list of coins available to make change
    
    Returns:
    int or math.inf
        the minimum number of coins needed to make change for the given amount
        if it is impossible to make change for the given amount, return math.inf
    """

    if amount == 0:
        return 0
    elif amount < 0:
        return math.inf
    else:
        min_coins = math.inf
        for coin in coins:
            num_coins = change(amount - coin, coins)
            if num_coins != math.inf:
                min_coins = min(min_coins, num_coins + 1)
        return min_coins

def giveChange(amount:int, coins:list) -> list:
    """
    Print the minimum number of coins needed to make change for the given amount. And print the optimal coins combination.
    
    Parameters:
    amount: int
        the amount of money to make change for
    coins: list
        the list of coins available to make change
    
    Returns:
        list
        the optimal coins combination: [number of coins, list of coins used]
    """

    if amount == 0:
        return [0, []]
    elif amount < 0:
        return [math.inf, []]
    else:
        min_coins = [math.inf, []]
        for coin in coins:
            num_coins = giveChange(amount - coin, coins)
            if num_coins[0] != math.inf and num_coins[0] + 1 < min_coins[0]:
                min_coins = [num_coins[0] + 1, num_coins[1] + [coin]]
        return min_coins

if __name__ == "__main__":
    print(change(48, [1, 5, 10, 25, 50]))