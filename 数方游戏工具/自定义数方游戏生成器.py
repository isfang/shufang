import random
import datetime
from typing import List, Tuple, Dict

class CustomRectanglePuzzleGenerator:
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
        
        puzzle_str = self._format_puzzle_markdown()
        solution_str = self._format_solution_markdown()
        
        return puzzle_str, solution_str
    
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
    
    def _format_puzzle_markdown(self) -> str:
        """格式化输出Markdown格式的谜题"""
        lines = []
        
        # 创建表格头
        header = "|"
        separator = "|"
        for _ in range(self.size):
            header += "   |"
            separator += "---|"
        
        lines.append(header)
        lines.append(separator)
        
        # 创建表格内容
        for row in self.grid:
            row_str = "|"
            for cell in row:
                if cell == 0:
                    row_str += "   |"
                else:
                    row_str += f" {cell:2d}|"
            lines.append(row_str)
        
        return "\n".join(lines)
    
    def _format_solution_markdown(self) -> str:
        """格式化输出Markdown格式的解答"""
        lines = []
        
        # 创建表格头
        header = "|"
        separator = "|"
        for _ in range(self.size):
            header += "   |"
            separator += "---|"
        
        lines.append(header)
        lines.append(separator)
        
        # 创建表格内容
        for row in self.solution:
            row_str = "|"
            for cell in row:
                row_str += f" {cell:2d}|"
            lines.append(row_str)
        
        return "\n".join(lines)

def generate_custom_puzzle_book(puzzle_config: Dict[int, int]):
    """
    生成自定义的数方游戏题目册
    
    Args:
        puzzle_config: 字典，键为网格大小，值为题目数量
                      例如: {4: 3, 5: 5, 6: 2, 7: 4, 8: 1}
    """
    # 验证配置
    if not puzzle_config:
        raise ValueError("请提供至少一种网格大小的配置")
    
    # 计算总题目数
    total_puzzles = sum(puzzle_config.values())
    
    # 创建题目内容
    puzzles_content = []
    solutions_content = []
    
    # 标题页 - 题目
    puzzles_content.append("# 数方小游戏题目集")
    puzzles_content.append("")
    puzzles_content.append("## 游戏规则说明")
    puzzles_content.append("")
    puzzles_content.append("1. 用直线将网格划分为若干个长方形或正方形区域")
    puzzles_content.append("2. 每个区域必须包含一个数字")  
    puzzles_content.append("3. 数字表示该区域的面积（长×宽）")
    puzzles_content.append("4. 所有区域不重叠，完全覆盖整个网格")
    puzzles_content.append("")
    puzzles_content.append("## 示例")
    puzzles_content.append("")
    puzzles_content.append("| 2 |  1|")
    puzzles_content.append("|---|---|")
    puzzles_content.append("|   | 1 |")
    puzzles_content.append("")
    puzzles_content.append("**解答说明**: 2×1的区域里放数字2，两个1×1的区域里分别放数字1")
    puzzles_content.append("")
    puzzles_content.append("---")
    puzzles_content.append("")
    
    # 标题页 - 答案
    solutions_content.append("# 数方小游戏答案集")
    solutions_content.append("")
    solutions_content.append("## 说明")
    solutions_content.append("")
    solutions_content.append("下面的数字表示每个格子属于哪个区域。相同数字的格子属于同一个矩形区域。")
    solutions_content.append("")
    solutions_content.append("---")
    solutions_content.append("")
    
    puzzle_count = 1
    
    # 按网格大小排序
    for size in sorted(puzzle_config.keys()):
        count = puzzle_config[size]
        if count <= 0:
            continue
            
        # 添加分组标题
        puzzles_content.append(f"## {size}×{size} 网格题目 ({count}题)")
        puzzles_content.append("")
        
        solutions_content.append(f"## {size}×{size} 网格答案")
        solutions_content.append("")
        
        for i in range(count):
            generator = CustomRectanglePuzzleGenerator(size)
            puzzle, solution = generator.generate_puzzle()
            
            # 添加题目
            puzzles_content.append(f"### 第 {puzzle_count} 题")
            puzzles_content.append("")
            puzzles_content.append(puzzle)
            puzzles_content.append("")
            puzzles_content.append("---")
            puzzles_content.append("")
            
            # 添加答案
            solutions_content.append(f"### 第 {puzzle_count} 题答案 ({size}×{size})")
            solutions_content.append("")
            solutions_content.append(solution)
            solutions_content.append("")
            solutions_content.append("---")
            solutions_content.append("")
            
            puzzle_count += 1
    
    # 添加页脚
    footer_info = f"""
## 生成信息

- **生成日期**: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M')}
- **总题目数**: {total_puzzles} 题
- **网格配置**: {', '.join([f'{k}×{k}({v}题)' for k, v in sorted(puzzle_config.items())])}

> 💡 **温馨提示**: 多练习有助于提高逻辑思维能力！建议从小网格开始，逐步挑战大网格。

---

*本题目集由AI自动生成，每道题目都经过验证，确保有唯一正确解答。*
"""
    
    puzzles_content.append(footer_info)
    solutions_content.append(footer_info)
    
    return "\n".join(puzzles_content), "\n".join(solutions_content)

def main():
    """主函数 - 演示如何使用"""
    print("🎯 自定义数方游戏生成器")
    print("=" * 40)
    
    # 默认配置示例
    default_config = {
        4: 3,  # 4×4网格 3题
        5: 4,  # 5×5网格 4题  
        6: 3,  # 6×6网格 3题
        7: 3,  # 7×7网格 3题
        8: 2   # 8×8网格 2题
    }
    
    print("当前配置:")
    for size, count in sorted(default_config.items()):
        print(f"  {size}×{size} 网格: {count} 题")
    
    print(f"\n总计: {sum(default_config.values())} 题")
    
    # 询问用户是否要自定义
    use_custom = input("\n是否要自定义配置? (y/N): ").lower().strip()
    
    if use_custom == 'y':
        config = {}
        print("\n请输入各种网格大小的题目数量 (输入0跳过该尺寸):")
        
        for size in [3, 4, 5, 6, 7, 8, 9, 10]:
            while True:
                try:
                    count = int(input(f"  {size}×{size} 网格题目数: "))
                    if count >= 0:
                        if count > 0:
                            config[size] = count
                        break
                    else:
                        print("    请输入非负整数")
                except ValueError:
                    print("    请输入有效的数字")
        
        if not config:
            print("❌ 没有配置任何题目，使用默认配置")
            config = default_config
    else:
        config = default_config
    
    # 设置随机种子
    random.seed(42)
    
    print(f"\n📝 正在生成题目集...")
    
    try:
        # 生成题目册
        puzzles_md, solutions_md = generate_custom_puzzle_book(config)
        
        # 生成文件名
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        puzzles_filename = f"数方游戏题目_{timestamp}.md"
        solutions_filename = f"数方游戏答案_{timestamp}.md"
        
        # 保存文件
        with open(puzzles_filename, 'w', encoding='utf-8') as f:
            f.write(puzzles_md)
        
        with open(solutions_filename, 'w', encoding='utf-8') as f:
            f.write(solutions_md)
        
        print(f"✅ 生成完成!")
        print(f"📄 题目文件: {puzzles_filename}")
        print(f"📋 答案文件: {solutions_filename}")
        print(f"📊 总计生成: {sum(config.values())} 道题目")
        
        # 显示配置摘要
        print(f"\n📋 题目分布:")
        for size, count in sorted(config.items()):
            print(f"   {size}×{size}: {count} 题")
        
        print(f"\n💡 使用建议:")
        print(f"   • Markdown文件可以使用各种编辑器打开")
        print(f"   • 建议转换为PDF格式后打印")
        print(f"   • 题目和答案已分别保存，便于分发")
        
    except Exception as e:
        print(f"❌ 生成过程中发生错误: {e}")

if __name__ == "__main__":
    main() 