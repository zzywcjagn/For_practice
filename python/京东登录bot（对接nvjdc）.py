import aiohttp
import json
from nonebot.typing import T_State
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event

nvjdcurl=""#nvjdc项目的地址，不带/login
qlkey="1"#配置文件内设置的qlkey 默认1
VerificationCode=""
session={}

async def SendSMS(nvjdcurl:str,tel:str,qlkey:str):
    url = nvjdcurl+"api/SendSMS"
    data = {
            "Phone": tel,
            "qlkey":qlkey
        }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data,) as resp:
           msg = await resp.text()
           jsonobj = json.loads(msg)
           print (jsonobj)
           return jsonobj

async def AutoCaptcha(nvjdcurl:str,tel:str):
    url = nvjdcurl+"api/AutoCaptcha"
    data = {
            "Phone": tel
        }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data,) as resp:
           msg = await resp.text()
           jsonobj = json.loads(msg)
           print (jsonobj)
           return jsonobj


async def VerifyCode(nvjdcurl:str,tel:str,yzm:str,qlkey:str):
    url = nvjdcurl+"api/VerifyCode"
    data = {
            "Phone": tel,
            "QQ":"",
            "qlkey":qlkey,
            "Code":yzm
        }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data,) as resp:
           msg = await resp.text()
           jsonobj = json.loads(msg)
           print (jsonobj)
           return jsonobj["data"]



jd_login = on_command("京东",block=True,priority=2)


@jd_login.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message())
    id=event.get_user_id()
    print(args)
    if args:
        state["tel"] = args  # 如果用户发送了参数则直接赋值


@jd_login.got("tel", prompt="请输入您的手机号码________,退出回复退出")
async def login_tel(bot: Bot, event: Event, state: T_State):
    global tel
    tel = state["tel"]
    id=event.get_user_id()
    global session
    session[id]={"tel":tel}
    ws= len(str(tel))
    print (ws)
    if tel == "退出":
        await jd_login.finish(message="已退出")
    elif len(str(tel)) != 11:
        await jd_login.reject(prompt="手机号输入错误，请重新输入")
    VerificationCode=await SendSMS(nvjdcurl,session[id]["tel"],qlkey)
    if VerificationCode["success"] is not False:
        pass
    else:
        await bot.send_private_msg(user_id=id,message="遇到安全验证，正在破解....")
        captcha=await AutoCaptcha(nvjdcurl,session[id]["tel"])
        if captcha["success"] is not False:
            pass
        else:
            await jd_login.finish(message=captcha["message"])
        

@jd_login.got("yzm", prompt="请输入获取到的验证码进行登录______退出回复退出")
async def login_yzm(bot: Bot, event: Event, state: T_State):
    yzm = state["yzm"]
    id=event.get_user_id()
    session[id]["yzm"]=yzm
    if yzm == "退出":
        await jd_login.finish(message="已退出")
    elif len(str(yzm)) != 6:
        await jd_login.reject(prompt="验证码输入错误，请重新输入")
    print(yzm)
    login=await VerifyCode(nvjdcurl,session[id]["tel"],session[id]["yzm"],qlkey)
    if login is not None:
        await jd_login.finish(message=login["nickname"]+"您好\n\n已经成功登陆")
    else:
        await jd_login.finish(message="获取错误，请重新输入！")