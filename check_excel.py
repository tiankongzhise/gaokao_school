import xlsxwriter
import csv

# 重新创建Excel文件，确保数据完整
print("\n重新创建Excel文件...")

# 读取CSV文件
with open('output/211_20250625.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    data = list(reader)
    print(f"CSV文件总行数: {len(data)}")

# 创建新的Excel文件
workbook = xlsxwriter.Workbook('output/211_20250625_fixed.xlsx')
worksheet = workbook.add_worksheet()

# 写入所有数据
for row_num, row_data in enumerate(data):
    for col_num, cell_data in enumerate(row_data):
        worksheet.write(row_num, col_num, cell_data)

workbook.close()
print("已创建修复的Excel文件: 211_20250625_fixed.xlsx")

print(f"新Excel文件应该包含 {len(data)} 行数据（包括表头）")
print(f"新Excel文件应该包含 {len(data) - 1} 条数据记录")