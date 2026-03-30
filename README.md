# EZChess - AI 棋類遊戲

一個在 8×8 棋盤上進行的雙方對弈遊戲，支援人類玩家、隨機 AI 和 Minimax AI 三種玩家類型。

## 目錄結構

```
EZChess/
├── main.py              ← 遊戲入口（支援 CLI 參數）
├── test_game.py         ← 單元測試
├── game/
│   ├── __init__.py
│   ├── board.py         ← 棋盤底層操作
│   ├── piece.py         ← 棋子移動規則 + 得分
│   └── game.py          ← GameState（回合/計分/犯規/勝負）
├── player/
│   ├── __init__.py
│   ├── player.py        ← HumanPlayer + RandomAI
│   └── ai.py            ← MinimaxAI（Alpha-Beta 剪枝）
├── ui/
│   ├── __init__.py
│   └── display.py       ← 終端機彩色棋盤顯示
└── utils/
    ├── __init__.py
    └── timer.py         ← 計時器
```

## 快速開始

### 基本遊戲模式

```bash
# 隨機 AI vs 隨機 AI
python main.py --mode rr

# 人類 vs 人類
python main.py --mode hh

# 人類 vs Minimax AI（推薦）
python main.py --mode ha

# Minimax AI vs Minimax AI
python main.py --mode aa --depth 2
```

### 模式說明

遊戲模式使用兩個字元表示：
- 第一個字元：AB 方（先手）
  - `h`: 人類玩家
  - `r`: 隨機 AI
  - `a`: Minimax AI

- 第二個字元：UV 方（後手）
  - `h`: 人類玩家
  - `r`: 隨機 AI
  - `a`: Minimax AI

有效模式：`hh`, `ha`, `ah`, `hr`, `rh`, `rr`, `ra`, `ar`, `aa`

### 命令行選項

```
usage: main.py [-h] [--mode MODE] [--depth DEPTH] [--no-initial-move]

options:
  -h, --help         顯示幫助訊息
  --mode MODE        遊戲模式 (預設: hh)
  --depth DEPTH      AI 搜尋深度 (預設: 3)  
  --no-initial-move  跳過 UV 初始異動
```

## 遊戲規則

### 棋盤與棋子

棋盤大小 8×8，兩方各持 6 顆棋子。

| 棋子 | 方向 | 最大步數 | 得分 |
|------|------|----------|------|
| A（AB）| 四方向 | 1~2 格 | 3 |
| B（AB）| 斜向 | 1~2 格 | 3 |
| c, d（AB）| 四方向 | 1 格 | 1 |
| e, f（AB）| 斜向 | 1 格 | 1 |
| U（UV）| 四方向 | 1~2 格 | 3 |
| V（UV）| 斜向 | 1~2 格 | 3 |
| w, x（UV）| 四方向 | 1 格 | 1 |
| y, z（UV）| 斜向 | 1 格 | 1 |

### 遊戲流程

1. **初始異動**：UV 方在 120 秒內將棋盤任意一子移到空格
2. **主遊戲**：AB 方先手，雙方輪流移動
3. **最大回合**：20 回合（40 手）
4. **輸出記錄**：每手必須輸出棋步、本手耗時、累積耗時

### 勝負判定

- **獵殺得分更高**：獲勝
- **同分比較耗時**：耗時更少者獲勝
- **犯規判負**（立即結束）：
  - 單次回應超過 120 秒
  - 第 4 次超過 60 秒
  - 非法棋步或程式錯誤

## 人類玩家輸入

人類玩家進行移動時，輸入格式為：

```
src_row,src_col,dst_row,dst_col
```

例子：
```
0,0,1,1     # 將 (0,0) 的棋子移到 (1,1)
2,3,3,3     # 將 (2,3) 的棋子移到 (3,3)
quit        # 放棄遊戲
```

## 運行測試

```bash
python test_game.py
```

這將執行以下測試：
1. 基本棋盤初始化和移動驗證
2. 捕獲和計分驗證
3. AI 分級遊戲驗證

## AI 評估函數

Minimax AI 使用以下評估函數：

```
評估值 = 獵殺得分差 × 10
       + 棋子存活價值差 × 5
       + 位置熱力圖差 × 0.5
       + 行動力差 × 0.3
```

- **獵殺得分差**：當前得分差異
- **棋子存活價值**：高價值棋子（A/B/U/V）=4，低價值棋子=1.5
- **位置熱力圖**：中央位置得分更高
- **行動力**：可用棋步數越多越好

## 技術特性

- **Alpha-Beta 剪枝**：加速 Minimax 搜尋
- **可調搜尋深度**：根據性能調整 AI 難度
- **計時系統**：精確記錄每手耗時和累積耗時
- **終端彩色顯示**：棋盤視覺化（AB 方紅色，UV 方藍色）

## 示例遊戲

```bash
# 快速測試遊戲邏輯
python main.py --mode rr --no-initial-move --depth 1

# 標準人機對戰（有初始異動）
python main.py --mode ha --depth 3

# AI vs AI 對戰
python main.py --mode aa --depth 4
```

## 常見問題

**Q: 如何加快 AI 的速度？**  
A: 降低 `--depth` 參數（預設 3），如 `--depth 2`

**Q: 如何提高 AI 的難度？**  
A: 提高 `--depth` 參數（如 `--depth 5`），但會導致每步耗時增加

**Q: 人類玩家如何進行初始異動？**  
A: 當提示時，輸入格式 `src_row,src_col,dst_row,dst_col` 進行任意棋子移動

## 許可證

本專案為大學 AI 課程作業。
