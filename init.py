import sys
import base64
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
servermsg[2] = t[4:]        # 服务器端口
del(t)
