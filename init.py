import os
import sys
import time
import base64
import hashlib
import urllib.request
IP = str(urllib.request.urlopen('https://checkip.amazonaws.com').read())
start = time.time()
if sys.argv[1] == "":
    print("Usage: vmesspp --version --server")
if sys.argv[1] != "1.0":
    print("[ERROR] Version number is incorrect")
serverip = sys.argv[2]
serverip = serverip.replace("vmesspp://","")
serverip = serverip.replace("'","")
serverip = serverip[2:]
servermsg = serverip.split('-')
bs = str(base64.b64encode(servermsg[1].encode("utf-8")), "utf-8")
serverip = bs
del(bs)
t            = servermsg[2]
servermsg[1] = servermsg[2] # IP地址
servermsg[2] = t[:4]        # 服务器端口
iphash       = t[4:]        # IP hash
del(t)
serverip     = servermsg[1] + ':' + servermsg[2]
end = time.time()
print("[Log] 服务器地址解析完成,耗时" + str(start-end))
obj = hashlib.md5()
obj.update(servermsg[1].encode("utf-8"))
result=obj.hexdigest()
print("[Log] 解读IPhash:" + result)
print("[Log] 开始检验IPhash")
if iphash != result:
    print("[ERROR] IPhash校验失败,建议删除vmess++客户端并删除p,q的值")
    sys.exit(1)
print("[Log] 请给出p,q的值以连接服务器")
print("[Ask] p=?")
p = input("p=")
print("[Ask] q=?")
q = input("q=")
urllib.request.open(serverip + "/login/" + p + "/" + q)
print("[Log] 已向服务器发送p,q,如不正确则无法取回文件")
print("[Log] IPhash检验成功 开始连接vmess++服务器")

print("[Info] vmess++ server ip:" + serverip)
print("[Ask] 请给出cookie.flag")
askFile = input("Enter Cookie: ")
print("[Log] 开始读入cookie.flag并试图测试加密方法,请稍后")
with open(askFile,"r") as f:
    pythonFile = f.read()
try:
    exec("import " + pythonFile)
    print("[Log] 测试加密方法成功")
except:
    print("[ERROR] Cookie.flag解密失败,请检查下载cookie.flag时的网络状况并删除p,q的值")
    sys.exit(1)
print("[Log] Cookie.flag解密成功,准备vmess++服务器")
print("[Ask] 目标Vmess++服务器是否允许ping?")
ping = input("y/n: ")
if ping == "y":
    network = os.system("ping " + servermsg[1] + " >nul")
    if(network):
        print("[ERROR] 目标Vmess++服务器无法连接")
        sys.exit(1)
    else:
        print("[Log] 目标Vmess++服务器ping成功")
print("[Ask] 请输入网址")
url = input("url: ")
urllib.request(serverip + "/api/account/cat/search/" + IP + url)
print("[Log] 已请求目标vmess++服务器,尝试下载文件")
print("[Ask] 请输入重连次数")
retry = input("retry: ")
retry = int(retry)
for i in range(retry):
    print("[Log] 连接第" + str(i+1) + "次")
    time.sleep(1)
    data = urllib.request(serverip + "/api/account/" + IP + "/send")
print("[Log] 文件下载成功")
websiteFile = input("[Ask] 请输入保存位置:")
with open(websiteFile,"wb") as f:
    f.write(data.read())