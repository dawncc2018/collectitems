import requests
import datetime
import os
import re
import base64

# 基础URL模板
BASE_URL_TEMPLATE = "https://node.freeclashnode.com/uploads/{year}/{month:02d}/{num}-{year}{month:02d}{day:02d}.txt"

# 输出文件路径
OUTPUT_FILE = "merged_links.txt"

def get_today_date():
    today = datetime.date.today()
    return today.year, today.month, today.day

def build_url(year, month, day, num):
    return BASE_URL_TEMPLATE.format(year=year, month=month, day=day, num=num)

def fetch_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Referer": "https://node.freeclashnode.com/"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"获取URL失败: {url}, 错误: {e}")
        return ""

def extract_links(content):
    try:
        decoded_content = base64.b64decode(content).decode('utf-8')
        if len(decoded_content) > 10:
            content = decoded_content
    except:
        pass
    
    links = []
    protocols = ['vless://', 'trojan://', 'ss://', 'ssr://', 'vmess://']
    
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        for protocol in protocols:
            if protocol in line:
                links.append(line)
                break
    
    return links

def merge_links(links):
    unique_links = list(set(links))
    return '\n'.join(unique_links)

def save_to_file(content, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"链接已保存到: {file_path}")

def generate_github_link(file_path):
    repo_owner = "dawncc2018"
    repo_name = "collectitems"
    branch = "main"
    file_path_in_repo = os.path.basename(file_path)
    
    github_link = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{branch}/{file_path_in_repo}"
    print(f"GitHub链接: {github_link}")
    return github_link

def main():
    print("开始提取和合并链接...")
    
    year, month, day = get_today_date()
    print(f"使用日期: {year}-{month:02d}-{day:02d}")
    
    all_links = []
    
    for num in range(5):
        url = build_url(year, month, day, num)
        print(f"构建的URL (num={num}): {url}")
        
        content = fetch_content(url)
        
        if content:
            links = extract_links(content)
            print(f"num={num} 提取到 {len(links)} 个链接")
            all_links.extend(links)
        else:
            print(f"num={num} 未能获取到内容")
    
    if not all_links:
        print("未提取到任何链接，程序退出。")
        return
    
    print(f"\n总共提取到 {len(all_links)} 个链接")
    
    merged_content = merge_links(all_links)
    
    save_to_file(merged_content, OUTPUT_FILE)
    
    github_link = generate_github_link(OUTPUT_FILE)
    
    print("\n任务完成！")
    print(f"本地文件: {os.path.abspath(OUTPUT_FILE)}")
    print(f"GitHub链接: {github_link}")

if __name__ == "__main__":
    main()
