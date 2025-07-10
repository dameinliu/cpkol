from tikapi import TikAPI, ValidationException, ResponseException
from dotenv import load_dotenv
import os
import json

load_dotenv()

api = TikAPI(os.getenv("TIKAPI_API_KEY"))

def save_json(data, page):
    # 保存为 search_result_page1.json, search_result_page2.json ...
    filename = f"search_result_page{page}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存: {filename}")

def fetch_and_save_all(query, category="general"):
    try:
        page = 1
        response = api.public.search(category=category, query=query)
        while response:
            data = response.json()
            save_json(data, page)
            next_cursor = data.get("nextCursor")
            if not next_cursor:
                break
            if page > 2:
                break
            print("Getting next items", next_cursor)
            response = response.next_items()
            page += 1
    except Exception as e:
        print("发生错误：", e)

if __name__ == "__main__":
    fetch_and_save_all("แมว")  # 这里可以换成你要搜索的关键词