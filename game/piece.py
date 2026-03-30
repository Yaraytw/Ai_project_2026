"""
棋子移動規則和得分計算模組
定義各類棋子的移動方式、最大步數、得分等
"""

class Piece:
    """棋子規則定義"""
    
    # 棋子屬性  {棋子: (方向類型, 最大步數, 得分, 所屬方)}
    PIECE_RULES = {
        # AB 方
        "A": ("orthogonal", 2, 3, "AB"),
        "B": ("diagonal", 2, 3, "AB"),
        "c": ("orthogonal", 1, 1, "AB"),
        "d": ("orthogonal", 1, 1, "AB"),
        "e": ("diagonal", 1, 1, "AB"),
        "f": ("diagonal", 1, 1, "AB"),
        # UV 方
        "U": ("orthogonal", 2, 3, "UV"),
        "V": ("diagonal", 2, 3, "UV"),
        "w": ("orthogonal", 1, 1, "UV"),
        "x": ("orthogonal", 1, 1, "UV"),
        "y": ("diagonal", 1, 1, "UV"),
        "z": ("diagonal", 1, 1, "UV"),
    }
    
    # 棋子價值（用於評估函數）
    PIECE_VALUE = {
        "A": 4, "B": 4, "c": 1.5, "d": 1.5, "e": 1.5, "f": 1.5,
        "U": 4, "V": 4, "w": 1.5, "x": 1.5, "y": 1.5, "z": 1.5,
    }
    
    # 方向定義
    ORTHOGONAL_DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # 右左下上
    DIAGONAL_DIRS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # 右下、左下、右上、左上
    
    @staticmethod
    def get_moves(piece, row, col, board):
        """
        獲取指定棋子的所有合法移動
        
        Args:
            piece: 棋子（如 'A', 'b', 'U' 等）
            row, col: 棋子當前位置
            board: 棋盤對象
        
        Returns:
            list: [(目標row, 目標col), ...] 的列表
        """
        if piece not in Piece.PIECE_RULES:
            return []
        
        piece_type, max_steps, _, _ = Piece.PIECE_RULES[piece]
        moves = []
        
        if piece_type == "orthogonal":
            dirs = Piece.ORTHOGONAL_DIRS
        else:  # diagonal
            dirs = Piece.DIAGONAL_DIRS
        
        for dr, dc in dirs:
            for step in range(1, max_steps + 1):
                target_row = row + dr * step
                target_col = col + dc * step
                
                # 檢查是否超出棋盤
                if not (0 <= target_row < 8 and 0 <= target_col < 8):
                    break
                
                target_piece = board.get_piece(target_row, target_col)
                
                # 空格可以移動
                if target_piece == "+":
                    moves.append((target_row, target_col))
                else:
                    # 遇到棋子，如果是對手可以吃，但不能跨過
                    if not Piece._same_side(piece, target_piece):
                        moves.append((target_row, target_col))
                    break  # 無論如何都要停止
        
        return moves
    
    @staticmethod
    def _same_side(piece1, piece2):
        """判斷兩個棋子是否同方"""
        if piece1 == "+" or piece2 == "+":
            return False
        side1 = Piece.PIECE_RULES[piece1][3]
        side2 = Piece.PIECE_RULES[piece2][3]
        return side1 == side2
    
    @staticmethod
    def get_points(piece):
        """獲取棋子的獵殺得分"""
        return Piece.PIECE_RULES.get(piece, (None, None, 0, None))[2]
    
    @staticmethod
    def get_value(piece):
        """獲取棋子的評估價值"""
        return Piece.PIECE_VALUE.get(piece, 0)
    
    @staticmethod
    def get_side(piece):
        """獲取棋子所屬方"""
        if piece == "+":
            return None
        return Piece.PIECE_RULES.get(piece, (None, None, None, None))[3]
