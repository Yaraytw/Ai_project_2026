"""
EZChess 遊戲入口
支援多種遊戲模式：AI vs AI、人 vs 人、人 vs AI、AI vs 人
"""

import argparse
import sys
from game.game import GameState
from player.player import HumanPlayer, RandomAI
from player.ai import MinimaxAI
from ui.display import Display


def create_player(mode_char, side):
    """
    根據模式字元創建玩家
    
    Args:
        mode_char: 'h' (HumanPlayer), 'r' (RandomAI), 'a' (MinimaxAI)
        side: "AB" 或 "UV"
    
    Returns:
        Player 對象
    """
    if mode_char == 'h':
        return HumanPlayer(side)
    elif mode_char == 'r':
        return RandomAI(side)
    elif mode_char == 'a':
        return MinimaxAI(side, depth=3)
    else:
        raise ValueError(f"未知的模式字元: {mode_char}")


def get_initial_move_uv(player, state):
    """
    讓 UV 方進行初始異動
    只有 UV 方需要進行初始異動（在遊戲開始前）
    """
    print("\n" + "="*50)
    print("初始異動：UV 方可選擇棋盤上『不分敵我』之任一子換到某個空格")
    print("="*50)
    
    while True:
        move = player.choose_move(state)
        if move:
            src, dst = move
            piece = state.board.get_piece(src[0], src[1])
            
            # 簡報規定：不分敵我之任一子皆可移動，只要不是空格即可
            if piece != "+":
                return move
            else:
                print("來源位置必須有棋子")
        else:
            print("移動失敗，請重試")


def play_game(ab_player, uv_player, is_initial_move_required=True, depth=3):
    """
    進行一局遊戲
    
    Args:
        ab_player: AB 方玩家
        uv_player: UV 方玩家
        is_initial_move_required: 是否需要 UV 初始異動
        depth: AI 搜尋深度
    """
    state = GameState()
    
    # 更新 AI 深度
    if isinstance(ab_player, MinimaxAI):
        ab_player.depth = depth
    if isinstance(uv_player, MinimaxAI):
        uv_player.depth = depth
    
    # 顯示初始棋盤
    print("\n" + "="*50)
    print("遊戲開始！")
    print("="*50)
    Display.display_board(state.board)
    
    # UV 方初始異動
    if is_initial_move_required:
        initial_move = get_initial_move_uv(uv_player, state)
        src, dst = initial_move
        piece = state.board.get_piece(src[0], src[1]) # 取得被異動的棋子名稱
        
        state.apply_move(src, dst, 0, is_initial=True)
        
        # 配合簡報格式，例如 B:(3,5)-(2,4)
        print(f"\nUV 方初始異動: {piece}:({src[0]},{src[1]})-({dst[0]},{dst[1]})")
        Display.display_board(state.board)
        # 注意：game.py 中的 apply_move 已經會自動處理換手與回合數初始化
    
    # 主遊戲迴圈
    move_count = 0
    while not state.is_game_over():
        Display.display_game_state(state)
        
        # 選擇當前玩家
        if state.current_side == "AB":
            current_player = ab_player
        else:
            current_player = uv_player
        
        print(f"輪到 {state.current_side} 方")
        
        # 獲取帶計時的移動
        result = current_player.timed_move(state)
        
        if result is None:
            print(f"{state.current_side} 方移動失敗或超時，犯規")
            state.forfeit_side = state.current_side
            state.game_ended = True
            break
        
        src, dst, elapsed = result
        piece = state.board.get_piece(src[0], src[1])
        captured = state.board.get_piece(dst[0], dst[1])
        points_gained = 0
        
        if captured != "+":
            from game.piece import Piece
            points_gained = Piece.get_points(captured)
        
        # 執行移動
        move_record = state.apply_move(src, dst, elapsed)
        
        if move_record is None:
            print(f"{state.current_side} 方非法移動或犯規")
            state.forfeit_side = state.current_side
            state.game_ended = True
            break
        
        move_count += 1
        
        # 顯示移動資訊，精準配合簡報要求的輸出格式
        print(f"{piece}:({src[0]},{src[1]})-({dst[0]},{dst[1]})", end="")
        if captured != "+":
            print(f" 吃掉 {captured} 得 {points_gained} 分", end="")
        print(f" | 本手耗時: {elapsed:.2f}s", end="")
        
        ab_total = state.ab_time
        uv_total = state.uv_time
        print(f" | 累積耗時: AB={ab_total:.2f}s UV={uv_total:.2f}s")
        
        Display.display_board(state.board)
    
    # 遊戲結束
    print("\n" + "="*50)
    print("遊戲結束")
    print("="*50)
    
    winner, reason = state.get_winner() if state.get_winner() else (None, None)
    
    Display.display_game_over(winner, reason)
    
    print(f"總回合數: {state.round_num}")
    print(f"AB 方: 得分={state.ab_points} 耗時={state.ab_time:.2f}s")
    print(f"UV 方: 得分={state.uv_points} 耗時={state.uv_time:.2f}s")
    
    if winner:
        print(f"勝者: {winner} 方")
    else:
        print("平局")


def main():
    """主程序"""
    parser = argparse.ArgumentParser(
        description='EZChess 遊戲',
        epilog='模式說明: h=人類, r=隨機AI, a=Minimax AI'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        default='hh',
        help='遊戲模式 (aa/hh/ha/ah/ra/ar/rr, 預設:hh)'
    )
    
    parser.add_argument(
        '--depth',
        type=int,
        default=3,
        help='AI 搜尋深度 (預設:3)'
    )
    
    parser.add_argument(
        '--no-initial-move',
        action='store_true',
        help='跳過 UV 初始異動'
    )
    
    args = parser.parse_args()
    
    # 驗證模式
    mode = args.mode.lower()
    if len(mode) != 2 or mode not in ['aa', 'hh', 'ha', 'ah', 'ra', 'ar', 'rr']:
        print("錯誤：模式必須是 aa/hh/ha/ah/ra/ar/rr")
        print("  第一個字元表示 AB 方: h=人類, r=隨機AI, a=Minimax AI")
        print("  第二個字元表示 UV 方: h=人類, r=隨機AI, a=Minimax AI")
        sys.exit(1)
    
    ab_mode, uv_mode = mode[0], mode[1]
    
    # 創建玩家
    ab_player = create_player(ab_mode, "AB")
    uv_player = create_player(uv_mode, "UV")
    
    # 進行遊戲
    try:
        play_game(
            ab_player,
            uv_player,
            is_initial_move_required=not args.no_initial_move,
            depth=args.depth
        )
    except KeyboardInterrupt:
        print("\n\n遊戲被使用者中斷")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()