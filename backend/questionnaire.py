from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# 允许本地所有端口的跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://127.0.0.1", "http://localhost:*", "http://127.0.0.1:*", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import tomli
with open('settings.toml', 'rb') as f:
    LOG_DIR = tomli.load(f).get('log_dir', 'log')
os.makedirs(LOG_DIR, exist_ok=True)
INFO_TSV_PATH = os.path.join(LOG_DIR, "info.tsv")

@app.post("/submit")
async def submit_json(request: Request):
    # 直接接收JSON数据
    data = await request.json()
    # 检查必需字段
    required_fields = [
        "id", "name", "age", "gender", "major", "grade", "aiFrequency", "aiAttitude", "time"
    ]
    for field in required_fields:
        if field not in data:
            return JSONResponse({"status": "error", "msg": f"缺少字段: {field}"}, status_code=400)
    # 检查info.tsv是否存在，若不存在则写入表头
    write_header = not os.path.exists(INFO_TSV_PATH)
    # 以追加模式写入TSV
    with open(INFO_TSV_PATH, "a", encoding="utf-8") as f:
        if write_header:
            f.write('\t'.join(required_fields) + '\n')
        f.write('\t'.join([str(data[k]).replace('\t', ' ') for k in required_fields]) + '\n')
    return JSONResponse({"status": "success", "filename": "info.tsv"})

if __name__ == "__main__":
    import uvicorn
    print("启用表单存储(接收JSON)...")
    uvicorn.run(app, host="0.0.0.0", port=8764)
