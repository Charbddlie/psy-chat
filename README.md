<div align="center">
  <img src='psy-front\public\favicon.ico' width="30%"/>

  # Psy Chat

  一个开源的心理学测试平台，支持流式AI对话，前后测问卷收集
  ## 启动
</div>

```
cd backend
python main.py
# 不论开发还是部署都需要启动后端服务
```

```
cd psy-front

# 开发
npm run serve
# 修改会实时显示到
# 访问显示的链接就能正常做题，但是占用比较高

# 或部署
# 占用小性能高，修改页面后需要重新build
# 此处build默认访问的后端地址在 psy-front\.env.production 中定义，如果build后在本地运行或者要上传到不同服务器都需要修改
npm run build
cd dist
python -m http.server 8080
```
