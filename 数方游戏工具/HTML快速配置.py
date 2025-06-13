#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML数方游戏快速生成配置文件

直接修改下面的配置，然后运行这个文件即可生成HTML格式的数方游戏题目。
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from HTML数方游戏生成器 import generate_html_puzzle_book
import datetime
import random

# ========================================
# 配置区域 - 请根据需要修改下面的配置
# ========================================

# 题目配置：键为网格大小，值为题目数量
PUZZLE_CONFIG = {
    3: 2,   # 3×3 网格 2 题 (入门级)
    4: 8,   # 4×4 网格 5 题 
    5: 8,   # 5×5 网格 4 题
    6: 8,   # 6×6 网格 3 题  
    7: 8,   # 7×7 网格 2 题
    8: 8,   # 8×8 网格 1 题 (挑战级)
}

# 其他配置
RANDOM_SEED = 43  # 随机种子，相同种子生成相同题目
OUTPUT_DIR = "../数方游戏输出"  # 输出目录

# ========================================
# 预设配置模板 (取消注释即可使用)
# ========================================

# 入门级配置 (适合5-8岁)
# PUZZLE_CONFIG = {
#     3: 4,
#     4: 6, 
#     5: 3,
# }

# 进阶级配置 (适合8-12岁)  
# PUZZLE_CONFIG = {
#     4: 4,
#     5: 6,
#     6: 5, 
#     7: 3,
# }

# 挑战级配置 (适合12岁以上)
# PUZZLE_CONFIG = {
#     5: 3,
#     6: 4,
#     7: 5,
#     8: 4,
#     9: 2,
# }

# 班级大批量配置
# PUZZLE_CONFIG = {
#     4: 15,
#     5: 15,
#     6: 10,
#     7: 8,
#     8: 5,
# }

def main():
    """生成HTML格式数方游戏题目"""
    print("🎯 HTML数方游戏快速生成器")
    print("=" * 50)
    
    # 显示当前配置
    print("📋 当前配置:")
    total_puzzles = 0
    for size, count in sorted(PUZZLE_CONFIG.items()):
        print(f"   {size}×{size} 网格: {count} 题")
        total_puzzles += count
    
    print(f"\n📊 总计: {total_puzzles} 道题目")
    
    if total_puzzles == 0:
        print("❌ 错误: 没有配置任何题目!")
        print("💡 请修改 PUZZLE_CONFIG 字典，设置至少一种网格大小的题目数量")
        return
    
    # 设置随机种子
    random.seed(RANDOM_SEED)
    
    print(f"\n🔄 正在生成HTML格式题目...")
    
    try:
        # 生成题目册
        puzzles_file, solutions_file = generate_html_puzzle_book(PUZZLE_CONFIG, OUTPUT_DIR)
        
        print(f"✅ 生成完成!")
        print(f"📄 题目文件: {puzzles_file}")
        print(f"📋 答案文件: {solutions_file}")
        
        # 显示文件大小
        puzzles_size = os.path.getsize(puzzles_file) / 1024
        solutions_size = os.path.getsize(solutions_file) / 1024
        print(f"📊 文件大小: 题目 {puzzles_size:.1f}KB, 答案 {solutions_size:.1f}KB")
        
        print(f"\n💡 使用建议:")
        print(f"   • 双击HTML文件即可在浏览器中打开")
        print(f"   • 网格采用正方形设计，视觉效果更佳")
        print(f"   • 在浏览器中按Ctrl+P可直接打印")
        print(f"   • 题目和答案分开保存，便于教学使用")
        
        print(f"\n🖨️ 打印设置建议:")
        print(f"   • 使用A4纸张，竖向打印")
        print(f"   • 选择'更多设置' -> '背景图形'打开")
        print(f"   • 可以双面打印节省纸张")
        print(f"   • 建议先打印一页测试效果")
        
        print(f"\n🎯 教学建议:")
        print(f"   • 先给孩子题目文件，让其独立思考")
        print(f"   • 完成后再提供答案文件对照")
        print(f"   • 从小网格开始，循序渐进增加难度")
        
    except Exception as e:
        print(f"❌ 生成过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 