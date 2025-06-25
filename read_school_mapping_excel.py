import pandas as pd
import json
from pathlib import Path

def read_excel_to_mapping():
    """读取Excel文件并生成school_mapping.json"""
    excel_path = Path("source/school_mapping.xlsx")
    
    if not excel_path.exists():
        print(f"错误: {excel_path} 文件不存在")
        return
    
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_path)
        print(f"Excel文件列名: {df.columns.tolist()}")
        print(f"前5行数据:")
        print(df.head())
        
        # 假设第一列是学校名称，第二列是学校代码
        # 根据实际情况调整列名
        if len(df.columns) >= 2:
            school_mapping = {}
            for index, row in df.iterrows():
                school_name = str(row.iloc[0]).strip()
                school_code = str(row.iloc[1]).strip()
                
                if school_name and school_code and school_name != 'nan' and school_code != 'nan':
                    school_mapping[school_name] = school_code
            
            # 保存为JSON文件
            with open('school_mapping.json', 'w', encoding='utf-8') as f:
                json.dump(school_mapping, f, ensure_ascii=False, indent=2)
            
            print(f"\n成功生成 school_mapping.json，包含 {len(school_mapping)} 所学校")
            print("前10所学校:")
            for i, (name, code) in enumerate(list(school_mapping.items())[:10]):
                print(f"  {name}: {code}")
        else:
            print("错误: Excel文件列数不足")
            
    except Exception as e:
        print(f"读取Excel文件时出错: {e}")

if __name__ == "__main__":
    read_excel_to_mapping()