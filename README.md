# httpRandomMusic
本项目能让你的小爱音箱播放局域网NAS上的音乐  
因为小爱play增强版的BES2300太垃圾了，曲库没一首歌能够完整放完的  

当然了这个程序还能配合esp8266或esp32作为随机的音乐电台

### 如何部署
在你的nas上安装Python3，下载并打开`httpRandomMusic.py`，编辑`fileDir`变量，填写你存放音乐的文件夹的完整路径  
如果你是Windows服务器，那你的路径可能是`E:\音乐`的，要把`\`换成`/`  

如果您需要在线转码，请修改`ffmpeg`变量，填写你的ffmpeg路径，比如群晖的是`/var/packages/VideoStation/target/bin/ffmpeg`  
如果不需要请留空，既改成`ffmpeg = ''`
如果您不知道您的音响到底能不能放flac等比较先进的音频格式，可以先留空试试，如果不能播放，再填写ffmpeg路径，因为音频会实时转成没有任何压缩的wav格式，所以服务端需要相对较高的局域网带宽和性能

#### 在2024/04/13修改了需要重写的解析的地址，在红米小爱play测试通过
然后修改路由器的hosts，加入这样一行，或者直接将服务器主机名改成`zyym.ie`
```
你服务器的ip zyym.ie
```
就算你使用别的方式也好，只要将`zyym.ie`这个不存在的域名在你局域网解析到你的服务器就行了  
劫持失败请在 路由器后台 -> 网络 ->DHCP/DNS-> 一般设置 -> 重绑定保护（丢弃 RFC1918 上行响应数据），把这个的勾去掉 保存应用  
然后启动程序  
如果你没有正确的配置解析或是主机名，程序将报错并拒绝启动  
请不要自作聪明的将程序里的op改成别的来尝试启动，绝对用不了  
```
# 正常是这样启动的
python3 httpRandomMusic.py
# Windows可能是这样的
python httpRandomMusic.py
```

### 验证部署
用其他设备浏览器访问 http://zyym.ie:65533 能正常播放  
如果你可以进去小爱音响的shell，那么尝试 `curl -v http://zyym.ie:65533`  
此时控制台会有响应的输出  
如果能验证通过但还是用不了，请尝试重启，并确保dns真的成功劫持了，因为只要能解析就一定能用

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
~~A:文件格式不支持，BES2300的音响性能太差，跑的是NuttX而不是旧款的Openwrt，使用了裁剪的ffmpeg，大概只能放mp3（印着xiaomi的小爱音响play和play增强版）~~  
已支持使用ffmpeg实时转码成wav，支持所有格式，你甚至可以将视频当音频放

Q:群晖怎么用？  
A:在软件中心安装Python3，如果需要ffmpeg实时转码还需要安装VideoStation，然后将本程序放到一个你喜欢的地方，在计划任务添加一个开机启动，命令是`python3 你的路径/httpRandomMusic.py`，然后手动点击一下运行，就可以用了


### 协议 咩License
使用此项目视为您已阅读并同意遵守 [此LICENSE](https://github.com/zanjie1999/LICENSE)   
Using this project is deemed to indicate that you have read and agreed to abide by [this LICENSE](https://github.com/zanjie1999/LICENSE)   


