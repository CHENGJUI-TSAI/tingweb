import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_ee_info():
    url = "http://nfuee.nfu.edu.tw/"
    response = requests.get(url, verify=False)
    response.encoding = 'utf-8'  # 確保編碼正確

    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # 收集數據
    news_list = []

    # 提取最新動態
    print("=== 最新動態 ===")
    h2_tags = soup.find_all('h2')
    for h2 in h2_tags:
        a_tag = h2.find('a')
        if a_tag and a_tag.text.strip():
            title = a_tag.text.strip()
            href = a_tag['href']
            if not href.startswith('http'):
                href = url.rstrip('/') + href
            print(title)
            # 添加到列表
            news_list.append({'標題': title})

    # 保存到Excel
    if news_list:
        try:
            df = pd.DataFrame(news_list)
            df.to_excel('results.xlsx', index=False)
            print("結果已保存到 results.xlsx")
        except PermissionError:
            print("無法保存到 results.xlsx，請確保檔案未被打開。")

if __name__ == "__main__":
    crawl_ee_info()