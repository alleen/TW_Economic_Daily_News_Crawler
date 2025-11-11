#!/usr/bin/env python3
"""RSS 功能完整測試 - 整合本地生成測試與 API endpoint 測試"""

import sys
import os
import requests

# 將父目錄加入 Python 路徑以便導入爬蟲模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from money_crawler import generate_money_rss
from global_crawler import generate_global_rss

def test_rss_generation():
    """測試 RSS 生成函數"""
    print("\n" + "=" * 60)
    print("📝 測試 1: RSS 生成函數")
    print("=" * 60)

    # 測試經濟日報 RSS 生成
    print("\n🔹 測試經濟日報 RSS 生成...")
    money_test_data = [
        {
            'title': '測試新聞：台股站穩2萬點',
            'publish_time': '2025-11-11 10:00',
            'reporter': '測試記者／台北報導',
            'content': '這是一則測試新聞的內容。台股今日表現亮眼...',
            'url': 'https://money.udn.com/money/story/12345/67890'
        }
    ]

    money_rss = generate_money_rss(money_test_data)

    if money_rss and ('<rss' in money_rss or '<?xml' in money_rss):
        print("✅ 經濟日報 RSS 生成成功")
        print(f"📊 包含 {len(money_test_data)} 則新聞")
        print(f"📦 RSS 大小: {len(money_rss)} bytes")
    else:
        print("❌ 經濟日報 RSS 生成失敗")
        return False    # 測試轉角國際 RSS 生成
    print("\n🔹 測試轉角國際 RSS 生成...")
    global_test_data = [
        {
            'title': '測試新聞：國際視野標題',
            'publish_time': '2025-11-11',
            'reporter': '轉角編輯部',
            'content': '這是一則轉角國際測試新聞的內容...',
            'url': 'https://global.udn.com/global_vision/story/8662/12345'
        }
    ]

    global_rss = generate_global_rss(global_test_data)

    if global_rss and ('<rss' in global_rss or '<?xml' in global_rss):
        print("✅ 轉角國際 RSS 生成成功")
        print(f"📊 包含 {len(global_test_data)} 則新聞")
        print(f"📦 RSS 大小: {len(global_rss)} bytes")
    else:
        print("❌ 轉角國際 RSS 生成失敗")
        return False

    print("\n📄 經濟日報 RSS Feed 預覽 (前 500 字元):")
    print("-" * 60)
    print(money_rss[:500])
    print("-" * 60)

    return True

def test_rss_endpoints():
    """測試 RSS API endpoints"""
    print("\n" + "=" * 60)
    print("📝 測試 2: RSS API Endpoints")
    print("=" * 60)

    endpoints = [
        ('經濟日報', 'http://127.0.0.1:5000/money/rss'),
        ('轉角國際', 'http://127.0.0.1:5000/global/rss')
    ]

    all_passed = True

    for name, url in endpoints:
        print(f"\n🔹 測試 {name} RSS endpoint...")
        print(f"   URL: {url}")

        try:
            response = requests.get(url, timeout=60)

            print(f"   ✅ HTTP 狀態碼: {response.status_code}")

            if response.status_code != 200:
                print(f"   ❌ 狀態碼錯誤")
                all_passed = False
                continue

            content_type = response.headers.get('Content-Type', 'N/A')
            print(f"   📝 Content-Type: {content_type}")
            print(f"   📦 回應大小: {len(response.text)} bytes")

            # 檢查是否為有效的 XML
            if response.text.startswith('<?xml') or response.text.startswith('<rss'):
                print("   ✅ 回應是有效的 RSS/XML 格式")

                # 計算新聞數量
                item_count = response.text.count('<item>')
                print(f"   📰 包含 {item_count} 則新聞")

                if item_count == 0:
                    print("   ⚠️  警告: RSS feed 中沒有新聞項目")

                # 顯示前幾行
                lines = response.text.split('\n')[:10]
                print(f"\n   📄 RSS Feed 前 10 行預覽:")
                print("   " + "-" * 56)
                for line in lines:
                    print(f"   {line}")
                print("   " + "-" * 56)

            else:
                print("   ❌ 回應不是 RSS/XML 格式")
                print("\n   前 500 字元:")
                print(response.text[:500])
                all_passed = False

        except requests.exceptions.Timeout:
            print(f"   ❌ 請求超時 - 伺服器可能正在爬取大量新聞")
            all_passed = False
        except requests.exceptions.ConnectionError:
            print(f"   ❌ 無法連接到伺服器")
            print("   � 請確認 Flask 伺服器是否正在運行 (python app.py)")
            all_passed = False
        except Exception as e:
            print(f"   ❌ 錯誤: {e}")
            all_passed = False

    return all_passed

def main():
    """執行所有測試"""
    print("\n🚀 開始執行 RSS 功能完整測試")
    print("=" * 60)

    # 測試 1: RSS 生成函數
    generation_passed = test_rss_generation()

    # 測試 2: RSS API endpoints
    endpoints_passed = test_rss_endpoints()

    # 總結
    print("\n" + "=" * 60)
    print("📊 測試結果總結")
    print("=" * 60)
    print(f"RSS 生成函數測試: {'✅ 通過' if generation_passed else '❌ 失敗'}")
    print(f"RSS API Endpoints 測試: {'✅ 通過' if endpoints_passed else '❌ 失敗'}")
    print("=" * 60)

    if generation_passed and endpoints_passed:
        print("\n✅ 所有測試通過！")
        return 0
    else:
        print("\n❌ 部分測試失敗，請檢查上述錯誤訊息")
        return 1

if __name__ == '__main__':
    sys.exit(main())

