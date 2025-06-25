import json

files = ['211-1.json', '211-2.json', '211-3.json', '211-4.json', '211-5.json', '211-6.json', '211-7.json']
total = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        count = len(data['data']['item'])
        total += count
        print(f'{f}: {count} 条记录')

print(f'总计: {total} 条记录')

# 检查CSV文件的行数
import csv
with open('output/211_20250625.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    csv_rows = sum(1 for row in reader)
    print(f'CSV文件总行数: {csv_rows} (包括表头)')
    print(f'CSV文件数据行数: {csv_rows - 1}')