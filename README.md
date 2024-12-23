# 关于本项目

### 请注意 本项目基于Python3.10开发 其他版本可能不支持


#### 目前正在进行TTS和ASR的开发
综合体验下来，我个人更喜欢FunASR和coquiTTS，这两个都是开源的，并且效果也不错，索性直接拿来做了。
代码已经clone下来了，另附原文链接：
- [FunASR](https://github.com/modelscope/FunASR)
- [coquiTTS](https://github.com/coqui-ai/TTS)

## 1. 想要做什么 
> 1. AI聊天机器人 **支持图片/文字 甚至是语音(tts/asr)**
> 2. 可能还有一点 **使用live2D**
> 3. 与其他搜索引擎的对接 **QtWebEngine组件**
> 4. Qt界面 **用PyQt5** (小黑窗虽然实用 但是太丑了) **后续如果性能提升 将使用C++**
> 5. 开放wss协议 => 不要只用http协议 **比较耗资源** (针对SparkAI)


## 2. 目前的进度：
- [ ] 在初次打开应用时提供一个接口 用于指引申请API Key，建议使用aihubmix但不强求 **重点只在于需要用户自行提供API Key 和 Base URL**
- [x] ollama本地模型对接 => **支持自定义本地模型，需要在Python内部写shell脚本装ollama以及本地大模型** 看情况 网络服务器并不需要这样(写脚本装ollama)
- [x] AI对接
- [x] 机器人对话 文字
- [x] 机器人对话 语音 => 针对于 Ollama 本地大模型 和 其他AI 的 模型 已经基本完工
- [x] 多轮聊天
- [x] TTS
- [ ] ASR
- [ ] 部署到Docker **不知道什么问题 比较麻烦**
- [ ] ZeroMQ, RabbitMQ选一个 **用于网络服务器**
- [ ] Redis 可能会用得上
- [ ] (如果可能)加入自己的AI模型
- [ ] ui界面
- [ ] live2D模型


## 3. 其他
- [x] 代码规范
- [x] 代码注释
- [x] 代码测试
- [ ] 代码优化
- [ ] 代码打包
- [ ] 代码部署
- [ ] 代码维护


## 个人最新的想法：
1. [x] 开发重心在于ollama本地模型(免费)
2. [x] 暂时放弃多模态功能 (不支持图片上传)
3. [ ] 是否还需要考虑添加删除大模型的功能？
4. [x] 多协程创建聊天文件需要带上token
5. [ ] 数据库可以使用mysql： 
        预设表的字段是: id[int]=>, model[varchar], prompt[varchar]=>给llm预设的人格/提示词等, filepath[varchar]=> 聊天记录的文件路径, time[datetime], user[varchar]=> 用户(将成为btree主键)


## 可以优化的算法
- [x] logger第一轮直接初始化
- [x] 有选择性地导包 (比如使用localAI时不导入webAI)


## 可能需要解决的地方
- [ ] logger毕竟是控制台玩物，真做成了Qt就都得删了


## 可供参考的网页：
- [Ollama-python](https://github.com/ollama/ollama-python/tree/main/examples)
- [Ollama-blog](https://ollama.org.cn/blog/)
- [batch-learning](https://blog.csdn.net/csfchh/article/details/106795352)
- [Spark AI](https://www.xfyun.cn/doc/platform/xfyunreadme.html)
- [Langchain](https://python.langchain.ac.cn/docs/how_to/)
- [FunASR](https://github.com/modelscope/FunASR)
- [coquiTTS](https://github.com/coqui-ai/TTS)
- [AIhubmix](https://doc.aihubmix.com/) => 没啥用