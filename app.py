from flask import Flask, jsonify, render_template, Response, request, abort
from flask_cors import CORS

from money_crawler import scrape_money_news, generate_money_rss
from global_crawler import scrape_global_news, generate_global_rss

app = Flask(__name__)
CORS(app)

# 中間件：限制只接受來自 127.0.0.1 的請求
@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    if client_ip != '127.0.0.1':
        abort(403)  # 拒絕非本地請求

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/money')
def money_page():
    return render_template('money.html')

@app.route('/global')
def global_page():
    return render_template('global.html')

@app.route('/money/scrape', methods=['GET'])
def scrape():
    news_data = scrape_money_news()
    return jsonify(news_data)

@app.route('/money/rss', methods=['GET'])
def money_rss():
    news_data = scrape_money_news()
    rss_xml = generate_money_rss(news_data)
    return Response(rss_xml, mimetype='application/rss+xml')

@app.route('/global/scrape', methods=['GET'])
def global_scrape():
    news_data = scrape_global_news()
    return jsonify(news_data)

@app.route('/global/rss', methods=['GET'])
def global_rss():
    news_data = scrape_global_news()
    rss_xml = generate_global_rss(news_data)
    return Response(rss_xml, mimetype='application/rss+xml')

# 主程式入口
if __name__ == '__main__':
    # 只監聽 127.0.0.1，不接受外部連線
    app.run(host='127.0.0.1', port=3322)