# coding=utf-8

# http随机音乐播放器
# 给小爱音箱用于播放nas的音乐
# 手搓了个简易http服务
# Sparkle
# v2.0

import os, random, urllib, posixpath, shutil, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

# 端口号
port = 65533

# 存音乐的目录
fileDir = '/data/音乐/' 

# 实时转码需要依赖ffmpeg的路径 如果为空就不转码
ffmpeg = 'ffmpeg'


fileList = None
fileIndex = 0
def updateFileList():
    global fileList
    global fileIndex
    os.chdir(fileDir)
    fileIndex = 0
    # for i in os.listdir(fileDir):
    #     if i.lower().split('.')[-1] in ['flac','mp3','wav','aac','m4a']:
    #         fileList.append(i)
    fileList = list(filter(lambda x: x.lower().split('.')[-1] in ['flac','mp3','wav','aac','m4a'], os.listdir('.')))
    fileList.sort(key=lambda x: os.path.getmtime(x))
    fileList.reverse()
    print(str(len(fileList)) + ' files')


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
            updateFileList()
            random.shuffle(fileList)
            self.return302(fileList[0])
        elif self.path == '/frist':
            updateFileList()
            self.return302(fileList[0])
        else:
            path = self.translate_path(self.path)
            print(path)
            if os.path.isfile(path):
                self.send_response(200)
                self.send_header("Content-type", 'audio/mpeg')
                if ffmpeg and path.lower().split('.')[-1] not in ['wav','mp3']:
                    self.end_headers()
                    pipe = subprocess.Popen(['ffmpeg', '-i', path, '-f', 'wav', '-'], stdout=subprocess.PIPE, bufsize=10 ** 8)
                    try:
                        shutil.copyfileobj(pipe.stdout, self.wfile)
                    finally:
                        pipe.terminate()
                else:
                    with open(path, 'rb') as f:
                        self.send_header("Content-Length", str(os.fstat(f.fileno())[6]))
                        self.end_headers()
                        shutil.copyfileobj(f, self.wfile)
            else:
                self.send_response(404)
                self.end_headers()



updateFileList()
HTTPServer(("", port), meHandler).serve_forever()
