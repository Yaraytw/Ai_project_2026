"""
終端機彩色棋盤顯示模組
"""


class Display:
    """棋盤顯示"""
    
    # ANSI 彩色代碼
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bg_black": "\033[40m",
        "bg_white": "\033[47m",
    }
    
    # 棋子顏色對應
    PIECE_COLORS = {
        "A": ("bold", "red"),      # AB 方主要棋子 - 紅色
        "B": ("bold", "red"),
        "c": ("red", None),         # AB 方次要棋子 - 淡紅
        "d": ("red", None),
        "e": ("red", None),
        "f": ("red", None),
        "U": ("bold", "blue"),     # UV 方主要棋子 - 藍色
        "V": ("bold", "blue"),
        "w": ("blue", None),        # UV 方次要棋子 - 淡藍
        "x": ("blue", None),
        "y": ("blue", None),
        "z": ("blue", None),
        "+": (None, None),          # 空格
    }
    
    @staticmethod
    def _colorize(text, style=None, color=None):
        """
        為文字著色
        
        Args:
            text: 要著色的文字
            style: "bold" 或 None
            color: 顏色名稱或 None
        
        Returns:
            著色後的文字
        """
        codes = []
        if style == "bold":
            codes.append(Display.COLORS["bold"])
        if color:
            codes.append(Display.COLORS[color])
        
        if codes:
            return "".join(codes) + text + Display.COLORS["reset"]
        return text
    
    @staticmethod
    def display_board(board, highlights=None):
        """
        顯示棋盤
        
        Args:
            board: Board 對象
            highlights: 要高亮的位置列表 [(row, col), ...]
        """
        if highlights is None:
            highlights = []
        
        print("\n     0   1   2   3   4   5   6   7")
        print("   +---+---+---+---+---+---+---+---+")
        
        for row in range(8):
            row_str = f" {row} |"
            for col in range(8):
                piece = board.get_piece(row, col)
                
                # 著色棋子
                if piece in Display.PIECE_COLORS:
                    style, color = Display.PIECE_COLORS[piece]
                    colored_piece = Display._colorize(piece, style, color)
                else:
                    colored_piece = piece
                
                # 高亮背景
                if (row, col) in highlights:
                    row_str += f" {Display.COLORS['bg_white']}{colored_piece}{Display.COLORS['reset']} |"
                else:
                    row_str += f" {colored_piece} |"
            
            print(row_str)
            print("   +---+---+---+---+---+---+---+---+")
        
        print()
    
    @staticmethod
    def display_game_state(state):
        """
        顯示遊戲狀態
        
        Args:
            state: GameState 對象
        """
        info = state.get_state_info()
        
        print("\n" + "="*50)
        print(f"回合: {info['round']} | 當前方: {info['current_side']}")
        print(f"AB 方得分: {info['ab_points']} | UV 方得分: {info['uv_points']}")
        print(f"AB 方耗時: {info['ab_time']:.2f}s | UV 方耗時: {info['uv_time']:.2f}s")
        
        if info['forfeit_side']:
            print(f"犯規: {info['forfeit_side']} 方")
        
        print("="*50 + "\n")
    
    @staticmethod
    def display_move(src, dst, piece, captured=None, points=0, elapsed=0):
        """
        顯示移動信息
        
        Args:
            src: (row, col) 來源
            dst: (row, col) 目標
            piece: 棋子
            captured: 被吃掉的棋子（如果有）
            points: 獲得的得分
            elapsed: 耗時（秒）
        """
        src_row, src_col = src
        dst_row, dst_col = dst
        
        move_str = f"({src_row},{src_col}) → ({dst_row},{dst_col})"
        
        if captured:
            move_str += f" 吃掉 {captured}"
            move_str += f" 得分: +{points}"
        
        move_str += f" | 耗時: {elapsed:.2f}s"
        
        print(move_str)
    
    @staticmethod
    def display_game_over(winner, reason):
        """
        顯示遊戲結束資訊
        
        Args:
            winner: 勝者 ("AB" 或 "UV")
            reason: 勝利原因 ("points" 或 "time" 或 "forfeit" 或 "draw")
        """
        if winner is None:
            print("\n" + "="*50)
            print("遊戲結束：平局")
            print("="*50 + "\n")
        else:
            reason_map = {
                "points": "獵殺得分更高",
                "time": "耗時更少",
                "forfeit": "對手犯規",
            }
            print("\n" + "="*50)
            print(f"遊戲結束：{winner} 方勝利 ({reason_map.get(reason, reason)})")
            print("="*50 + "\n")
