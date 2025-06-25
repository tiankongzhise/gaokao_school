
import requests
import json
import os
import pandas as pd
from pathlib import Path
import time
from typing import Dict, List

# 配置
year_list = [2024, 2023, 2022]
url_template = 'https://static-data.gaokao.cn/www/2.0/schoolprovincescore/{school_code}/{year}/43.json?a=www.gaokao.cn'
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "if-modified-since": "Wed, 11 Jun 2025 10:40:09 GMT",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}

# 创建必要的目录
temp_dir = Path("../temp")
score_dir = Path("../score")
temp_dir.mkdir(exist_ok=True)
score_dir.mkdir(exist_ok=True)

def load_school_mapping() -> Dict[str, str]:
    """加载学校映射数据"""
    with open('../school_mapping.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def fetch_score_data(school_code: str, year: int, session: requests.Session) -> Dict:
    """获取指定学校和年份的录取分数线数据"""
    url = url_template.format(school_code=school_code, year=year)
    
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 检查响应是否设置了新的cookies
        if response.cookies:
            session.cookies.update(response.cookies)
            
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败 {url}: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"JSON解析失败 {url}: {e}")
        return {}

def save_temp_data(school_name: str, year: int, data: Dict):
    """保存临时数据到temp文件夹"""
    filename = f"{school_name}_{year}.json"
    filepath = temp_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"已保存: {filepath}")

def merge_school_data(school_name: str) -> List[Dict]:
    """合并同一学校的所有年份数据"""
    all_data = []
    
    for year in year_list:
        filename = f"{school_name}_{year}.json"
        filepath = temp_dir / filename
        
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'data' in data and isinstance(data['data'], list):
                    # 为每条记录添加年份信息
                    for record in data['data']:
                        record['year'] = year
                    all_data.extend(data['data'])
    
    return all_data

def save_excel_data(school_name: str, data: List[Dict]):
    """将数据保存为Excel文件"""
    if not data:
        print(f"警告: {school_name} 没有数据可保存")
        return
    
    df = pd.DataFrame(data)
    filename = f"{school_name}.xlsx"
    filepath = score_dir / filename
    
    df.to_excel(filepath, index=False, engine='openpyxl')
    print(f"已保存Excel: {filepath}")

def main():
    """主函数"""
    # 加载学校映射
    school_mapping = load_school_mapping()
    
    # 创建会话以保持cookies
    session = requests.Session()
    
    print(f"开始爬取 {len(school_mapping)} 所学校的录取分数线数据...")
    
    # 遍历所有学校
    for school_name, school_code in school_mapping.items():
        print(f"\n正在处理: {school_name} (代码: {school_code})")
        
        # 获取每年的数据
        for year in year_list:
            print(f"  获取 {year} 年数据...")
            data = fetch_score_data(school_code, year, session)
            
            if data:
                save_temp_data(school_name, year, data)
            else:
                print(f"  {year} 年数据获取失败")
            
            # 添加延时避免请求过快
            time.sleep(1)
        
        # 合并该学校的所有年份数据
        merged_data = merge_school_data(school_name)
        if merged_data:
            save_excel_data(school_name, merged_data)
        
        # 学校间添加更长延时
        time.sleep(2)
    
    print("\n所有数据爬取完成！")

if __name__ == "__main__":
    main()
