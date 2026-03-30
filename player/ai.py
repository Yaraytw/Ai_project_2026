"""
AI 演算法模組
實現 MinimaxAI，使用 Alpha-Beta 剪枝
"""

import random
from player.player import Player
from game.piece import Piece


class MinimaxAI(Player):
    """使用 Minimax + Alpha-Beta 剪枝的 AI"""
    
    def __init__(self, side, depth=3):
        """
        初始化 AI
        
        Args:
            side: "AB" 或 "UV"
            depth: 搜尋深度
        """
        super().__init__(side)
        self.depth = depth
        self.opponent_side = "UV" if side == "AB" else "AB"
    
    def choose_move(self, state):
        """
        選擇最佳移動
        
        Returns:
            (src, dst): ((row, col), (row, col))
        """
        valid_moves = state.get_valid_moves(self.side)
        
        if not valid_moves:
            return None
        
        # 如果只有一個移動，直接返回
        if len(valid_moves) == 1:
            return valid_moves[0]
        
        # Minimax 搜尋
        best_move = None
        best_score = float('-inf')
        
        for move in valid_moves:
            # 測試這個移動
            state_copy = state.copy()
            src, dst = move
            piece = state_copy.board.get_piece(src[0], src[1])
            
            # 執行移動
            captured = state_copy.board.get_piece(dst[0], dst[1])
            points = Piece.get_points(captured) if captured != "+" else 0
            
            state_copy.board.set_piece(src[0], src[1], "+")
            state_copy.board.set_piece(dst[0], dst[1], piece)
            
            # 更新狀態
            if self.side == "AB":
                state_copy.ab_points += points
            else:
                state_copy.uv_points += points
            
            state_copy.round_num += 1
            state_copy.current_side = self.opponent_side
            
            # 評估
            score = self.minimax(state_copy, self.depth - 1, float('-inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def minimax(self, state, depth, alpha, beta, is_maximizing):
        """
        Minimax 搜尋 + Alpha-Beta 剪枝
        
        Args:
            state: GameState
            depth: 剩餘搜尋深度
            alpha: Alpha 值
            beta: Beta 值
            is_maximizing: 是否為最大化層
        
        Returns:
            評估值（整數）
        """
        # 終止條件
        if depth == 0 or state.is_game_over():
            return self.evaluate(state)
        
        valid_moves = state.get_valid_moves(state.current_side)
        
        if not valid_moves:
            # 沒有合法棋步，視為平局或對手獲勝
            return self.evaluate(state)
        
        if is_maximizing:
            # 我方行動
            max_score = float('-inf')
            for move in valid_moves:
                state_copy = state.copy()
                src, dst = move
                piece = state_copy.board.get_piece(src[0], src[1])
                captured = state_copy.board.get_piece(dst[0], dst[1])
                points = Piece.get_points(captured) if captured != "+" else 0
                
                state_copy.board.set_piece(src[0], src[1], "+")
                state_copy.board.set_piece(dst[0], dst[1], piece)
                
                if state_copy.current_side == "AB":
                    state_copy.ab_points += points
                else:
                    state_copy.uv_points += points
                
                state_copy.current_side = "UV" if state_copy.current_side == "AB" else "AB"
                
                score = self.minimax(state_copy, depth - 1, alpha, beta, False)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                
                if beta <= alpha:
                    break  # Beta 剪枝
            
            return max_score
        else:
            # 對手行動
            min_score = float('inf')
            for move in valid_moves:
                state_copy = state.copy()
                src, dst = move
                piece = state_copy.board.get_piece(src[0], src[1])
                captured = state_copy.board.get_piece(dst[0], dst[1])
                points = Piece.get_points(captured) if captured != "+" else 0
                
                state_copy.board.set_piece(src[0], src[1], "+")
                state_copy.board.set_piece(dst[0], dst[1], piece)
                
                if state_copy.current_side == "AB":
                    state_copy.ab_points += points
                else:
                    state_copy.uv_points += points
                
                state_copy.current_side = "UV" if state_copy.current_side == "AB" else "AB"
                
                score = self.minimax(state_copy, depth - 1, alpha, beta, True)
                min_score = min(min_score, score)
                beta = min(beta, score)
                
                if beta <= alpha:
                    break  # Alpha 剪枝
            
            return min_score
    
    def evaluate(self, state):
        """
        評估當前局面
        
        評估值 = 獵殺得分差 × 10
               + 棋子存活價值差 × 5
               + 位置熱力圖差 × 0.5
               + 行動力差 × 0.3
        """
        # 獵殺得分差
        ab_score = state.ab_points
        uv_score = state.uv_points
        score_diff = (ab_score - uv_score) * 10
        
        # 棋子存活價值
        ab_value = 0
        uv_value = 0
        
        for row in range(8):
            for col in range(8):
                piece = state.board.get_piece(row, col)
                if piece != "+":
                    value = Piece.get_value(piece)
                    side = Piece.get_side(piece)
                    if side == "AB":
                        ab_value += value
                    else:
                        uv_value += value
        
        value_diff = (ab_value - uv_value) * 5
        
        # 位置熱力圖（中央較有利）
        ab_heat = 0
        uv_heat = 0
        
        for row in range(8):
            for col in range(8):
                piece = state.board.get_piece(row, col)
                if piece != "+":
                    # 距離中心的倒數距離
                    center_dist = max(abs(row - 3.5), abs(col - 3.5))
                    heat_value = max(0, 4 - center_dist) * 0.5
                    
                    side = Piece.get_side(piece)
                    if side == "AB":
                        ab_heat += heat_value
                    else:
                        uv_heat += heat_value
        
        heat_diff = (ab_heat - uv_heat) * 0.5
        
        # 行動力（合法棋步數）
        ab_moves = len(state.get_valid_moves("AB")) if state.current_side == "AB" else 0
        uv_moves = len(state.get_valid_moves("UV")) if state.current_side == "UV" else 0
        mobility_diff = (ab_moves - uv_moves) * 0.3
        
        # 如果是我方的視角，反轉評估
        total = score_diff + value_diff + heat_diff + mobility_diff
        
        if self.side == "AB":
            return total
        else:
            return -total
