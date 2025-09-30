# 简易赛车游戏

这是一个使用 Python 和 Pygame 编写的简易赛车游戏示例。玩家可以通过左右方向键（或 A/D 键）控制赛车在三条车道之间移动，躲避迎面而来的障碍物。每躲避一个障碍物都会提升分数，游戏会记录历史最高分。

## 环境依赖

- Python 3.11+
- Pygame

## 快速开始

1. （可选）创建并激活虚拟环境：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows 使用 .venv\\Scripts\\activate
   ```
2. 安装依赖：
   ```bash
   pip install pygame
   ```
3. 在项目根目录运行游戏：
   ```bash
   python game.py
   ```

## 操作说明

启动后即可进入游戏界面，按以下按键进行操作：

- ← / A：向左切换车道
- → / D：向右切换车道
- R：重新开始
- Esc：退出游戏
