#!/usr/bin/env python3
"""測試所有 API 端點"""

import requests
import sys

def test_endpoint(url, name, expected_content_type=None):
    """測試單一端點"""
    print(f"\n{'='*60}")
    print(f"測試: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")

    try:
        response = requests.get(url, timeout=5)
        print(f"✅ 狀態碼: {response.status_code}")
        print(f"📝 Content-Type: {response.headers.get('Content-Type', 'N/A')}")

        if expected_content_type:
            if expected_content_type in response.headers.get('Content-Type', ''):
                print(f"✅ Content-Type 正確")
            else:
                print(f"⚠️  Content-Type 不符合預期")

        # 顯示回應的前幾個字元
        preview = response.text[:200].replace('\n', ' ')
        print(f"📄 回應預覽: {preview}...")

        return True

    except requests.exceptions.Timeout:
        print(f"❌ 請求超時")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ 無法連接")
        return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("開始測試所有端點")
    print("="*60)

    base_url = "http://127.0.0.1:3322"

    tests = [
        (f"{base_url}/", "首頁", "text/html"),
        (f"{base_url}/money/scrape", "Money Scrape (JSON)", "application/json"),
        (f"{base_url}/money/rss", "Money RSS Feed", "application/rss+xml"),
    ]

    results = []
    for url, name, content_type in tests:
        result = test_endpoint(url, name, content_type)
        results.append((name, result))

    # 總結
    print("\n" + "="*60)
    print("測試總結")
    print("="*60)

    for name, result in results:
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"{status} - {name}")

    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n總計: {passed}/{total} 個測試通過")

    if passed == total:
        print("\n🎉 所有測試通過！")
        return 0
    else:
        print(f"\n⚠️  有 {total - passed} 個測試失敗")
        return 1

if __name__ == '__main__':
    sys.exit(main())
