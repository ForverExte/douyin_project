import random
import subprocess
import time
import os
import sys
from functools import partial
import urllib.parse

from playwright.async_api import async_playwright
import tkinter as tk
from tkinter import filedialog

from database import Database
from my_pack.js import js_code


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
    try:

        def run_js_hidden(js_code):
            return subprocess.Popen(
                ["node", "-e", js_code],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
                text=True
            ).communicate()[0]


        def call_js_function(js_code, function_name, *args):
            args_str = ", ".join([f"'{arg}'" if isinstance(arg, str) else str(arg) for arg in args])
            wrapped_js_code = f"""
            {js_code}
            console.log({function_name}({args_str}));
            """
            return run_js_hidden(wrapped_js_code).strip()

        query = '&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items()])
        a_bogus = call_js_function(js_code, 'sign_reply', query, HEADERS)

        params["a_bogus"] = a_bogus
        return params

    except Exception as e:
        print(f"获取签名时发生错误: {str(e)}")
        raise


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




def get_file_path(filename):
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), filename)
    else:
        return filename

async def async_login_and_save_cookies():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto("https://www.douyin.com/user/self")

        print("请扫描二维码登录...")
        try:
            # 等待“登录成功”文本出现
            await page.wait_for_selector("text=登录成功", timeout=30000)
            print("登录成功")
        except Exception as e:
            print("登录失败或超时")
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
    cookies_path = get_file_path('ck.ini')
    try:
        with open(cookies_path, 'r') as file:
            data = file.read()
        cookies_str = data.strip().replace("cookies =", "").strip()
        return eval(cookies_str)
    except Exception as e:
        print(f"读取cookies文件失败: {str(e)}")
        return {}

def get_token():
    token_path = get_file_path('token.ini')
    try:
        with open(token_path, 'r') as file:
            data = file.read()
        token_str = data.strip().replace("token =", "").strip()
        return eval(token_str)
    except Exception as e:
        print(f"读取token文件失败: {str(e)}")
        return {}
