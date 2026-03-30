"""
棋盤底層操作模組
管理 8x8 棋盤状態、棋子位置、捕獲等
"""

class Board:
    """棋盤管理類別"""
    
    BOARD_SIZE = 8
    EMPTY = "+"
    
    def __init__(self):
        """初始化棋盤"""
        self.grid = [[self.EMPTY for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self._init_pieces()
    
    def _init_pieces(self):
        """設置初始棋子位置"""
        # AB 方（上方）
        self.grid[0][0] = "A"
        self.grid[0][1] = "B"
        self.grid[1][0] = "c"
        self.grid[1][1] = "d"
        self.grid[0][2] = "e"
        self.grid[0][3] = "f"
        
        # UV 方（下方）
        self.grid[7][6] = "U"
        self.grid[7][7] = "V"
        self.grid[6][6] = "w"
        self.grid[6][7] = "x"
        self.grid[7][4] = "y"
        self.grid[7][5] = "z"
    
    def get_piece(self, row, col):
        """取得指定位置的棋子"""
        if self._is_valid_pos(row, col):
            return self.grid[row][col]
        return None
    
    def set_piece(self, row, col, piece):
        """設置指定位置的棋子"""
        if self._is_valid_pos(row, col):
            self.grid[row][col] = piece
    
    def is_empty(self, row, col):
        """檢查指定位置是否為空"""
        if self._is_valid_pos(row, col):
            return self.grid[row][col] == self.EMPTY
        return False
    
    def _is_valid_pos(self, row, col):
        """檢查位置是否在棋盤範圍內"""
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE
    
    def get_all_pieces(self, side):
        """取得某一方的所有棋子位置"""
        pieces = {}
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.grid[row][col]
                if piece != self.EMPTY and self._is_piece_of_side(piece, side):
                    pieces[(row, col)] = piece
        return pieces
    
    def _is_piece_of_side(self, piece, side):
        """判斷棋子是否屬於某一方"""
        if side == "AB":
            return piece in "ABcdef"
        elif side == "UV":
            return piece in "UVwxyz"
        return False
    
    def copy(self):
        """複製棋盤"""
        new_board = Board.__new__(Board)
        new_board.grid = [row[:] for row in self.grid]
        return new_board
    
    def __str__(self):
        """字串表示"""
        result = []
        for row in self.grid:
            result.append(" ".join(row))
        return "\n".join(result)
