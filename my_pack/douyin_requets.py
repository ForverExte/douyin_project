import json
import re
import requests

from my_pack.basic_functions import get_signature, get_web_id, get_cookie, get_token
from my_pack.field import SearchChannelType

first_rid = None

def headers_all():
    headers = {
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
    return headers


def headers_video():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'priority': 'u=1, i',
        'referer': 'https://www.douyin.com/user/self?showTab=post',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }
    return headers


def user_video(need_time_list=1, sec_user_id=''):
    params = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'sec_user_id': sec_user_id,
        'max_cursor': '0',
        'locate_query': 'false',
        'show_live_replay_strategy': '1',
        'need_time_list': need_time_list,
        'time_list_query': '0',
        'whale_cut_token': '',
        'cut_version': '1',
        'count': '10',
        'publish_video_strategy_type': '2',
        'update_version_code': '170400',
        'pc_client_type': '1',
        'version_code': '290100',
        'version_name': '29.1.0',
        'cookie_enabled': 'true',
        'screen_width': '1920',
        'screen_height': '1080',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '127.0.0.0',
        'browser_online': 'true',
        'engine_name': 'Blink',
        'engine_version': '127.0.0.0',
        'os_name': 'Windows',
        'os_version': '10',
        'cpu_core_num': '16',
        'device_memory': '8',
        'platform': 'PC',
        'downlink': '10',
        'effective_type': '4g',
        'round_trip_time': '100',
        'webid': get_web_id(),
        'verifyFp': 'verify_lzz3t10y_QJ3e5YRU_KHiu_4aZy_BlEd_1TW0RKstScjZ',
        'fp': 'verify_lzz3t10y_QJ3e5YRU_KHiu_4aZy_BlEd_1TW0RKstScjZ',
        'msToken': get_token(),
    }
    return params


def headers_user_search():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,pt;q=0.5,pt-BR;q=0.4,pt-PT;q=0.3',
        'priority': 'u=1, i',
        'referer': 'https://www.douyin.com/search/%E5%8D%97%E9%A3%8E%E4%B8%8D%E7%9F%A5%E6%88%91%E6%84%8F?aid=7b68f878-42f4-4019-b54c-ba3195726c74&enter_from=discover&source=search_history',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }
    return headers


def user_search(search_channel: SearchChannelType = SearchChannelType.GENERAL, offset=0):
    params = {
        "device_platform": "webapp",
        "aid": "6383",
        "channel": "channel_pc_web",
        "search_channel": search_channel,
        "keyword": '',
        "search_source": "switch_tab",
        "query_correct_type": "1",
        "is_filter_search": "0",
        "from_group_id": "",
        "offset": offset,
        "count": "15",
        "need_filter_settings": "1",
        "list_type": "multi",
        "update_version_code": "170400",
        "pc_client_type": "1",
        "version_code": "170400",
        "version_name": "17.4.0",
        "cookie_enabled": "true",
        "screen_width": "1920",
        "screen_height": "1080",
        "browser_language": "zh-CN",
        "browser_platform": "Win32",
        "browser_name": "Chrome",
        "browser_version": "127.0.0.0",
        "browser_online": "true",
        "engine_name": "Blink",
        "engine_version": "127.0.0.0",
        "os_name": "Windows",
        "os_version": "10",
        "cpu_core_num": "16",
        "device_memory": "8",
        "platform": "PC",
        "downlink": "5.35",
        "effective_type": "4g",
        "round_trip_time": "150",
        'webid': get_web_id(),
        'msToken': get_token()['xmst']
    }
    if offset > 0:
        params['need_filter_settings'] = 0
    if first_rid:
        params['search_id'] = first_rid

    return params


def search_users(offset=0, keyword='', rid=None):
    global first_rid

    params = get_signature(params=user_search())

    params['offset'] = offset
    print(f"使用关键字搜索: {params['keyword']}")
    params['keyword'] = keyword
    print(f"Searching with keyword: {params['keyword']}")

    if rid is not None:
        params['rid'] = rid

    response = requests.get(
        'https://www.douyin.com/aweme/v1/web/discover/search/',
        params=params,
        cookies=get_cookie(),
        headers=headers_all(),
    )

    json_search = json.loads(response.text)

    current_rid = json_search.get('rid')
    if current_rid:
        first_rid = current_rid

    user_info = []
    for user in json_search.get('user_list', []):
        user_data = {
            'nickname': user['user_info']['nickname'],
            'sec_uid': user['user_info']['sec_uid'],
            'uid': user['user_info']['uid'],
            'unique_id': user['user_info']['unique_id'],
            'signature': user['user_info']['signature'],
        }

        account_cert_info = user['user_info'].get('account_cert_info', '')
        match = re.search(r'"label_text":"(.*?)"', account_cert_info)
        user_data['account_cert_info'] = match.group(1) if match else "未认证"

        user_info.append(user_data)

    return user_info, first_rid


def user_message(id):
    params = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'publish_video_strategy_type': '2',
        'source': 'channel_pc_web',
        'sec_user_id': id,
        'personal_center_strategy': '1',
        'update_version_code': '170400',
        'pc_client_type': '1',
        'version_code': '170400',
        'version_name': '17.4.0',
        'cookie_enabled': 'true',
        'screen_width': '1920',
        'screen_height': '1080',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '127.0.0.0',
        'browser_online': 'true',
        'engine_name': 'Blink',
        'engine_version': '127.0.0.0',
        'os_name': 'Windows',
        'os_version': '10',
        'cpu_core_num': '16',
        'device_memory': '8',
        'platform': 'PC',
        'downlink': '10',
        'effective_type': '4g',
        'round_trip_time': '100',
        'webid': get_web_id(),
        'verifyFp': 'verify_lzz3t10y_QJ3e5YRU_KHiu_4aZy_BlEd_1TW0RKstScjZ',
        'fp': 'verify_lzz3t10y_QJ3e5YRU_KHiu_4aZy_BlEd_1TW0RKstScjZ',
        'msToken': get_token()['xmst'],
    }
    return params


def video_comments(aweme_id, cursor='0', count='20'):
    params = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'aweme_id': aweme_id,
        'cursor': cursor,
        'count': count,
        'item_type': '0',
        'insert_ids': '',
        'whale_cut_token': '',
        'cut_version': '1',
        'rcFT': '',
        'update_version_code': '170400',
        'pc_client_type': '1',
        'version_code': '170400',
        'version_name': '17.4.0',
        'cookie_enabled': 'true',
        'screen_width': '1536',
        'screen_height': '864',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '127.0.0.0',
        'browser_online': 'true',
        'engine_name': 'Blink',
        'engine_version': '127.0.0.0',
        'os_name': 'Windows',
        'os_version': '10',
        'cpu_core_num': '16',
        'device_memory': '8',
        'platform': 'PC',
        'downlink': '5',
        'effective_type': '4g',
        'round_trip_time': '200',
        'webid': get_web_id(),
        'msToken': get_token()['xmst'],
        'verifyFp': 'verify_lzz3t10y_QJ3e5YRU_KHiu_4aZy_BlEd_1TW0RKstScjZ',
        'fp': 'verify_lzz3t10y_QJ3e5YRU_KHiu_4aZy_BlEd_1TW0RKstScjZ',
    }
    return params


def comments_level2(item_id, comment_id, cursor_level2, count_level2):
    params = {
        'device_platform': 'webapp',
        'aid': '6383',
        'channel': 'channel_pc_web',
        'item_id': item_id,
        'comment_id': comment_id,
        'cut_version': '1',
        'cursor': cursor_level2,
        'count': count_level2,
        'item_type': '0',
        'update_version_code': '170400',
        'pc_client_type': '1',
        'version_code': '170400',
        'version_name': '17.4.0',
        'cookie_enabled': 'true',
        'screen_width': '1536',
        'screen_height': '864',
        'browser_language': 'zh-CN',
        'browser_platform': 'Win32',
        'browser_name': 'Chrome',
        'browser_version': '127.0.0.0',
        'browser_online': 'true',
        'engine_name': 'Blink',
        'engine_version': '127.0.0.0',
        'os_name': 'Windows',
        'os_version': '10',
        'cpu_core_num': '16',
        'device_memory': '8',
        'platform': 'PC',
        'downlink': '3.8',
        'effective_type': '4g',
        'round_trip_time': '100',
        'webid': '7404341132018189835',
        'msToken': 'jtFID5Ah5vI_3Hua5qiuuSaCAcPGXx-aojuUR114lNnweevPv5ywaa8VDXFRKzp4uOtjbLyKsIWfuxFpDkTUC3ufYjk-NadNboFH6P2yy5C0LDeYMRI71g==',
        'verifyFp': 'verify_lzz3t10y_QJ3e5YRU_KHiu_4aZy_BlEd_1TW0RKstScjZ',
        'fp': 'verify_lzz3t10y_QJ3e5YRU_KHiu_4aZy_BlEd_1TW0RKstScjZ',
    }
    return params
