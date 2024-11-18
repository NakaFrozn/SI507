# from lzma import is_check_supported
# from tkinter import YES
# from xarray import corr


class TwentyQuestions:
    def __init__(self):
        """
        Initialize the TwentyQuestions class with predefined small and medium trees.
        Sets the current tree to the small tree by default.
        """
        self.smallTree = (
            "Is it bigger than a breadbox?",
            ("an elephant", None, None),
            ("a mouse", None, None),
        )
        self.mediumTree = (
            "Is it bigger than a breadbox?",
            ("Is it gray?", ("an elephant", None, None), ("a tiger", None, None)),
            ("a mouse", None, None),
        )
        self.currentTree = self.smallTree  # Default tree

    def inputChecker(self, userIn: str) -> bool:
        """
        aka(yes(userIn))
        Check if the user's input is an affirmative response.

        Parameters
        ----------
        userIn : str
            The input string from the user.

        Returns
        -------
        bool
            True if the input is an affirmative response ('y', 'yes', 'yup', 'sure'), else False.
        """

        affirmative = ["y", "yes", "yup", "sure"]
        return userIn.strip().lower() in affirmative

    def checkIfLeaf(self, curNode) -> bool:
        """
        Determine if the given node is a leaf node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the node is a leaf (both children are None), else False.
        """

        return (curNode[1] is None and curNode[2] is None)

    def simplePlay(self, curNode) -> bool:
        """
        Conduct a simple play through of the game using the current node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        bool
            True if the player successfully guesses the item, else False.
        """
        if self.checkIfLeaf(curNode):
            print(f"Is it {curNode[0]}?")
            return self.inputChecker(input())
        else:
            print(curNode[0])
            answer = input()
            if self.inputChecker(answer):
                return self.simplePlay(curNode[1])
            else:
                return self.simplePlay(curNode[2])

    def createNode(self, userQuestion: str, userAnswer: str, isCorrectForQues: bool, curNode: tuple) -> tuple:
        """
        Create a new node in the decision tree.

        Parameters
        ----------
        userQuestion : str
            The question to differentiate the new answer from the current node.
        userAnswer : str
            The answer provided by the user.
        isCorrectForQues : bool
            True if the userAnswer is the correct response to the userQuestion.
        curNode : tuple
            The current node in the decision tree at which the game has arrived. 
            This node typically represents the point in the game 
            where the player's guess was incorrect, 
            and a new question-answer pair needs to be 
            added to refine the tree. 


        Returns
        -------
        tuple
            The new node created with the user's question and answer 
            and curNode
        """
            
        if isCorrectForQues:
            return (userQuestion, (userAnswer, None, None), curNode)
        else:
            return (userQuestion, curNode, (userAnswer, None, None))

    def playLeaf(self, curNode) -> tuple:
        """
        Handle gameplay when a leaf node is reached in the decision tree. This method is called when 
        the game's traversal reaches a leaf node, indicating a guess at the player's thought. 
        If the guess is incorrect, the method will
        1. prompts the player for the correct answer 
        2. prompts the player for a distinguishing question
        3. ask user what is the answer for the new input item to this distinguishing question(refer the io result of play in the homework doc)
           notice the node should follow (tree question, (node for answer yes), (node for answer no))
        4. creating a new node in the tree for future gameplay. It should call self.createNode(...)

        Parameters
        ----------
        curNode : tuple
            The current leaf node in the decision tree. A leaf node is represented as a tuple with the guessed 
            object as the first element and two `None` elements, signifying that it has no further branches.

        Returns
        -------
        tuple
            The updated node based on user input. If the player's response indicates that the initial guess was 
            incorrect, this method returns a new node that includes the correct answer and a new question 
            differentiating it from the guessed object. If the guess was correct, it simply returns the unchanged 
            `curNode`.
        
        Notes
        -----
        The method interacts with the player to refine the decision tree. It's a crucial part of the learning 
        aspect of the game, enabling the tree to expand with more nuanced questions and answers based on 
        player feedback.
        """
        print(f"Is it {curNode[0]}?")
        if not self.inputChecker(input()):
            print("What should be the correct answer?")
            user_answer = input().strip()
            print("What question would distinguish your answer from the incorrect guess?")
            user_question = input()
            print(f"Is {user_answer} the correct answer for {user_question}? (Yes/No)")
            is_correct = self.inputChecker(input())
            return self.createNode(user_question, user_answer, is_correct, curNode)
        else:
            return curNode



    def play(self, curNode) -> tuple:
        """
        Conduct gameplay starting from the given node.

        Parameters
        ----------
        curNode : tuple
            The current node in the decision tree.

        Returns
        -------
        tuple
            The updated tree after playing from the given node.
        """
        if self.checkIfLeaf(curNode):
            return self.playLeaf(curNode)
        else:
            print(curNode[0])
            if self.inputChecker(input()):
                return (curNode[0], self.play(curNode[1]), curNode[2])
            else:
                return (curNode[0], curNode[1], self.play(curNode[2]))

    def playRound(self) -> None:
        """
        Execute a single round of the game, starting from the current state of the currentTree attribute. This method 
        calls the 'play' method to navigate through the tree. It then updates the 'currentTree' 
        attribute with the potentially modified tree resulting from this round of gameplay.

  
        Returns
        -----
        None
        """
        self.currentTree = self.play(self.currentTree)


    def saveTree(self, node, treeFile) -> None:
        """
        Recursively save the decision tree to a file.

        Parameters
        ----------
        node : tuple
            The current node in the decision tree.
        treeFile : _io.TextIOWrapper
            The file object where the tree is to be saved.
        """
        if node is None:
            treeFile.write("None\n")
        else:
            if self.checkIfLeaf(node):
                treeFile.write(f"Leaf\n{node[0]}\n")
            else:
                treeFile.write(f"Internal node\n{node[0]}\n")
                self.saveTree(node[1], treeFile)
                self.saveTree(node[2], treeFile)

    def saveGame(self, treeFileName) -> None:
        """
        Save the current state of the game's decision tree to a specified file. This method opens the file 
        with the given filename and writes the structure of the current decision tree to it. The tree is saved 
        in a txt format.

        The method uses the 'saveTree' function to perform the recursive traversal and writing of the tree 
        structure. Each node of the tree is written to the file with its type ('Leaf' or 'Internal node') 
        followed by its content (question or object name). 

        Important: the format of the txt file should be exactly the same as the ones in our doc to pass the autograder. 
        
        Parameters
        ----------
        treeFileName : str
            The name of the file where the current state of the decision tree will be saved. The file will be 
            created or overwritten if it already exists.

        """
        with open(treeFileName, "w") as treeFile:
            self.saveTree(self.currentTree, treeFile)


    def loadTree(self, treeFile) -> tuple:
        """
        Recursively read a binary decision tree from a file and reconstruct it.

        Parameters
        ----------
        treeFile : _io.TextIOWrapper
            An open file object to read the tree from.

        Returns
        -------
        tuple
            The reconstructed binary tree.
        """
        line = treeFile.readline().strip()
        if line == "None":
            return None
        elif line == "Leaf":
            return (treeFile.readline().strip(), None, None)
        else:
            return (treeFile.readline().strip(), self.loadTree(treeFile), self.loadTree(treeFile))

    def loadGame(self, treeFileName) -> None:
        """
        Load the game state from a specified file and update the current decision tree. This method opens the 
        file with the given filename and reconstructs the decision tree based on its contents. 

        The method employs the 'loadTree' function to perform recursive reading of the tree structure from the 
        file. Each node's type ('Leaf' or 'Internal node') and content (question or object name) are read and 
        used to reconstruct the tree in memory. This restored tree becomes the new 'self.currentTree' of the game.

        Parameters
        ----------
        treeFileName : str
            The name of the file from which the game state will be loaded. The file should exist and contain a 
            previously saved decision tree.

        """
        with open(treeFileName, "r") as treeFile:
            self.currentTree = self.loadTree(treeFile)


    def printTree(self):
        self._printTree(tree = self.currentTree)

    def _printTree(self, tree, prefix = '', bend = '', answer = ''):
        """Recursively print a 20 Questions tree in a human-friendly form.
        TREE is the tree (or subtree) to be printed.
        PREFIX holds characters to be prepended to each printed line.
        BEND is a character string used to print the "corner" of a tree branch.
        ANSWER is a string giving "Yes" or "No" for the current branch."""
        text, left, right = tree
        if left is None  and  right is None:
            print(f'{prefix}{bend}{answer}It is {text}')
        else:
            print(f'{prefix}{bend}{answer}{text}')
            if bend == '+-':
                prefix = prefix + '| '
            elif bend == '`-':
                prefix = prefix + '  '
            self._printTree(left, prefix, '+-', "Yes: ")
            self._printTree(right, prefix, '`-', "No:  ")

def main():
    """
    The main function for the 20 Questions game. This function initializes the game,
    allows the user to load a saved game, plays multiple rounds of the game, and
    prompts the user to save the game state at the end.
    """

    print("Welcome to 20 Questions!")
    game = TwentyQuestions()

    # Check if the user wants to load a saved game
    load = game.inputChecker(input("Do you want to load from a saved game? (Yes/No) "))
    if load:
        filename = input("Enter the name of the file: ").strip()
        game.loadGame(filename)
    else:
        print("Starting a new game!")

    # Start a loop to play multiple rounds
    while True:
        game.playRound()
        print("Do you want to play again?")
        if not game.inputChecker(input()): # If the user doesn't want to play again, break the loop
            break
    
    # Check if the user wants to save the game
    save = game.inputChecker(input("Do you want to save the game? (Yes/No) "))
    if save:
        filename = input("Enter the name of the file: ").strip()
        game.saveGame(filename)
        print(f"Game saved to {filename}")
    print("Thanks for playing!")

if __name__ == '__main__':
    main()

"""
############################## Homework 20questions ##############################

% Student Name: Zhonghan Xie

% Student Unique Name: jonasxie

% Lab Section 00X:  004

% I worked with the following classmates: NA

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""