# 关于本项目

## 1. 想要做什么 
1. AI聊天机器人 **支持图片/文字 甚至是语音(tts/asr）**
2. 可能还有一点 **使用live2D**
3. 与其他搜索引擎的对接 **目前想法是使用高并发爬虫**
4. Qt界面 **用PyQt5** (小黑窗虽然实用 但是太丑了)


## 2. 目前的进度：
- [ ] 登录注册等操作(需要记录用户信息 也许可以不写 
    => 在初次打开应用时提供一个接口 用于指引申请API Key，建议使用aihubmix但不强求
    **重点只在于需要用户自行提供API Key 和 Base URL**)
- [ ] (理论上可能)需要数据库 => 阿里云 部署linux主机 TCP/IP编程 Gin服务器
- [ ] OpenAI及其他AI对接
- [x] Spark AI对接
- [ ] (如果可能)加入自己的AI模型
- [ ] 高并发爬虫
- [ ] ui界面
- [x] 机器人对话 文字
- [ ] 机器人对话 图片
- [ ] 机器人对话 语音

## 3. API接口网址
- [Spark AI](https://www.xfyun.cn/doc/platform/xfyunreadme.html)
- [Langchain](https://python.langchain.ac.cn/docs/how_to/)
- [AIhubmix](https://doc.aihubmix.com/) => 我的评价是没啥用

## 4. 其他
- [ ] 代码规范
- [ ] 代码注释
- [ ] 代码测试
- [ ] 代码优化
- [ ] 代码打包
- [ ] 代码部署
- [ ] 代码维护