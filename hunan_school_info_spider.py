import requests
import json
import os
import pandas as pd
from pathlib import Path
import time
from typing import Dict, List
import argparse


URL_TEMPLATE = 'https://static-data.gaokao.cn/www/2.0/school/{school_code}/info.json?a=www.gaokao.cn'

# 请求头
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
}

class HunanScoreSpider:
    def __init__(self):
        self.temp_dir = Path("temp_school_info")
        self.score_dir = Path("school_info")
        self.session = requests.Session()
        
        # 创建必要的目录
        self.temp_dir.mkdir(exist_ok=True)
        self.score_dir.mkdir(exist_ok=True)
        
        print(f"初始化爬虫")
    
    def load_school_mapping(self) -> Dict[str, str]:
        """加载学校映射数据"""
        mapping_file = Path('school_mapping.json')
        if not mapping_file.exists():
            raise FileNotFoundError("school_mapping.json 文件不存在，请先运行 read_school_mapping_excel.py")
        
        with open(mapping_file, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        print(f"加载了 {len(mapping)} 所学校的映射数据")
        return mapping
    
    def fetch_school_info_data(self, school_code: str) -> Dict:
        """获取指定学校和年份的录取分数线数据"""
        url = URL_TEMPLATE.format(school_code=school_code)
        
        try:
            response = self.session.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            
            # 检查响应是否设置了新的cookies
            if response.cookies:
                self.session.cookies.update(response.cookies)
                print(f"    更新了cookies: {dict(response.cookies)}")
            
            data = response.json()
            
            # 检查数据有效性
            if 'data' in data and isinstance(data['data'], dict):
                total_records = 0
                for key, value in data['data'].items():
                    if isinstance(value, dict) and 'item' in value:
                        total_records += len(value['item'])
                print(f"    成功获取 {total_records} 条记录")
                return data
            elif 'data' in data and isinstance(data['data'], list):
                print(f"    成功获取 {len(data['data'])} 条记录")
                return data
            else:
                print(f"    响应格式异常或无数据")
                return data
            
        except requests.exceptions.RequestException as e:
            print(f"    请求失败: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"    JSON解析失败: {e}")
            return {}
        except Exception as e:
            print(f"    未知错误: {e}")
            return {}
    
    def save_temp_data(self, school_name: str, data: Dict):
        """保存临时数据到temp文件夹"""
        filename = f"{school_name}.json"
        filepath = self.temp_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"    已保存临时文件: {filepath}")
    
    def merge_school_data(self, school_name: str) -> List[Dict]:
        """合并同一学校的所有年份数据"""
        all_data = []
        filename = f"{school_name}.json"
        filepath = self.temp_dir / filename
        
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if 'data' in data:
                    year_records = []
                    if isinstance(data['data'], dict):
                        # 新格式：data是字典，包含不同类型的数据
                        for type_key, type_data in data['data'].items():
                            if isinstance(type_data, dict) and 'item' in type_data:
                                for record in type_data['item']:
                                    record['type_key'] = type_key
                                    year_records.append(record)
                    elif isinstance(data['data'], list):
                        # 旧格式：data是列表
                        for record in data['data']:
                            year_records.append(record)
                    
                    all_data.extend(year_records)
                    print(f"    合并 {school_name} 数据: {len(year_records)} 条")
            except Exception as e:
                print(f"    读取 {school_name} 数据失败: {e}")
        
        return all_data
    
    def save_excel_data(self, school_name: str, data: List[Dict]):
        """将数据保存为Excel文件"""
        if not data:
            print(f"    警告: {school_name} 没有数据可保存")
            return
        
        try:
            df = pd.DataFrame(data)
            filename = f"{school_name}.xlsx"
            filepath = self.score_dir / filename
            
            df.to_excel(filepath, index=False, engine='openpyxl')
            print(f"    已保存Excel: {filepath} ({len(data)} 条记录)")
        except Exception as e:
            print(f"    保存Excel失败: {e}")
    
    def crawl_all_schools(self):
        """爬取所有学校的数据"""
        # 加载学校映射
        school_mapping = self.load_school_mapping()
        
        print(f"\n开始爬取 {len(school_mapping)} 所学校的录取分数线数据...")
        success_count = 0
        total_schools = len(school_mapping)
        
        # 遍历所有学校
        for i, (school_name, school_code) in enumerate(school_mapping.items(), 1):
            print(f"\n[{i}/{total_schools}] 正在处理: {school_name} (代码: {school_code})")
            
            school_has_data = False
            

            data = self.fetch_school_info_data(school_code)
            
            if data and 'data' in data:
                self.save_temp_data(school_name, data)
            #     school_has_data = True
            # # 合并该学校的所有年份数据
            # if school_has_data:
            #     merge_data = self.merge_school_data(school_name)
            #     print(f"  合并 {school_name} 的数据...")
            #     self.save_excel_data(school_name, merge_data)
                success_count += 1
            
            # 学校间添加更长延时
            time.sleep(2)
            
            # 每处理10所学校显示进度
            if i % 10 == 0:
                print(f"\n进度: {i}/{total_schools} ({i/total_schools*100:.1f}%), 成功: {success_count}")
        
        print(f"\n所有数据爬取完成！")
        print(f"总计处理: {total_schools} 所学校")
        print(f"成功获取数据: {success_count} 所学校")
        print(f"成功率: {success_count/total_schools*100:.1f}%")

def main():
    parser = argparse.ArgumentParser(description='湖南省高考录取分数线爬虫')
    args = parser.parse_args()
    
    spider = HunanScoreSpider()
    spider.crawl_all_schools()

if __name__ == "__main__":
    main()