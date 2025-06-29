import requests
import json
import time
import re
import requests
import urllib3
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from tk_base_utils import get_current_dir_path

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 创建自定义SSL上下文
class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

url ='https://ks.hneao.cn/gaokao/v1/volunteer/yxjhk/zyzpage?pageSize=10000&pageNo=1&tbrcdm=12&pcdm=3&kldm=2&jhxzdm=0&jhlbdm=00&zylxdm=1&secondSubject2=0&secondSubject3=000&lqpc=3&jhkl=2&jhxz=0&jhlb=00&yxdh=1101&_=1751158067867'
header_info = '''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Connection: keep-alive
Cookie: BIGipServerpool_xgk_student=696521388.893.0000; LOGIN_USER_TYPE=student; C2AT=eyJraWQiOiJHcHJkcm5ualJ0V1hBSmpIbDctcnR3IiwidHlwIjoiSldUIiwiYWxnIjoiUlMyNTYifQ.eyJhYyI6IjEzMjM3MzkyNjUyIiwic2V4IjoiMSIsImlzcyI6ImMyIiwib3JnaW5zaWRzIjpbXSwib2lkIjpbXSwidWlkIjoiZjk0M2U0Y2JiOWM1NDNiNjk3MmUzZGRhYzZjZWFiZWIiLCJjZXIiOiI0MzA1MjgyMDA3MDQxODYxNTgiLCJjZXJ0eXBlIjoib3RoZXIiLCJwaG9uZSI6IjEzMjM3MzkyNjUyIiwibmFtZSI6IuiwreW_l-S4nCIsIndubyI6IjA1MjUxNTcwIiwiZXhwIjoxNzUyNDA5MTIyLCJhaWQiOiJXMWVzWTd6YVNrNndjR3FmdkhMNWx3Iiwicm8iOlsiZGVmYXVsdCJdLCJpYXQiOjE3NTExMTMxMjIsImNpZCI6W119.L-7WFVsamMpKm8ORnQfrV_7LGfC1HcnaaxAj5FZeXbj0sZOppg5HAYu0viILIXk06m2xB4Q4-1B5ZGUEqh5s8F7Pp277dMiHV-sQVvi_M_E4NNCBGdh-zRIa0JYYARzmOL2E84P_qLYEEA982P8wBPNyCW3NEoNnWqDFDSxgYSQ; C2RT=f943e4cbb9c543b6972e3ddac6ceabeb.71bd008abaed688a8e39fdfe2c82161e; USER_GXQY_ALL=z56oBf7CaDpka4kpJXEElix2FTdOwyaPZuktxrpwVk3PH2w9SaSqnVYsHfQVFgpR2eo6cPPfZGoYJvCu7iIt8RUBB1pvzzGGO1kLiwXfiJlTtGb6j14WI09neVeo+RBCcnS93MwgXcwnSvpGnpt6dp0izMCLGrS2YuPOhfJNRbvEdNAoS/7wzXA8CLBTE5cSI6gN8oDjfAI+zMJnyGbTVw==
Host: ks.hneao.cn
Referer: https://ks.hneao.cn/student/volunteer/volunteerSystem/yxjhcx?dataId=MxUAZZjkRBSjFptzGQZ67g
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0
X-Requested-With: XMLHttpRequest
platform: student
sec-ch-ua: "Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"'''
MAX_PAGE = 1
json_name = '专业组信息'

def parse_headers(header_string):
    """解析header字符串为字典格式"""
    headers = {}
    for line in header_string.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    return headers

def update_url_page(url, yxdh):
    """更新URL中的page参数"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params['yxdh'] = [str(yxdh)]
    query_params['_'] = [str(int(time.time()*1000))]
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def get_yxdh_mapping():
    """获取学校代号映射
    从temp_school_info目录下读取所有JSON文件，提取yxdh和yxmc字段
    返回字典：{yxdh: yxmc}
    """
    yxdh_mapping = {}
    current_dir = get_current_dir_path()
    school_info_dir = current_dir.parent/'temp_school_info'
    
    # 确保目录存在
    if not school_info_dir.exists():
        print(f"目录不存在: {school_info_dir}")
        return yxdh_mapping
    print(f"读取学校信息目录: {school_info_dir}")
    # 遍历目录中的所有JSON文件
    for json_file in school_info_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 检查JSON结构
                if 'result' in data and 'records' in data['result']:
                    for school in data['result']['records']:
                        if 'yxdh' in school and 'yxmc' in school:
                            yxdh_mapping[school['yxdh']] = school['yxmc']
        except Exception as e:
            print(f"处理文件 {json_file.name} 时出错: {e}")
    
    print(f"共读取到 {len(yxdh_mapping)} 所学校的信息")
    return yxdh_mapping


def crawl_data():
    """爬取数据的主函数"""
    headers = parse_headers(header_info)
    
    # 创建会话并配置SSL适配器
    session = requests.Session()
    
    # 配置重试策略
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    # 挂载SSL适配器
    adapter = SSLAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    yxdh_mapping = get_yxdh_mapping()

    print(f"开始爬取数据，共{len(yxdh_mapping)}页")
    count = 0
    success_count = 0
    fail_school = []
    for yxdh, yxmc in yxdh_mapping.items():
        try:
            # 更新URL中的page参数
            current_url = update_url_page(url, yxdh)
            
            print(f"正在爬取{yxmc}...")
            
            # 发送请求，使用配置好的会话
            response = session.get(
                current_url, 
                headers=headers, 
                timeout=30,
                verify=False,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # 获取响应数据
            data = response.json()
            
            # 保存为JSON文件
            filename = f"{yxmc}.json"
            current_dir = get_current_dir_path()
            file_path = current_dir.parent/'temp_zyz_info'
            file_path.mkdir(parents=True, exist_ok=True)
            full_file_name = file_path/filename
            with open(full_file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            success_count += 1
            count += 1
            print(f"{yxmc}名称,代号{yxdh}数据已保存到 {full_file_name}")
            print(f'共{len(yxdh_mapping)}条,已完成{count}条,成功{success_count}条')
            # 限制请求频率：每秒一次
            if count < len(yxdh_mapping):  # 最后一页不需要等待
                time.sleep(1)
                
        except requests.exceptions.RequestException as e:
            print(f"请求{yxmc}时发生错误: {e}")
            fail_school.append(yxmc)
            continue
        except json.JSONDecodeError as e:
            print(f"解析{yxmc}JSON数据时发生错误: {e}")
            fail_school.append(yxmc)
            continue
        except Exception as e:
            print(f"处理{yxmc}时发生未知错误: {e}")
            fail_school.append(yxmc)
            continue
    
    print("爬取完成！")

if __name__ == "__main__":
    crawl_data()

