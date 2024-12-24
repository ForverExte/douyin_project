import asyncio
import random
import subprocess
import time
from functools import partial
import urllib.parse
from playwright.async_api import async_playwright
from tkinter import messagebox

from my_pack import threaded
from my_pack.js import js_code

import urllib.parse

HEADERS = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.douyin.com/video/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
}

subprocess.Popen = partial(subprocess.Popen, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)


def get_signature(params):
    import execjs
    DOUYIN_SIGN = execjs.compile(js_code)
    query = '&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items()])
    a_bogus = DOUYIN_SIGN.call('sign_reply', query, HEADERS)
    params["a_bogus"] = a_bogus
    return params



def get_web_id():
    def e(t):
        if t is not None:
            return str(t ^ (int(16 * random.random()) >> (t // 4)))
        else:
            return ''.join(
                [str(int(1e7)), '-', str(int(1e3)), '-', str(int(4e3)), '-', str(int(8e3)), '-', str(int(1e11))]
            )
    web_id = ''.join(
        e(int(x)) if x in '018' else x for x in e(None)
    )
    return web_id.replace('-', '')[:19]


async def async_login_and_save_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.douyin.com/user/self")
        try:
            await page.wait_for_selector("text=登录成功", timeout=30000)
        except Exception as e:
            await browser.close()
            raise e
        xmst_value = await page.evaluate("window.localStorage.getItem('xmst');")
        print(f"xmst: {xmst_value}")
        with open('token.ini', 'w') as f:
            f.write("token = {\n")
            f.write(f"    'xmst': '{xmst_value}',\n")
            f.write("}\n")
        time.sleep(10)
        cookies = await context.cookies()
        cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        with open('ck.ini', 'w') as f:
            f.write("cookies = {\n")
            for key, value in cookies_dict.items():
                f.write(f"    '{key}': '{value}',\n")
            f.write("}\n")
        await browser.close()
        return xmst_value


def get_cookie():
    with open('./ck.ini', 'r') as file:
        data = file.read()
    cookies_str = data.strip().replace("cookies =", "").strip()
    cookies = eval(cookies_str)
    return cookies


def get_token():
    with open('./token.ini', 'r') as file:
        data = file.read()
    token_str = data.strip().replace("token =", "").strip()
    token = eval(token_str)
    return token
