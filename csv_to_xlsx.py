import csv
import xlsxwriter
import os
from datetime import datetime

def csv_to_xlsx(csv_file_path, xlsx_file_path):
    """将CSV文件转换为Excel文件"""
    # 创建Excel工作簿
    workbook = xlsxwriter.Workbook(xlsx_file_path)
    worksheet = workbook.add_worksheet()
    
    # 读取CSV文件并写入Excel
    with open(csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row_num, row in enumerate(reader):
            for col_num, cell_data in enumerate(row):
                worksheet.write(row_num, col_num, cell_data)
    
    workbook.close()
    print(f"已转换: {os.path.basename(csv_file_path)} -> {os.path.basename(xlsx_file_path)}")

def convert_all_csv_to_xlsx(output_dir):
    """将output目录中的所有CSV文件转换为Excel文件"""
    csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        csv_path = os.path.join(output_dir, csv_file)
        xlsx_file = csv_file.replace('.csv', '.xlsx')
        xlsx_path = os.path.join(output_dir, xlsx_file)
        
        csv_to_xlsx(csv_path, xlsx_path)
        
        # 删除原CSV文件（可选）
        # os.remove(csv_path)
    
    print(f"\n所有CSV文件已转换为Excel格式！")

if __name__ == "__main__":
    output_dir = r"e:\github_code_lib\gaokao_school\output"
    convert_all_csv_to_xlsx(output_dir)