# httpRandomMusic
本项目能让你的小爱音箱播放局域网NAS上的音乐  
因为小爱play增强版的BES2300太垃圾了，曲库没一首歌能够完整放完的  

当然了这个程序还能配合esp8266或esp32作为随机的音乐电台

### 如何部署
在你的nas上安装Python3，下载并打开`httpRandomMusic.py`，编辑`fileDir`变量，填写你存放音乐的文件夹的完整路径  
如果你是Windows服务器，那你的路径可能是`E:\音乐`的，要把`\`换成`/`  
然后修改路由器的hosts，加入这样一行
```
你服务器的ip op.lan
```
就算你使用别的方式也好，只要将`op.lan`这个不存在的域名在你局域网解析到你的服务器就行了
然后启动程序
```
# 正常是这样启动的
python3 httpRandomMusic.py
# Windows可能是这样的
python httpRandomMusic.py
```

### 如何使用
```
小爱同学
打开小怪
```
然后以下三条指令三选一
|指令|功能|
|----|----|
|播放服务器的音乐|按着上次的进度继续播放（没有进度就是从头放）|
|从头播放服务器的音乐|按修改时间倒序播放（先放最后放进文件夹的文件）|
|随机播放服务器的音乐|随机播放（播放列表打乱，不会重复随机到同一首）|

### FAQ
Q:为什么不做文件名搜索功能？  
A:因为与技能的网抑云歌曲搜索功能冲突（搜索xxx，播放xxx），以及这只是个附属功能，小爱同学只支持中文语音识别，所以搜索非常局限  

Q:为什么只支持一层文件夹内文件播放？  
A:因为没有写多层文件夹文件扫描，以及加快扫描速度，欢迎PR  

Q:怎么放不出声音？  
A:文件格式不支持，BES2300的音响性能太差大概只能放mp3（印着xiaomi的小爱音响play和play增强版）

