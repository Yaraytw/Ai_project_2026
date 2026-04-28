"""
遊戲狀態管理模組
管理回合、計分、犯規檢查、勝負判定等
"""

from game.board import Board
from game.piece import Piece


class MoveRecord:
    """移動記錄"""
    def __init__(self, src, dst, piece, captured=None, points=0, elapsed=0):
        self.src = src
        self.dst = dst
        self.piece = piece
        self.captured = captured  # 被吃掉的棋子
        self.points = points
        self.elapsed = elapsed


class GameState:
    """遊戲狀態管理"""
    
    MAX_ROUNDS = 20
    TIME_NORMAL = 60
    TIME_EXTENDED = 120
    MAX_EXTENDS = 3
    SLOW_FORFEIT_CNT = 4
    
    def __init__(self):
        """初始化遊戲狀態"""
        self.board = Board()
        self.round_num = 0  # 當前回合數（0 表示還未開始）
        self.current_side = "UV"  # UV 方先進行初始異動
        self.ab_points = 0
        self.uv_points = 0
        self.ab_time = 0
        self.uv_time = 0
        self.time_extends = {"AB": 3, "UV": 3}  # 剩餘延長次數
        self.slow_responses = {"AB": 0, "UV": 0}  # 超過 60 秒的次數
        self.moves_history = []  # 移動歷史
        self.initial_move_done = False  # 是否已完成 UV 初始異動
        self.forfeit_side = None  # 犯規方（如果有）
        self.game_ended = False
    
    def setup_game(self, initial_move=None):
        """
        設置遊戲（處理 UV 的初始異動）
        
        Args:
            initial_move: ((row, col), (row, col)) 初始異動
        """
        if initial_move:
            src, dst = initial_move
            self.apply_move(src, dst, 0, is_initial=True)
    
    def apply_move(self, src, dst, elapsed, is_initial=False):
        """
        執行一步棋
        
        Args:
            src: (row, col) 來源位置
            dst: (row, col) 目標位置
            elapsed: 本手耗時（秒）
            is_initial: 是否為初始異動
        
        Returns:
            MoveRecord: 移動記錄
            None: 移動非法或犯規
        """
        # 檢查犯規
        if self.forfeit_side:
            return None
        
        src_row, src_col = src
        dst_row, dst_col = dst
        piece = self.board.get_piece(src_row, src_col)
        
        # 移動合法性檢查
        if not piece or piece == "+":
            return None
        
        side = Piece.get_side(piece)
        if not is_initial and side != self.current_side:
            return None
        
        # 檢查目標是否可達
        valid_moves = Piece.get_moves(piece, src_row, src_col, self.board)
        if (dst_row, dst_col) not in valid_moves:
            return None
        
        # 執行移動
        captured_piece = self.board.get_piece(dst_row, dst_col)
        points = 0
        if captured_piece != "+":
            points = Piece.get_points(captured_piece)
        
        self.board.set_piece(src_row, src_col, "+")
        self.board.set_piece(dst_row, dst_col, piece)
        
        # 更新計分和耗時
        if side == "AB":
            self.ab_points += points
            self.ab_time += elapsed
        else:
            self.uv_points += points
            self.uv_time += elapsed
        
        # 檢查超時犯規
        if elapsed > self.TIME_EXTENDED:
            self.forfeit_side = side
            self.game_ended = True
            return None
        
        if elapsed > self.TIME_NORMAL:
            self.time_extends[side] -= 1
            self.slow_responses[side] += 1
            if self.slow_responses[side] >= self.SLOW_FORFEIT_CNT:
                self.forfeit_side = side
                self.game_ended = True
                return None
            if self.time_extends[side] < 0:
                self.forfeit_side = side
                self.game_ended = True
                return None
        
        # 記錄移動
        move_record = MoveRecord(src, dst, piece, captured_piece, points, elapsed)
        self.moves_history.append(move_record)
        
        # 更新遊戲狀態與換手防呆
        if is_initial:
            self.initial_move_done = True
            self.round_num = 1
            self.current_side = "AB"  # 確保初始異動完，狀態機強制換 AB 先手
        else:
            # 只有當 UV (後手) 走完時，才算完整的一回合結束
            if self.current_side == "UV":
                self.round_num += 1
                
            self.current_side = "UV" if self.current_side == "AB" else "AB"
            
            # 檢查是否達到最大回合數
            if self.round_num > self.MAX_ROUNDS:
                self.game_ended = True
        
        return move_record
    
    def get_valid_moves(self, side):
        """
        獲取某一方的所有合法棋步
        
        Args:
            side: "AB" 或 "UV"
        
        Returns:
            list: [((src_row, src_col), (dst_row, dst_col)), ...]
        """
        moves = []
        pieces = self.board.get_all_pieces(side)
        
        for (row, col), piece in pieces.items():
            valid_dests = Piece.get_moves(piece, row, col, self.board)
            for dst in valid_dests:
                moves.append(((row, col), dst))
        
        return moves
    
    def is_game_over(self):
        """檢查遊戲是否結束"""
        return self.game_ended or self.forfeit_side is not None
    
    def get_winner(self):
        """
        獲取勝者
        
        Returns:
            ("AB" or "UV", reason: "points" | "time" | "forfeit")
            None: 遊戲未結束
        """
        if self.forfeit_side:
            loser = self.forfeit_side
            winner = "UV" if loser == "AB" else "AB"
            return (winner, "forfeit")
        
        if not self.game_ended:
            return None
        
        # 比較獵殺得分
        if self.ab_points > self.uv_points:
            return ("AB", "points")
        elif self.uv_points > self.ab_points:
            return ("UV", "points")
        else:
            # 同分比較耗時
            if self.ab_time < self.uv_time:
                return ("AB", "time")
            elif self.uv_time < self.ab_time:
                return ("UV", "time")
            else:
                return (None, "draw")  # 平局
    
    def get_state_info(self):
        """獲取遊戲狀態資訊"""
        return {
            "round": self.round_num,
            "current_side": self.current_side,
            "ab_points": self.ab_points,
            "uv_points": self.uv_points,
            "ab_time": self.ab_time,
            "uv_time": self.uv_time,
            "game_ended": self.game_ended,
            "forfeit_side": self.forfeit_side,
        }
    
    def copy(self):
        """複製遊戲狀態（用於 AI 搜尋）"""
        new_state = GameState.__new__(GameState)
        new_state.board = self.board.copy()
        new_state.round_num = self.round_num
        new_state.current_side = self.current_side
        new_state.ab_points = self.ab_points
        new_state.uv_points = self.uv_points
        new_state.ab_time = self.ab_time
        new_state.uv_time = self.uv_time
        new_state.time_extends = self.time_extends.copy()
        new_state.slow_responses = self.slow_responses.copy()
        new_state.moves_history = self.moves_history[:]
        new_state.initial_move_done = self.initial_move_done
        new_state.forfeit_side = self.forfeit_side
        new_state.game_ended = self.game_ended
        return new_state