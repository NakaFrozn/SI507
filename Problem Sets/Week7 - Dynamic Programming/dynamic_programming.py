import math

def change(amount:int, coins:list[int]) -> int:
    """
    Given an amount and a list of coins, return the number of ways to make change for the amount.
    
    Parameters
    ----------
    amount : int
        The amount of money to make change for.
    coins : list[int]
        A list of coin denominations.
    
    Returns
    -------
    int
        The coins needed to make change for the amount.
        When there is no solution, returns math.inf.
    """
    if amount == 0:
        return 0
    
    if amount < 0 or len(coins) == 0:
        return math.inf
    
    dp = [math.inf] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i-coin]+1)
    
    return dp[amount]

def giveChange(amount:int, coins:list[int]) -> tuple[int, list[int]]:
    """
    This function takes in the amount of money and the denominations of coins. Then returns the minimum number of coins needed and the coins.

    Parameters
    ----------
    amount : int
        The amount of money to make change for.
    coins : list[int]
        A list of coin denominations.
    
    Returns
    -------
    tuple[int, list[int]]
        The minimum number of coins needed and the coins.
        When there is no solution, returns math.inf.
    """
    dp = [[math.inf,[]] for _ in range(amount+1)]
    dp[0] = [0, []]
    if amount == 0:
        return dp[0]
    if amount < 0:
        return [math.inf, []]
    for coin in coins:
        for i in range(coin, amount+1):
            if dp[i-coin][0] + 1 < dp[i][0]:
                dp[i][0] = dp[i-coin][0] + 1
                dp[i][1] = dp[i-coin][1] + [coin]
    return dp[amount]