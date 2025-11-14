import requests
from datetime import datetime
from email.utils import formatdate
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

def scrape_global_news():
    base_url = 'https://global.udn.com/global_vision/cate/120868'
    response = requests.get(base_url)
    response.encoding = 'utf-8'

    # 檢查請求是否成功
    if response.status_code == 200:
        # 解析HTML內容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找出所有<a>標籤，並篩選出符合條件的URL
        links = soup.find_all('a')
        story_urls = set()
        for link in links:
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                if full_url.startswith('https://global.udn.com/global_vision/story'):
                    # 移除 query string 參數
                    clean_url = full_url.split('?')[0]
                    story_urls.add(clean_url)

        # 初始化，用於儲存新聞資訊
        news_data = []

        # 爬取每個新聞的內容
        for story_url in story_urls:
            story_response = requests.get(story_url)
            story_response.encoding = 'utf-8'
            if story_response.status_code == 200:
                story_soup = BeautifulSoup(story_response.text, 'html.parser')

                # 爬取標題
                title_tag = story_soup.find('h1', class_='article-content__title')
                title = title_tag.get_text(strip=True) if title_tag else 'N/A'

                # 爬取發布時間
                time_tag = story_soup.find('div', class_='article-content__authors-mark')
                publish_time = time_tag.get_text(strip=True) if time_tag else 'N/A'

                # 爬取報導者
                reporter_tag = story_soup.find('p', class_='article-content__authors-name')
                reporter = reporter_tag.get_text(strip=True) if reporter_tag else 'N/A'

                # 爬取內文
                content_tag = story_soup.find('section', class_='article-content__editor')
                paragraphs = content_tag.find_all('p') if content_tag else []
                content = '\n'.join(p.get_text(strip=True) for p in paragraphs)

                # 過濾：如果任何必要欄位為空或 'N/A'，則跳過此新聞
                if not (title and title != 'N/A' and
                        publish_time and publish_time != 'N/A' and
                        reporter and reporter != 'N/A' and
                        content and content.strip()):
                    continue

                # 將爬取到的內容存入字典
                news_item = {
                    'title': title,
                    'publish_time': publish_time,
                    'reporter': reporter,
                    'content': content,
                    'url': story_url
                }
                news_data.append(news_item)
        return news_data
    else:
        return []

def generate_global_rss(news_data):
    """將全球新聞資料轉換成 RSS 2.0 格式"""
    # 建立 RSS 根元素
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

    # 建立 channel 元素
    channel = ET.SubElement(rss, 'channel')

    # 添加頻道資訊
    title = ET.SubElement(channel, 'title')
    title.text = '轉角國際 - 全球視野'

    link = ET.SubElement(channel, 'link')
    link.text = 'https://global.udn.com/global_vision/cate/120868'

    description = ET.SubElement(channel, 'description')
    description.text = '轉角國際全球視野新聞'

    language = ET.SubElement(channel, 'language')
    language.text = 'zh-TW'

    last_build_date = ET.SubElement(channel, 'lastBuildDate')
    last_build_date.text = formatdate(timeval=None, localtime=False, usegmt=True)

    # 添加每則新聞為 item
    for news in news_data:
        # 過濾：確保所有必要欄位都有效
        title = news.get('title', '')
        publish_time = news.get('publish_time', '')
        reporter = news.get('reporter', '')
        content = news.get('content', '')

        if not (title and title != 'N/A' and
                publish_time and publish_time != 'N/A' and
                reporter and reporter != 'N/A' and
                content and content.strip()):
            continue

        item = ET.SubElement(channel, 'item')

        item_title = ET.SubElement(item, 'title')
        item_title.text = title

        item_link = ET.SubElement(item, 'link')
        item_link.text = news.get('url', '')

        item_description = ET.SubElement(item, 'description')
        # 組合報導者和內文
        desc_text = f"<p><strong>報導者：</strong>{reporter}</p>"
        desc_text += f"<p>{content}</p>"
        item_description.text = desc_text

        item_pub_date = ET.SubElement(item, 'pubDate')
        # 嘗試解析發布時間並轉換為 RFC 822 格式
        try:
            # 如果有發布時間，使用它；否則使用當前時間
            if publish_time and publish_time != 'N/A':
                item_pub_date.text = publish_time
            else:
                item_pub_date.text = formatdate(timeval=None, localtime=False, usegmt=True)
        except:
            item_pub_date.text = formatdate(timeval=None, localtime=False, usegmt=True)

        item_guid = ET.SubElement(item, 'guid', isPermaLink='true')
        item_guid.text = news.get('url', '')

    # 轉換為字串
    tree = ET.ElementTree(rss)
    ET.indent(tree, space='  ', level=0)

    # 生成 XML 字串，包含 XML 聲明
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rss_content = ET.tostring(rss, encoding='unicode', method='xml')

    return xml_declaration + rss_content
