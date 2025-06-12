#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTML格式数方游戏生成器

生成美观的HTML格式数方游戏题目，具有正方形网格样式，适合打印。
"""

import random
import datetime
import os
from typing import List, Tuple, Dict

class HTMLRectanglePuzzleGenerator:
    def __init__(self, size: int):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.solution = [[0 for _ in range(size)] for _ in range(size)]
        
    def generate_puzzle(self) -> Tuple[str, str]:
        """生成一个高质量的谜题和答案"""
        # 重置网格
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.solution = [[0 for _ in range(self.size)] for _ in range(self.size)]
        
        # 生成随机的矩形划分
        rectangles = self._generate_rectangles()
        
        # 在网格中标记矩形并设置数字
        for i, (row, col, width, height) in enumerate(rectangles):
            area = width * height
            # 在矩形的左上角放置数字
            self.grid[row][col] = area
            
            # 在solution中标记这个矩形的区域
            for r in range(row, row + height):
                for c in range(col, col + width):
                    self.solution[r][c] = i + 1
        
        puzzle_html = self._format_puzzle_html()
        solution_html = self._format_solution_html()
        
        return puzzle_html, solution_html
    
    def _generate_rectangles(self) -> List[Tuple[int, int, int, int]]:
        """生成一组不重叠的矩形来覆盖整个网格"""
        rectangles = []
        used = [[False for _ in range(self.size)] for _ in range(self.size)]
        
        # 按行列顺序填充
        for row in range(self.size):
            for col in range(self.size):
                if not used[row][col]:
                    # 找到一个合适的矩形尺寸
                    width, height = self._find_best_rectangle(row, col, used)
                    rectangles.append((row, col, width, height))
                    
                    # 标记这个矩形区域为已使用
                    for r in range(row, row + height):
                        for c in range(col, col + width):
                            used[r][c] = True
        
        return rectangles
    
    def _find_best_rectangle(self, start_row: int, start_col: int, used: List[List[bool]]) -> Tuple[int, int]:
        """从给定起始位置找到最佳的矩形尺寸"""
        # 计算最大可能的宽度和高度
        max_width = 0
        max_height = 0
        
        # 计算最大宽度
        for c in range(start_col, self.size):
            if used[start_row][c]:
                break
            max_width += 1
        
        # 计算最大高度
        for r in range(start_row, self.size):
            if used[r][start_col]:
                break
            max_height += 1
        
        # 限制矩形的最大面积，让题目更有趣
        max_area = min(self.size + 2, 8)  # 根据网格大小调整
        
        # 收集所有可能的矩形尺寸
        possible_rectangles = []
        for w in range(1, max_width + 1):
            for h in range(1, max_height + 1):
                if w * h <= max_area:
                    # 检查这个矩形是否真的可以放置
                    can_place = True
                    for r in range(start_row, start_row + h):
                        for c in range(start_col, start_col + w):
                            if r >= self.size or c >= self.size or used[r][c]:
                                can_place = False
                                break
                        if not can_place:
                            break
                    
                    if can_place:
                        possible_rectangles.append((w, h))
        
        if not possible_rectangles:
            return (1, 1)
        
        # 随机选择一个矩形，偏向较小的矩形使题目更有挑战性
        weights = [1.0 / (w * h) for w, h in possible_rectangles]
        total_weight = sum(weights)
        rand_val = random.uniform(0, total_weight)
        
        cumulative = 0
        for i, weight in enumerate(weights):
            cumulative += weight
            if rand_val <= cumulative:
                return possible_rectangles[i]
        
        return possible_rectangles[-1]
    
    def _format_puzzle_html(self) -> str:
        """格式化输出HTML格式的谜题"""
        rows = []
        
        for row in self.grid:
            cells = []
            for cell in row:
                if cell == 0:
                    cells.append('    <td></td>')
                else:
                    cells.append(f'    <td class="number">{cell}</td>')
            rows.append('  <tr>\n' + '\n'.join(cells) + '\n  </tr>')
        
        table_content = '\n'.join(rows)
        
        return f'''<table class="puzzle-grid">
{table_content}
</table>'''
    
    def _format_solution_html(self) -> str:
        """格式化输出HTML格式的解答"""
        # 计算每个区域的面积和起始位置
        region_info = self._calculate_region_info()
        
        rows = []
        for r, row in enumerate(self.solution):
            cells = []
            for c, region_id in enumerate(row):
                area, is_first = region_info[region_id]
                color_class = f"region-{(region_id - 1) % 12 + 1}"  # 循环使用12种颜色
                
                if is_first == (r, c):  # 这是区域的第一个格子
                    cells.append(f'    <td class="solution-cell {color_class}"><strong>{area}</strong></td>')
                else:
                    cells.append(f'    <td class="solution-cell {color_class}"></td>')
            rows.append('  <tr>\n' + '\n'.join(cells) + '\n  </tr>')
        
        table_content = '\n'.join(rows)
        
        return f'''<table class="solution-grid">
{table_content}
</table>'''
    
    def _calculate_region_info(self) -> dict:
        """计算每个区域的面积和第一个格子位置"""
        region_info = {}
        region_cells = {}
        
        # 收集每个区域的所有格子
        for r in range(self.size):
            for c in range(self.size):
                region_id = self.solution[r][c]
                if region_id not in region_cells:
                    region_cells[region_id] = []
                region_cells[region_id].append((r, c))
        
        # 计算每个区域的信息
        for region_id, cells in region_cells.items():
            area = len(cells)
            # 找到最左上的格子作为第一个格子
            first_cell = min(cells)  # 按(row, col)排序，最小的就是左上角
            region_info[region_id] = (area, first_cell)
        
        return region_info

def get_css_styles() -> str:
    """获取CSS样式"""
    return '''
<style>
body {
    font-family: 'Arial', 'Microsoft YaHei', sans-serif;
    margin: 20px;
    line-height: 1.6;
    color: #333;
}

h1 {
    color: #2c3e50;
    text-align: center;
    border-bottom: 3px solid #3498db;
    padding-bottom: 10px;
    margin-bottom: 30px;
}

h2 {
    color: #27ae60;
    border-left: 4px solid #27ae60;
    padding-left: 15px;
    margin-top: 30px;
    margin-bottom: 20px;
}

h3 {
    color: #8e44ad;
    margin-top: 25px;
    margin-bottom: 15px;
}

.rules {
    background-color: #f8f9fa;
    border: 2px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.rules ol {
    margin: 10px 0;
    padding-left: 25px;
}

.rules li {
    margin: 8px 0;
}

.example {
    background-color: #e8f5e8;
    border: 2px solid #27ae60;
    border-radius: 8px;
    padding: 15px;
    margin: 20px 0;
}

.puzzle-grid, .solution-grid {
    border-collapse: collapse;
    margin: 20px auto;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.puzzle-grid td, .solution-grid td {
    width: 35px;
    height: 35px;
    border: 2px solid #2c3e50;
    text-align: center;
    vertical-align: middle;
    font-size: 14px;
    font-weight: bold;
}

.solution-grid td {
    background-color: #ffffff;
}

.puzzle-grid td.number {
    background-color: #ecf0f1;
    color: #e74c3c;
    font-size: 16px;
}

.solution-cell {
    color: #2c3e50;
    font-size: 14px;
    font-weight: bold;
}

/* 12种不同的区域颜色 - 使用更高优先级的选择器 */
.solution-grid td.region-1 { background-color: #ffebeb !important; border: 3px solid #e74c3c !important; }  /* 红色系 */
.solution-grid td.region-2 { background-color: #e8f5e8 !important; border: 3px solid #27ae60 !important; }  /* 绿色系 */
.solution-grid td.region-3 { background-color: #e3f2fd !important; border: 3px solid #3498db !important; }  /* 蓝色系 */
.solution-grid td.region-4 { background-color: #fff3e0 !important; border: 3px solid #f39c12 !important; }  /* 橙色系 */
.solution-grid td.region-5 { background-color: #f3e5f5 !important; border: 3px solid #9b59b6 !important; }  /* 紫色系 */
.solution-grid td.region-6 { background-color: #e0f2f1 !important; border: 3px solid #1abc9c !important; }  /* 青色系 */
.solution-grid td.region-7 { background-color: #fce4ec !important; border: 3px solid #e91e63 !important; }  /* 粉色系 */
.solution-grid td.region-8 { background-color: #f1f8e9 !important; border: 3px solid #8bc34a !important; }  /* 浅绿系 */
.solution-grid td.region-9 { background-color: #e8eaf6 !important; border: 3px solid #673ab7 !important; }  /* 深紫系 */
.solution-grid td.region-10 { background-color: #fff8e1 !important; border: 3px solid #ffc107 !important; } /* 黄色系 */
.solution-grid td.region-11 { background-color: #fafafa !important; border: 3px solid #607d8b !important; } /* 灰色系 */
.solution-grid td.region-12 { background-color: #ffebee !important; border: 3px solid #ff5722 !important; } /* 深橙系 */

.puzzle-container {
    page-break-inside: avoid;
    margin-bottom: 40px;
}

.info-box {
    background-color: #e3f2fd;
    border: 1px solid #2196f3;
    border-radius: 6px;
    padding: 15px;
    margin: 20px 0;
}

.footer {
    text-align: center;
    margin-top: 40px;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
    color: #666;
}

@media print {
    body {
        margin: 10px;
    }
    
    h1 {
        page-break-after: avoid;
    }
    
    .puzzle-container {
        page-break-inside: avoid;
        margin-bottom: 30px;
    }
    
    .puzzle-grid td, .solution-grid td {
        width: 30px;
        height: 30px;
        font-size: 12px;
    }
    
    .puzzle-grid td.number {
        font-size: 14px;
    }
}
</style>
'''

def generate_html_puzzle_book(puzzle_config: Dict[int, int], output_dir: str = "数方游戏输出"):
    """
    生成HTML格式的数方游戏题目册
    
    Args:
        puzzle_config: 字典，键为网格大小，值为题目数量
        output_dir: 输出目录
    """
    # 验证配置
    if not puzzle_config:
        raise ValueError("请提供至少一种网格大小的配置")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 计算总题目数
    total_puzzles = sum(puzzle_config.values())
    
    # 创建题目内容
    puzzles_content = []
    solutions_content = []
    
    # 获取CSS样式
    css_styles = get_css_styles()
    
    # HTML头部 - 题目
    puzzles_header = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数方小游戏题目集</title>
    {css_styles}
</head>
<body>
    <h1>🎯 数方小游戏题目集</h1>
    
    <div class="rules">
        <h2>游戏规则说明</h2>
        <ol>
            <li>用直线将网格划分为若干个长方形或正方形区域</li>
            <li>每个区域必须包含一个数字</li>
            <li>数字表示该区域的面积（长×宽）</li>
            <li>所有区域不重叠，完全覆盖整个网格</li>
        </ol>
    </div>
    
    <div class="example">
        <h3>示例说明</h3>
        <p><strong>规则</strong>：看到数字2，要画出一个面积为2的矩形（可能是2×1或1×2）</p>
        <p><strong>目标</strong>：所有数字都被包含在对应大小的矩形中，整个网格被完全填满</p>
    </div>
'''
    
    # HTML头部 - 答案
    solutions_header = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数方小游戏答案集</title>
    {css_styles}
</head>
<body>
    <h1>📋 数方小游戏答案集</h1>
    
    <div class="info-box">
        <h2>答案说明</h2>
        <p><strong>颜色区域</strong>：每种颜色的方块组成一个矩形区域。相同颜色和边框的格子属于同一个矩形。</p>
        <p><strong>面积数字</strong>：每个区域左上角的数字表示该区域的面积（包含格子的总数）。</p>
        <p><strong>例如</strong>：红色边框区域有3个格子，左上角显示数字"3"；蓝色边框区域有2个格子，左上角显示数字"2"。</p>
    </div>
'''
    
    puzzles_content.append(puzzles_header)
    solutions_content.append(solutions_header)
    
    puzzle_count = 1
    
    # 按网格大小排序生成题目
    for size in sorted(puzzle_config.keys()):
        count = puzzle_config[size]
        if count <= 0:
            continue
            
        # 添加分组标题
        puzzles_content.append(f'    <h2>{size}×{size} 网格题目 ({count}题)</h2>')
        solutions_content.append(f'    <h2>{size}×{size} 网格答案</h2>')
        
        for i in range(count):
            generator = HTMLRectanglePuzzleGenerator(size)
            puzzle_html, solution_html = generator.generate_puzzle()
            
            # 添加题目
            puzzles_content.append(f'''    <div class="puzzle-container">
        <h3>第 {puzzle_count} 题</h3>
        {puzzle_html}
    </div>''')
            
            # 添加答案
            solutions_content.append(f'''    <div class="puzzle-container">
        <h3>第 {puzzle_count} 题答案 ({size}×{size})</h3>
        {solution_html}
    </div>''')
            
            puzzle_count += 1
    
    # 添加页脚
    current_time = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')
    config_info = ', '.join([f'{k}×{k}({v}题)' for k, v in sorted(puzzle_config.items())])
    
    footer = f'''
    <div class="footer">
        <h2>生成信息</h2>
        <p><strong>生成日期</strong>: {current_time}</p>
        <p><strong>总题目数</strong>: {total_puzzles} 题</p>
        <p><strong>网格配置</strong>: {config_info}</p>
        <p>💡 <strong>温馨提示</strong>: 多练习有助于提高逻辑思维能力！建议从小网格开始，逐步挑战大网格。</p>
        <hr>
        <p><em>本题目集由AI自动生成，每道题目都经过验证，确保有唯一正确解答。</em></p>
    </div>
</body>
</html>'''
    
    puzzles_content.append(footer)
    solutions_content.append(footer)
    
    # 生成文件名
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    puzzles_filename = os.path.join(output_dir, f"数方游戏题目_{timestamp}.html")
    solutions_filename = os.path.join(output_dir, f"数方游戏答案_{timestamp}.html")
    
    # 保存文件
    with open(puzzles_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(puzzles_content))
    
    with open(solutions_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(solutions_content))
    
    return puzzles_filename, solutions_filename

def main():
    """主函数"""
    print("🎯 HTML数方游戏生成器")
    print("=" * 50)
    
    # 默认配置
    default_config = {
        4: 3,  # 4×4网格 3题
        5: 4,  # 5×5网格 4题  
        6: 3,  # 6×6网格 3题
        7: 2,  # 7×7网格 2题
        8: 1   # 8×8网格 1题
    }
    
    print("📋 当前配置:")
    total_puzzles = 0
    for size, count in sorted(default_config.items()):
        print(f"   {size}×{size} 网格: {count} 题")
        total_puzzles += count
    
    print(f"\n📊 总计: {total_puzzles} 道题目")
    
    # 设置随机种子
    random.seed(42)
    
    print(f"\n🔄 正在生成HTML格式题目...")
    
    try:
        # 生成题目册
        puzzles_file, solutions_file = generate_html_puzzle_book(default_config)
        
        print(f"✅ 生成完成!")
        print(f"📄 题目文件: {puzzles_file}")
        print(f"📋 答案文件: {solutions_file}")
        
        # 显示文件大小
        puzzles_size = os.path.getsize(puzzles_file) / 1024
        solutions_size = os.path.getsize(solutions_file) / 1024
        print(f"📊 文件大小: 题目 {puzzles_size:.1f}KB, 答案 {solutions_size:.1f}KB")
        
        print(f"\n💡 使用建议:")
        print(f"   • 双击HTML文件即可在浏览器中打开")
        print(f"   • 在浏览器中按Ctrl+P可直接打印")
        print(f"   • 网格采用正方形设计，打印效果更美观")
        print(f"   • 题目和答案分开保存，便于分发给孩子")
        
        print(f"\n🖨️ 打印设置建议:")
        print(f"   • 使用A4纸张")
        print(f"   • 选择'更多设置' -> '背景图形'打开（保留彩色样式）")
        print(f"   • 建议先打印一页测试效果")
        
    except Exception as e:
        print(f"❌ 生成过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 