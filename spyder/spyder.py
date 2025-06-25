import requests
import json
import time
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

url ='https://api.zjzw.cn/web/api/?is_military_school=1&keyword=&page=2&province_id=&ranktype=&request_type=1&size=20&top_school_id=[589,3703,3117,2013,2466]&type=&uri=apidata/api/gkv3/school/lists&signsafe=ff2ebb56025572bf7a5e87a6533b7f8f'
header_info = '''Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: keep-alive
Cookie: aliyungf_tc=5e2e68bc8a6a05af8ec0d91395f235cc3a728e181b1aba23e4e45fa63a0092a2; acw_tc=ac11000117508286374662338e00a5e13036aaea1dcfda759b4408038339d7
Host: api.zjzw.cn
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0
sec-ch-ua: "Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"'''
MAX_PAGE = 1
json_name = '军校'

def parse_headers(header_string):
    """解析header字符串为字典格式"""
    headers = {}
    for line in header_string.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

def update_url_page(url, page):
    """更新URL中的page参数"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params['page'] = [str(page)]
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def crawl_data():
    """爬取数据的主函数"""
    headers = parse_headers(header_info)
    
    print(f"开始爬取数据，共{MAX_PAGE}页")
    
    for page in range(1, MAX_PAGE + 1):
        try:
            # 更新URL中的page参数
            current_url = update_url_page(url, page)
            
            print(f"正在爬取第{page}页...")
            
            # 发送请求
            response = requests.get(current_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 获取响应数据
            data = response.json()
            
            # 保存为JSON文件
            filename = f"{json_name}-{page}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"第{page}页数据已保存到 {filename}")
            
            # 限制请求频率：每秒一次
            if page < MAX_PAGE:  # 最后一页不需要等待
                time.sleep(1)
                
        except requests.exceptions.RequestException as e:
            print(f"请求第{page}页时发生错误: {e}")
            continue
        except json.JSONDecodeError as e:
            print(f"解析第{page}页JSON数据时发生错误: {e}")
            continue
        except Exception as e:
            print(f"处理第{page}页时发生未知错误: {e}")
            continue
    
    print("爬取完成！")

if __name__ == "__main__":
    crawl_data()

