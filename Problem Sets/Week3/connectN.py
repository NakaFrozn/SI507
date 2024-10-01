from enum import Enum
import unittest


class Notation(Enum):
    """Enumeration for representing different types of notations in the game.

    Attributes:
        EMPTY (int): Represents an empty cell on the board.
        PLAYER1 (int): Represents a cell occupied by Player 1.
        PLAYER2 (int): Represents a cell occupied by Player 2.
    """

    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2


class Player:
    """Represents a player in the game.

    Attributes:
        __playerName (str): The name of the player.
        __playerNotation (Notation): The notation (symbol) used by the player on the board.
        __curScore (int): The current score of the player.

    Args:
        playerName (str): The name of the player.
        playerNotation (Notation): The notation (symbol) used by the player.
        curScore (int): The initial score of the player.
    """

    def __init__(self, playerName, playerNotation, curScore) -> None:
        self.__playerName = playerName
        self.__playerNotation = playerNotation
        self.__curScore = curScore

    def display(self) -> None:
        """Displays the player's details including name, notation, and current score."""
        print(
            f"Player: {self.__playerName}, Current Score: {self.__curScore}, Notation: {self.__playerNotation}, "
        )

    def addScoreByOne(self) -> None:
        """Increments the player's score by one."""
        self.__curScore += 1

    def getScore(self) -> int:
        """Returns the current score of the player."""
        return self.__curScore

    def getName(self) -> str:
        """Returns the name of the player."""
        return self.__playerName

    def getNotation(self) -> Notation:
        """Returns the notation used by the player."""
        return self.__playerNotation


class Board:
    """Represents the game board.

    Attributes:
        __rowNum (int): Number of rows in the board.
        __colNum (int): Number of columns in the board.
        __grid (list): 2D list representing the game board.

    Args:
        rowNum (int): Number of rows in the board.
        colNum (int): Number of columns in the board.
    """

    def __init__(self, rowNum, colNum) -> None:
        self.__rowNum = rowNum
        self.__colNum = colNum
        self.__grid = [[Notation.EMPTY for i in range(colNum)] for j in range(rowNum)]

    def initGrid(self) -> None:
        """Initializes the game board with empty cells."""
        self.__grid = [[Notation.EMPTY for i in range(self.__colNum)] for j in range(self.__rowNum)]

    def getColNum(self) -> int:
        """Returns the number of columns in the board."""
        return self.__colNum

    def placeMark(self, colNum, mark) -> bool:
        """Attempts to place a mark on the board at the specified column.

        Args:
            colNum (int): The column number where the mark is to be placed.
            mark (Notation): The mark to be placed on the board.

        Returns:
            bool: True if the mark was successfully placed, False otherwise.
        """
        if colNum < 0 or colNum >= self.__colNum:
            print("Error Move: Invalid column number.")
            return False
        if self.__grid[0][colNum] != Notation.EMPTY:
            print("Error Move: The column is full.")
            return False
        if mark == Notation.EMPTY:
            print("Error Move: Invalid notation.")
            return False
        for i in range(self.__rowNum - 1, -1, -1):  # iterate for the bottom to the top row
            if self.__grid[i][colNum] == Notation.EMPTY:
                self.__grid[i][colNum] = mark
                return True
        return False

    def checkFull(self) -> bool:
        """Checks if the board is completely filled.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        for i in range(self.__colNum):
            if self.__grid[0][i] == Notation.EMPTY:
                return False
        return True

    def display(self) -> None:
        """Displays the current state of the board."""
        boardStr = ""
        for row in self.__grid:
            for cell in row:
                if cell == Notation.EMPTY:
                    boardStr += "O"
                elif cell == Notation.PLAYER1:
                    boardStr += "R"
                elif cell == Notation.PLAYER2:
                    boardStr += "Y"
            boardStr += "\n"
        print(f"Current Board is:\n{boardStr}")

    # Private methods for internal use
    def __checkWinHorizontal(self, target) -> Notation | None:
        for row in self.__grid:
            for i in range(self.__colNum - target + 1):
                if all(cell == row[i] for cell in row[i : i + target]) and row[i] != Notation.EMPTY:
                    # Check if all cells in the row are the same and not empty
                    return row[i]
        return None

    def __checkWinVertical(self, target) -> Notation | None:
        for col in range(self.__colNum):
            for i in range(self.__rowNum - target + 1):
                if (
                    all(self.__grid[i][col] == self.__grid[j][col] for j in range(i, i + target))
                    and self.__grid[i][col] != Notation.EMPTY
                ):
                    # Check if all cells in the column are the same and not empty
                    return self.__grid[i][col]
        return None

    def __checkWinOneDiag(self, target, rowNum, colNum) -> Notation | None:
        for row in range(rowNum - target + 1):
            for col in range(colNum - target + 1):
                if (
                    all(
                        self.__grid[row + i][col + i] == self.__grid[row][col]
                        for i in range(target)
                    )
                    and self.__grid[row][col] != Notation.EMPTY
                ):
                    # The next cell in a right diagonal line is always (row+1, col+1)
                    # Check if all cells in the diagonal are the same and not empty
                    return self.__grid[row][col]
        return None

    def __checkWinAntiOneDiag(self, target, rowNum, colNum) -> Notation | None:
        for row in range(rowNum - target + 1):
            for col in range(colNum - target + 1):
                if (
                    all(
                        self.__grid[row - i][col + i] == self.__grid[row][col]
                        for i in range(target)
                    )
                    and self.__grid[row][col] != Notation.EMPTY
                ):
                    # The next cell in a left diagonal line is always (row-1, col+1)
                    # Check if all cells in the diagonal are the same and not empty
                    return self.__grid[row][col]
        return None

    def __checkWinDiagonal(self, target) -> Notation | None:
        return self.__checkWinOneDiag(
            target, self.__rowNum, self.__colNum
        ) or self.__checkWinAntiOneDiag(target, self.__rowNum, self.__colNum)

    def checkWin(self, target) -> Notation | None:
        """Checks if there is a winning condition on the board.

        Args:
            target (int): The number of consecutive marks needed for a win.

        Returns:
            Notation or None: The notation of the winning player, or None if there is no winner.
        """
        return (
            self.__checkWinHorizontal(target)
            or self.__checkWinVertical(target)
            or self.__checkWinDiagonal(target)
        )


class Game:
    """Represents the game logic and flow.

    Args:
        rowNum (int): Number of rows in the game board.
        colNum (int): Number of columns in the game board.
        connectN (int): Number of consecutive marks needed for a win.
        targetScore (int): The score a player needs to reach to win the game.
        playerName1 (str): Name of the first player.
        playerName2 (str): Name of the second player.
    """

    def __init__(self, rowNum, colNum, connectN, targetScore, playerName1, playerName2) -> None:
        self.__board = Board(rowNum, colNum)
        player1 = Player(playerName1, Notation.PLAYER1, 0)
        player2 = Player(playerName2, Notation.PLAYER2, 0)
        self.__playerList = [player1, player2]
        self.__curPlayer = player1
        self.__connectN = connectN
        self.__targetScore = targetScore

    def __playBoard(self, curPlayer) -> None:
        """Handles the process of a player making a move on the board.

        Args:
            curPlayer (Player): The current player who is making the move.
        """
        isPlaced = False
        while not isPlaced:
            colNum = input(
                f"{curPlayer.getName()}, please enter the column number you want to place: "
            )
            if colNum.isdigit() and 0 <= int(colNum) <= self.__board.getColNum():
                if colNum[0] == "0" and len(colNum) > 1:
                    print(
                        "Invalid column number. Please enter a valid number with no leading zeros."
                    )
                    continue
                else:
                    colNum = int(colNum)
                    self.__board.placeMark(colNum, curPlayer.getNotation())
                    isPlaced = True
            else:
                print("Invalid column number. Please enter a valid number.")
                continue

    def __changeTurn(self) -> None:
        """Switches the turn to the other player."""
        if self.__curPlayer == self.__playerList[0]:
            self.__curPlayer = self.__playerList[1]
        else:
            self.__curPlayer = self.__playerList[0]

    def playRound(self) -> None:
        """Plays a single round of the game."""
        curWinnerNotation = None
        self.__board.initGrid()
        self.__curPlayer = self.__playerList[0]
        print("Starting a new round!")
        while not curWinnerNotation:
            self.__curPlayer.display()  # display the current player's details
            self.__board.display()  # display the current state of the board
            self.__playBoard(self.__curPlayer)  # let current player make a move
            curWinnerNotation = self.__board.checkWin(
                self.__connectN
            )  # check if the current player wins with connecting N
            if curWinnerNotation:
                print(f"Congratulations! {self.__curPlayer.getName()} wins this round!!")
                self.__board.display()  # display the final state of the board
                self.__curPlayer.addScoreByOne()  # increment the winner's score
            elif self.__board.checkFull():  # check if the board is full
                print("The board is full. It's a tie!")
                break
            else:
                self.__changeTurn()  # switch to the other player

    def play(self) -> None:
        """Starts and manages the game play until a player wins."""
        while (
            self.__playerList[0].getScore() < self.__targetScore
            and self.__playerList[1].getScore() < self.__targetScore
        ):
            # Play a round of the game when both players' scores are less than the target score
            self.playRound()

        print("Game Over!")
        if self.__playerList[0].getScore() == self.__targetScore:
            print(f"Congratulations! {self.__playerList[0].getName()} wins the game!!")
        else:
            print(f"Congratulations! {self.__playerList[1].getName()} wins the game!!")
        for player in self.__playerList:
            player.display()


"""
############################## Homework ConnectN ##############################

% Student Name: Zhonghan Xie

% Student Unique Name: jonasxie

% Lab Section 00X: 

% I worked with the following classmates: N/A

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""


def main():
    """Main function to start the game."""
    game = Game(4, 4, 3, 2, "P1", "P2")
    game.play()


if __name__ == "__main__":
    main()
