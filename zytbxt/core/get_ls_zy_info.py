import requests
import json
import time
import re
import requests
from sqlalchemy.orm import query
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

url ='https://ks.hneao.cn/gaokao/v1/zymk/lnfsxzy/queryLnsjZyPage?pageSize=100&pageNo=1&nf=2024&yxdh=1101&zyzdm=0100004500105&zyzbh=105&pcdm=3&_=1751177072574'
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

def update_url_page(url, nf,yxdh,zyzdm,zyzbh):
    """更新URL中的page参数"""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    query_params['nf'] = [str(nf)]
    query_params['yxdh'] = [str(yxdh)]
    query_params['zyzdm'] = [str(zyzdm)]
    query_params['zyzbh'] = [str(zyzbh)]
    query_params['_'] = [str(int(time.time()*1000))]
    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))

def get_query_mapping():
    """获取查询参数映射
    从temp_ls_zy_info目录下读取所有JSON文件，提取 nf,yxdh,zyzdm,zyzbh,yxmc字段
    返回list[dict]：[{'nf': nf, 'yxdh': yxdh, 'zyzdm': zyzdm, 'zyzbh': zyzbh,'yxmc': yxmc}]
    """
    current_dir = get_current_dir_path()
    school_info_dir = current_dir.parent/'temp_ls_zyz_info'
    
    # 确保目录存在
    if not school_info_dir.exists():
        print(f"目录不存在: {school_info_dir}")
        return []
    print(f"读取学校信息目录: {school_info_dir}")
    # 准备结果列表
    result_list = []
    fail_list = []
    # 遍历目录中的所有JSON文件
    for json_file in school_info_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 检查JSON结构
                # 提取学校记录
                records = data["result"]["records"]

                for school in records:
                    # 学校基本信息
                    school_info = {
                        key: value for key, value in school.items()
                        if key != "yxNfZyzVoList" and key != "yxnfList"
                    }
                    
                    # 处理专业组信息
                    for program in school["yxNfZyzVoList"]:
                        # 合并学校信息和专业组信息
                        combined = {**school_info, **program}
                        result_list.append(combined)
        except Exception as e:
            print(f"处理文件 {json_file.name} 时出错: {e}")
            fail_list.append(json_file.name)
    
    print(f"共读取到 {len(result_list)} 条专业组的信息,失败{len(fail_list)}条")
    if fail_list:
        print(f"失败文件列表: {fail_list}")
        with open(current_dir.parent/'temp_ls_zyz_info_fail.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(fail_list))
    return result_list



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
    
    query_mapping = get_query_mapping()

    print(f"开始爬取数据，共{len(query_mapping)}条")
    count = 0
    success_count = 0
    fail_school = []
    for temp_dict in query_mapping:
        try:
            # 保存为JSON文件
            filename = f"{temp_dict['nf']}-{temp_dict['yxmc']}-{temp_dict['zyzdm']}-{temp_dict['zyzbh']}.json"
            current_dir = get_current_dir_path()
            file_path = current_dir.parent/'temp_ls_zy_info'
            file_path.mkdir(parents=True, exist_ok=True)
            full_file_name = file_path/filename
            if full_file_name.exists():
                print(f"{temp_dict['nf']}年{temp_dict['yxmc']}的{temp_dict['zyzdm']}{temp_dict['zyzbh']}专业组数据已存在,跳过")
                count += 1
                success_count += 1
                continue


            # 更新URL中的page参数
            current_url = update_url_page(url, temp_dict['nf'],temp_dict['yxdh'],temp_dict['zyzdm'],temp_dict['zyzbh'])
            
            print(f"正在爬取{temp_dict['nf']}年{temp_dict['yxmc']}的{temp_dict['zyzdm']}{temp_dict['zyzbh']}专业组...")

            
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
            

            with open(full_file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            success_count += 1
            count += 1
            print(f"{temp_dict['nf']}年{temp_dict['yxmc']}院校代码,专业组{temp_dict['zyzdm']}数据已保存到 {full_file_name}")
            print(f'共{len(query_mapping)}条,已完成{count}条,成功{success_count}条')
            # 限制请求频率：每秒一次
            if count < len(query_mapping):  # 最后一页不需要等待
                time.sleep(1)
                
        except requests.exceptions.RequestException as e:
            print(f"请求{temp_dict['nf']}年{temp_dict['yxmc']}-{temp_dict['zyzdm']}时发生错误: {e}")
            fail_school.append(temp_dict)
            continue
        except json.JSONDecodeError as e:
            print(f"解析{temp_dict['nf']}年{temp_dict['yxmc']}-{temp_dict['zyzdm']}JSON数据时发生错误: {e}")
            fail_school.append(temp_dict)
            continue
        except Exception as e:
            print(f"处理{temp_dict['nf']}年{temp_dict['yxmc']}-{temp_dict['zyzdm']}时发生未知错误: {e}")
            fail_school.append(temp_dict)   
            continue
    print(f'共{len(query_mapping)}条,失败{len(fail_school)}条,失败数据:{fail_school}')
    print("爬取完成！")

if __name__ == "__main__":
    crawl_data()

