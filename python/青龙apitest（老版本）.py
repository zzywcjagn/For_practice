import requests,json
from flask import Flask,request

app = Flask(__name__)




#获取token
def gettoken():
    with open(qlroot+'/config/auth.json','r',encoding='utf8')as fp:
        json_data = json.load(fp)
        token=json_data['token']
    return token


#变量部分
qlroot = "" #填写青龙映射的根目录，如/root/ql
qlurl= ""#填写反代后青龙的网址
apiurl=qlurl +"/api"
url= apiurl+"/envs?t=1633076856051"
pin=""

#获取京东昵称
def getnickname(cookie):
    geturl="https://get.zzzytd.top/nick.php"
    payload2 = {
        'cookie':cookie
        }
    d=requests.get(url=geturl,data=json.dumps(payload2))
    nickname=d.text
    print (nickname)
    return nickname

#搜索变量
def search(searchValue):
    payload1 = {'searchValue': searchValue}
    token = gettoken()
    headers={
        'Authorization':'Bearer '+token,
        'Origin':qlurl,
        'content-type':'application/json;charset=UTF-8'
    }
    bb=requests.get (url=url,params=payload1,headers=headers)
    ssjg=bb.json()
    print (bb.json()['data'])
    if ssjg['data'] == []:
        return "error"
    else:
        ssjg=ssjg['data'][0]
        ssjg_cookie=ssjg['value']
        ssjg_id=ssjg['_id']
        ssjg_remarks=ssjg['remarks']
        return ssjg

#添加变量
def addenv(jdcookie):
    nickname=getnickname(jdcookie)
    token = gettoken()
    headers={
        'Authorization':'Bearer '+token,
        'Origin':qlurl,
        'content-type':'application/json;charset=UTF-8'
    }
    payload2 = [{
        'name': 'JD_COOKIE',
        'remarks':nickname,
        'value':jdcookie
        }]
    r = requests.post(url=url, data=json.dumps(payload2),headers=headers)
    jg= r.json()['data'][0]
    print(jg)
    return jg

#更新变量
def updateenv(jdcookie,ssjg_id):
    nickname=getnickname(jdcookie)
    token = gettoken()
    headers={
        'Authorization':'Bearer '+token,
        'Origin':qlurl,
        'content-type':'application/json;charset=UTF-8'
    }
    payload3 = {
        'name': "JD_COOKIE",
        'remarks': nickname,
        'value': jdcookie,
        '_id': ssjg_id
        }
    gxbl=requests.put(url=url, data=json.dumps(payload3),headers=headers)
    gxbl=gxbl.json()['data']
    print(gxbl)
    return gxbl

@app.route('/ql', methods = ['POST'])
def index():
    pin= request.form['pin']
    if pin is not None:
        pin1= "pt_pin="+pin
        jdcookie=request.form['cookie']
        ssjg=search(pin1)
        if ssjg == "error":
            jg=addenv(jdcookie)
        elif ssjg['value'] is not None:
            ssjg_id=ssjg['_id']
            jg=updateenv(jdcookie,ssjg_id)
        else:
            return "error"
        return jg
    else:
        return "提交的参数错误"

if __name__ == '__main__':
    app.run("127.0.0.1", 8081)