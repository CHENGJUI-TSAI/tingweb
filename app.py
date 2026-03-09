from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_news():
    url = "http://nfuee.nfu.edu.tw/"
    response = requests.get(url, verify=False)
    response.encoding = 'utf-8'

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    news_list = []

    h2_tags = soup.find_all('h2')
    for h2 in h2_tags:
        a_tag = h2.find('a')
        if a_tag and a_tag.text.strip():
            title = a_tag.text.strip()
            href = a_tag['href']
            if not href.startswith('http'):
                href = url.rstrip('/') + href
            news_list.append({'title': title, 'link': href})

    return news_list

@app.route('/')
def index():
    news = get_news()
    return render_template('index.html', news=news)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')

    news = get_news()
    relevant_news = []

    # 檢查每個新聞是否相關
    for item in news:
        if any(keyword in item['title'] for keyword in user_message.split()):
            relevant_news.append(item)

    if relevant_news:
        response = "根據你的問題，以下是相關資訊：<br>" + "<br>".join([f"{item['title']} - <a href='{item['link']}' target='_blank'>查看詳情</a>" for item in relevant_news])
    else:
        response = "抱歉，我沒有找到相關資訊。請試試其他關鍵字，如「獎學金」或「公告」。"

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)