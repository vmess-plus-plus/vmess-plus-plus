import sys
import time
import base64
import hashlib

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
print("[Log]解读IPhash:" + result)
print("[Log]开始检验IPhash")
if iphash != result:
    print("[ERROR]IPhash校验失败,建议删除vmess++客户端并删除p,q的值")
    sys.exit(1)
print("[Log] IPhash检验成功 开始连接vmess++服务器")

print("[Info] vmess++ server ip:" + serverip)
