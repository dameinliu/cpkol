from tikapi import TikAPI, ValidationException, ResponseException

api = TikAPI("fQ6AYAyM4V3yGXyAAgQUeK8XieOpugNZxyKqY1dHTgxPN2VT")

try:
    response = api.public.explore(
        session_id=1,  # ✅ 唯一、有效
        region="US",            # 可换为 "TH", "VN", "ID", "MY" 等
        language="en"           # TikTok 显示语言
    )
    data = response.json()
    # print(data)
    for post in data.get("itemList", []):
        print(post.get("desc", "No description available"))
    
except ValidationException as e:
    print(f"参数校验失败: {e}, 字段: {e.field}")

except ResponseException as e:
    print(f"TikAPI 响应异常: {e}, 状态码: {e.response.status_code}")
