# coding=utf-8

# http随机音乐播放器
# 给小爱音箱用于播放nas的音乐
# 手搓了个简易http服务
# Sparkle
# v4.0

import os, random, urllib, posixpath, shutil, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

# 端口号
port = 65533

# 存音乐的目录
fileDir = '/Users/sparkle/Music/网易云音乐'  

# 实时转码需要依赖ffmpeg的路径 如果为空就不转码
ffmpeg = 'ffmpeg'


fileList = None
fileIndex = 0
def updateFileList(search=''):
    global fileList
    global fileIndex
    try:
        os.chdir(fileDir)
    except Exception as e:
        print(e)
        print('ERROR: 请检查目录是否存在或是否有权限访问')
        exit()
    fileIndex = 0
    # fileList = list(filter(lambda x: x.lower().split('.')[-1] in ['flac','mp3','wav','aac','m4a'], os.listdir('.')))
    fileList = []
    for path, _, files in os.walk('.'):
        for f in files:
            if f.lower().split('.')[-1] in ['flac','mp3','wav','aac','m4a']:
                fpath = os.path.join(path, f)[2:]
                # 搜索关键词可以是文件夹名也可以是文件名
                if not search or search in fpath:
                    fileList.append(fpath)
    fileList.sort(key=lambda x: os.path.getmtime(x))
    fileList.reverse()
    print(str(len(fileList)) + ' files')
    print(fileList[1])


class meHandler(BaseHTTPRequestHandler):
    def translate_path(self, path):
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        trailing_slash = path.rstrip().endswith('/')
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        path = posixpath.normpath(path)
        words = path.split('/')
        words = filter(None, words)
        path = fileDir
        for word in words:
            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path

    def return302(self, filename):
        self.send_response(302)
        self.send_header('Location', '/' + urllib.parse.quote(filename))
        self.end_headers()

    def play(self, path):
        print(path)
        if os.path.isfile(path):
            self.send_response(200)
            if ffmpeg and path.lower().split('.')[-1] not in ['wav','mp3']:
                self.send_header("Content-type", 'audio/wav')
                t = subprocess.getoutput('{} -i "{}" 2>&1 | {} Duration'.format(ffmpeg, path, 'findstr' if os.name == 'nt' else 'grep')).split()[1][:-1].split(':')
                # 根据码率计算文件总大小，让RTOS的音响显示正确的进度条
                self.send_header("Content-Length", str((float(t[0]) * 3600 + float(t[1]) * 60 + float(t[2])) * 176400))
                self.end_headers()
                pipe = subprocess.Popen([ffmpeg, '-i', path, '-f', 'wav', '-'], stdout=subprocess.PIPE, bufsize=10 ** 8)
                try:
                    shutil.copyfileobj(pipe.stdout, self.wfile)
                finally:
                    self.wfile.flush()
                    pipe.terminate()
            else:
                self.send_header("Content-type", 'audio/mpeg')
                with open(path, 'rb') as f:
                    self.send_header("Content-Length", str(os.fstat(f.fileno())[6]))
                    self.end_headers()
                    shutil.copyfileobj(f, self.wfile)
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        global fileList
        global fileIndex
        print(self.path)
        if self.path == '/':
            self.return302(fileList[fileIndex])
            fileIndex += 1
            if fileIndex >= len(fileList):
                fileIndex = 0
        elif self.path == '/random':
            # 随机播放
            updateFileList()
            random.shuffle(fileList)
            self.return302(fileList[0])
            fileIndex = 1
        elif self.path == '/frist':
            # 从头开始播放
            updateFileList()
            self.return302(fileList[0])
            fileIndex = 1
        elif self.path.startswith('/s/'):
            # 搜索
            updateFileList(self.path[3:])
            self.return302(fileList[0])
            fileIndex = 1
        else:
            path = self.translate_path(self.path)
            self.play(path)



if os.system("nslookup zyym.ie"):
    print('ERROR: 请将zyym.ie指向本机ip，否则小爱音箱可能无法访问')
updateFileList()
HTTPServer(("", port), meHandler).serve_forever()
