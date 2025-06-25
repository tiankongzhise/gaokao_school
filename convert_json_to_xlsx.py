import json
import os
from datetime import datetime
from collections import defaultdict
import xlsxwriter

def load_json_file(file_path):
    """加载JSON文件并返回数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['data']['item']

def group_json_files(directory):
    """根据文件名规则对JSON文件进行分组"""
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    groups = defaultdict(list)
    
    for file in json_files:
        if '-' in file:
            # 如果文件名包含'-'，取'-'之前的部分作为系列名
            series_name = file.split('-')[0]
            groups[series_name].append(file)
        else:
            # 如果文件名不包含'-'，文件名去掉扩展名作为系列名
            series_name = file.replace('.json', '')
            groups[series_name].append(file)
    
    return groups

def convert_to_xlsx(directory):
    """将JSON文件转换为Excel文件"""
    # 创建输出目录
    output_dir = os.path.join(directory, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取当前日期
    current_date = datetime.now().strftime('%Y%m%d')
    
    # 对JSON文件进行分组
    file_groups = group_json_files(directory)
    
    for series_name, files in file_groups.items():
        print(f"处理系列: {series_name}")
        all_data = []
        
        # 加载该系列的所有JSON文件数据
        for file in files:
            file_path = os.path.join(directory, file)
            print(f"  加载文件: {file}")
            data = load_json_file(file_path)
            all_data.extend(data)
        
        if not all_data:
            print(f"  警告: {series_name} 系列没有数据")
            continue
        
        # 获取所有字段名（表头）
        all_keys = set()
        for item in all_data:
            all_keys.update(item.keys())
        headers = sorted(list(all_keys))
        
        # 生成Excel文件名
        excel_filename = f"{series_name}_{current_date}.xlsx"
        excel_path = os.path.join(output_dir, excel_filename)
        
        # 创建Excel文件
        workbook = xlsxwriter.Workbook(excel_path)
        worksheet = workbook.add_worksheet()
        
        # 写入表头
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)
        
        # 写入数据
        for row_num, item in enumerate(all_data, 1):
            for col_num, header in enumerate(headers):
                value = item.get(header, '')
                worksheet.write(row_num, col_num, value)
        
        workbook.close()
        print(f"  已保存: {excel_filename} (共 {len(all_data)} 条记录)")
    
    print(f"\n转换完成！所有文件已保存到: {output_dir}")

if __name__ == "__main__":
    # 设置工作目录
    directory = r"e:\github_code_lib\gaokao_school"
    convert_to_xlsx(directory)