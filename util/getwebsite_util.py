import requests
from bs4 import BeautifulSoup
import json

url = "https://www.toolify.ai/category/3d-model-generator"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

data = []
# 使用更精确的选择器来匹配目标元素
for tool_div in soup.select('div[class*="flex-1 bg-white"]'):
    # 查找名称元素
    name_div = tool_div.select_one('div[class*="text-xl font-semibold"]')
    # 查找URL元素 - 使用go-tool-detail-name类
    url_element = tool_div.select_one('a.go-tool-detail-name')
    
    # 提取链接并清理URL
    full_url = tool_div.select_one('a[class*="flex-shrink-0 ml-3"]').get('href')
    
    # 跳过Chrome网上应用店的链接
    if 'chromewebstore.google.com' in full_url:
        continue
        
    # 移除查询参数和协议前缀
    link_url = full_url.split('?')[0] if '?' in full_url else full_url
    link_url = link_url.replace('https://', '').replace('http://', '')
    
    # 只保留主域名（第一个斜杠之前的部分）
    link_url = link_url.split('/')[0]
    
    # 移除 www. 前缀（如果存在）
    link_url = link_url.replace('www.', '')
    
    # 重新添加https://前缀
    link_url = 'https://' + link_url
    
    name = name_div.text.strip()
    # 去除重复数据
    if {"name": name, "url": link_url} not in data:
        data.append({"name": name, "url": link_url})

# 按名称排序并以JSON格式输出结果
print(json.dumps(data, ensure_ascii=False, indent=2))
