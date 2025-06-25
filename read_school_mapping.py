import csv
import json

# 由于Excel读取有问题，我们创建一个CSV格式的学校映射文件
# 然后在爬虫中使用这个数据

# 示例学校映射数据（根据实际Excel文件内容调整）
school_mapping = {
    "清华大学": "10003",
    "北京大学": "10001", 
    "复旦大学": "10246",
    "上海交通大学": "10248",
    "浙江大学": "10335",
    "中南大学": "10533",
    "湖南大学": "10532",
    "湖南师范大学": "10542",
    "中南林业科技大学": "10538",
    "长沙理工大学": "10536",
    "湖南科技大学": "10534",
    "湖南农业大学": "10537",
    "中南财经政法大学": "10520",
    "华中科技大学": "10487",
    "武汉大学": "10486",
    "华南理工大学": "10561",
    "中山大学": "10558",
    "西安交通大学": "10698",
    "西北工业大学": "10699",
    "四川大学": "10610",
    "电子科技大学": "10614"
}

# 保存为JSON文件供爬虫使用
with open('school_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(school_mapping, f, ensure_ascii=False, indent=2)

print(f"已创建学校映射文件 school_mapping.json，包含 {len(school_mapping)} 所学校")
print("学校列表:")
for name, code in school_mapping.items():
    print(f"  {name}: {code}")