"""
玩家模組
包含 HumanPlayer（人類玩家）和 RandomAI（隨機 AI）
"""

import random
from utils.timer import Timer
from game.piece import Piece


class Player:
    """玩家基類"""
    
    def __init__(self, side):
        """
        初始化玩家
        
        Args:
            side: "AB" 或 "UV"
        """
        self.side = side
        self.timer = Timer()
    
    def choose_move(self, state):
        """
        選擇一步棋
        
        Args:
            state: GameState 對象
        
        Returns:
            (src, dst): ((row, col), (row, col))
            None: 玩家放棄或出錯
        """
        raise NotImplementedError
    
    def timed_move(self, state):
        """
        在計時的情況下進行移動
        
        Returns:
            (src, dst, elapsed): ((row, col), (row, col), 耗時秒數)
            None: 移動失敗
        """
        self.timer.start()
        move = self.choose_move(state)
        elapsed = self.timer.stop()
        
        if move is None:
            return None
        
        src, dst = move
        return (src, dst, elapsed)


class HumanPlayer(Player):
    """人類玩家"""
    
    def choose_move(self, state):
        """
        人類玩家選擇移動
        """
        while True:
            try:
                move_str = input(f"請輸入 {self.side} 方的移動 (e.g., 0,0,0,1): ").strip()
                
                if move_str.lower() == "quit":
                    return None
                
                parts = move_str.split(",")
                if len(parts) != 4:
                    print("格式錯誤，請輸入 src_row,src_col,dst_row,dst_col")
                    continue
                
                src_row, src_col, dst_row, dst_col = map(int, parts)
                
                # 驗證移動
                piece = state.board.get_piece(src_row, src_col)
                if piece == "+" or Piece.get_side(piece) != self.side:
                    print("該位置沒有你方的棋子")
                    continue
                
                valid_moves = Piece.get_moves(piece, src_row, src_col, state.board)
                if (dst_row, dst_col) not in valid_moves:
                    print("非法移動")
                    continue
                
                return ((src_row, src_col), (dst_row, dst_col))
            
            except ValueError:
                print("輸入必須為整數")
                continue


class RandomAI(Player):
    """隨機 AI"""
    
    def choose_move(self, state):
        """
        隨機選擇一個合法移動
        """
        valid_moves = state.get_valid_moves(self.side)
        
        if not valid_moves:
            return None
        
        return random.choice(valid_moves)
