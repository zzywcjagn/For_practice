import aiohttp
import json
from nonebot.typing import T_State
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event


VerificationCode=""

async def get_VerificationCode(tel:str):
    url = "http://test.rori.cf/login"
    data = {
            "tel": tel,
            "id":"tel"
        }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data,) as resp:
           msg = await resp.text()
           
           jsonobj = json.loads(msg)
           print (jsonobj)
           return jsonobj



async def get_login(tel:str,yzm:str):
    url = "http://test.rori.cf/login"
    data = {
            "tel": tel,
            "id":tel,
            "yzm":yzm
        }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data,) as resp:
           msg = await resp.text()
           jsonobj = json.loads(msg)
           print (jsonobj)
           return jsonobj["value"]



jd_login = on_command("京东",block=True,priority=2)


@jd_login.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message())
    print(args)
    if args:
        state["tel"] = args  # 如果用户发送了参数则直接赋值


@jd_login.got("tel", prompt="请输入您的手机号码________,退出回复退出")
async def login_tel(bot: Bot, event: Event, state: T_State):
    global tel
    tel = state["tel"]
    ws= len(str(tel))
    print (ws)
    if tel == "退出":
        await jd_login.finish(message="已退出")
    elif len(str(tel)) != 11:
        await jd_login.reject(prompt="手机号输入错误，请重新输入")
    VerificationCode=await get_VerificationCode(tel)
    if VerificationCode is not None:
        pass
    else:
        await jd_login.finish(message="获取错误，请重新输入！")

@jd_login.got("yzm", prompt="请输入获取到的验证码进行登录______退出回复退出")
async def login_yzm(bot: Bot, event: Event, state: T_State):
    yzm = state["yzm"]

    if yzm == "退出":
        await jd_login.finish(message="已退出")
    elif len(str(yzm)) != 6:
        await jd_login.reject(prompt="验证码输入错误，请重新输入")
    print(yzm)
    login=await get_login(tel,yzm)
    if login is not None:
        await jd_login.finish(message="已经成功登陆，cookie为\n"+login)
    else:
        await jd_login.finish(message="获取错误，请重新输入！")