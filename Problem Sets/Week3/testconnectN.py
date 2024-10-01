
class TestConnectN(unittest.TestCase):
    """Create a test case for the ConnectN game."""
    def setUp(self):
        self.game = Game(4, 4, 3, 2, 'P1', 'P2')
    def test_initGrid(self):
        # test the number of columns in the board
        self.game.__board.initGrid()
        self.assertEqual(self.game.__board.getColNum(), 4)
    def test_placeMark(self):
        # test placing a mark on the board
        self.game.__board.initGrid()
        self.assertTrue(self.game.__board.placeMark(1, Notation.PLAYER1))