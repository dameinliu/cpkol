from tikapi import TikAPI
import os
from dotenv import load_dotenv

# 加载.env配置
load_dotenv()

# 创建 TikAPI 客户端实例
api = TikAPI(os.getenv("TIKAPI_API_KEY"))
api.set(
    __options__={
        'params':{
			'accountKey':{
				'name': 'X-Account-Key',
				'help': "The Account Key is invalid.",
				'location': "headers",
				'validate': "^[a-zA-Z0-9]{10,}$"
			}
        }
    }
)