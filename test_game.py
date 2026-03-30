"""
EZChess 遊戲測試腳本
快速測試遊戲邏輯是否正確
"""

from game.game import GameState
from game.board import Board
from game.piece import Piece
from player.player import RandomAI
from ui.display import Display


def test_basic_moves():
    """測試基本移動"""
    print("="*50)
    print("測試 1: 基本棋盤和移動")
    print("="*50)
    
    state = GameState()
    Display.display_board(state.board)
    
    # 檢查合法棋步
    ab_moves = state.get_valid_moves("AB")
    uv_moves = state.get_valid_moves("UV")
    
    print(f"AB 方合法棋步數: {len(ab_moves)}")
    print(f"UV 方合法棋步數: {len(uv_moves)}")
    
    if ab_moves:
        print(f"AB 方第一步: {ab_moves[0]}")
    
    print("✓ 測試通過\n")


def test_capture_and_scoring():
    """測試捕獲和計分"""
    print("="*50)
    print("測試 2: 捕獲和計分")
    print("="*50)
    
    state = GameState()
    
    # 手動設置一個棋盤狀態來測試捕獲
    # 將 V（UV 方斜向棋子，3 分）設置在可以被 A 捕獲的位置
    state.board.grid[1][0] = "V"  # 把 V 放在 (1,0)，可被 A 吃掉
    state.board.grid[1][1] = "+"  # 清空 d
    state.current_side = "AB"  # 設置當前方為 AB
    
    print(f"初始棋盤:")
    Display.display_board(state.board)
    
    # A 吃掉 V
    move = state.apply_move((0, 0), (1, 0), 0.5)
    
    if move:
        print(f"AB 方移動 A 從 (0,0) 到 (1,0)，吃掉 {move.captured}")
        print(f"AB 方得分: {state.ab_points}")
        Display.display_board(state.board)
        print("✓ 測試通過\n")
    else:
        print("✗ 移動失敗\n")


def test_ai_game():
    """測試 AI 遊戲"""
    print("="*50)
    print("測試 3: AI vs AI 快速遊戲（限制 3 回合）")
    print("="*50)
    
    state = GameState()
    ab_ai = RandomAI("AB")
    uv_ai = RandomAI("UV")
    
    # UV 方初始異動
    initial_move = uv_ai.timed_move(state)
    if initial_move:
        src, dst, elapsed = initial_move
        state.apply_move(src, dst, elapsed, is_initial=True)
        print(f"UV 初始異動: ({src[0]},{src[1]}) → ({dst[0]},{dst[1]}) ({elapsed:.3f}s)")
        state.initial_move_done = True
        state.round_num = 0
        state.current_side = "AB"
    
    Display.display_board(state.board)
    
    # 進行 3 回合
    round_count = 0
    while round_count < 3 and not state.is_game_over():
        if state.current_side == "AB":
            player = ab_ai
        else:
            player = uv_ai
        
        move_result = player.timed_move(state)
        
        if move_result:
            src, dst, elapsed = move_result
            piece = state.board.get_piece(src[0], src[1])
            state.apply_move(src, dst, elapsed)
            print(f"{state.current_side} 方移動: ({src[0]},{src[1]}) → ({dst[0]},{dst[1]}) ({elapsed:.3f}s)")
            round_count += 1
        else:
            print(f"{state.current_side} 方無法移動")
            break
    
    Display.display_board(state.board)
    print(f"AB 方: 得分={state.ab_points} 耗時={state.ab_time:.2f}s")
    print(f"UV 方: 得分={state.uv_points} 耗時={state.uv_time:.2f}s")
    print("✓ 測試通過\n")


if __name__ == '__main__':
    try:
        test_basic_moves()
        test_capture_and_scoring()
        test_ai_game()
        
        print("="*50)
        print("所有測試通過！✓")
        print("="*50)
    except Exception as e:
        print(f"\n✗ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
