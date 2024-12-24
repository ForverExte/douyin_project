import os
import tkinter as tk
import webbrowser

from tkinter import ttk, filedialog, Menu
from PIL import Image, ImageTk
from openpyxl import Workbook
import pandas as pd

from my_pack import *
from my_pack.basic_functions import *
from my_pack.douyin_requets import *


first_rid = None
current_bubble = None
first_max_cursor = None
current_index = 1
current_cursor = '0'
default_count = '50'
cursor_level2 = '0'
count_level2 = '50'
aweme_id = ''
num = 1
num_level2 = 1


def login_and_save_cookies():
    return asyncio.run(async_login_and_save_cookies())

def show_frame(frame):
    for f in frames:
        f.pack_forget()
    frame.pack(side="right", expand=True, fill="both")


def add_button(button_frame, frames):
    all_search = tk.Button(button_frame, text='   用户搜索  ', command=lambda: show_frame(frames[0]))
    all_search.grid(row=0, pady=5)

    view_video = tk.Button(button_frame, text='查看用户视频', command=lambda: show_frame(frames[1]))
    view_video.grid(row=1, pady=5)

    view_video_comments = tk.Button(button_frame, text='查看视频评论', command=lambda: show_frame(frames[2]))
    view_video_comments.grid(row=2, pady=5)

    button_frame.grid_rowconfigure(0, weight=0)
    button_frame.grid_rowconfigure(1, weight=0)
    button_frame.grid_rowconfigure(2, weight=0)

    button_frame.grid_rowconfigure(3, weight=1)

    check_cdk = tk.Button(button_frame, text='      验证      ')
    check_cdk.grid(row=4, pady=5, sticky='s')

    button_frame.grid_rowconfigure(4, weight=1)


def copy_nickname(tree):
    selected_item = tree.selection()
    values = tree.item(selected_item, 'values')
    if values:
        sec_uid = values[1]
        tree.clipboard_clear()
        tree.clipboard_append(sec_uid)
        return sec_uid
    return None



def check_cookie_file():
    if os.path.exists('ck.ini'):
        with open('ck.ini', 'r') as file:
            lines = file.readlines()
        if len(lines) == 0:
            status_label.config(text='cookie未获取', bg='white')
        elif len(lines) >= 50:
            status_label.config(text='cookie已获取', bg='white')
        else:
            status_label.config(text='cookie不完整', bg='white')
    else:
        status_label.config(text='文件不存在')

    top_frame.after(1000, check_cookie_file)


def open_user_page(selected_item, unique_id):
    if selected_item:
        url = f"https://www.douyin.com/user/{unique_id}"
        webbrowser.open(url)


def show_right_click_menu(event, tree, memu):
    selected_item = tree.identify_row(event.y)
    if selected_item:
        tree.selection_set(selected_item)
        memu.post(event.x_root, event.y_root)


@threaded
def on_search():
    if status_label.cget("text") == "cookie已获取":
        global current_offset, first_rid
        current_offset = 0
        first_rid = None

        keyword = search_entry.get()
        for item in treeview.get_children():
            treeview.delete(item)
        users, rid = search_users(offset=current_offset, keyword=keyword, rid=first_rid)
        update_treeview(users)
        # print(rid)
        # print(users)
    else:
        messagebox.showwarning("警告", "请先扫码登录获取cookie再使用！")


@threaded
def on_get_10_more():
    global current_offset
    current_offset += 10
    users, rid = search_users(offset=current_offset, keyword=search_entry.get())
    update_treeview(users)
    # print(rid)
    # print(users)


@threaded
def on_get_50_more():
    global current_offset
    for rid in range(5):
        current_offset += 10
        users, rid = search_users(offset=current_offset, keyword=search_entry.get())
        update_treeview(users)

    # print(rid)
    # print(users)


def user_message_search(sec_uid):
    import execjs
    DOUYIN_SIGN = execjs.compile(js_code)

    params = user_message(id=sec_uid)
    query = '&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items()])

    a_bogus = DOUYIN_SIGN.call('sign_datail', query, headers_all()["user-agent"])
    params["a_bogus"] = a_bogus

    response = requests.get(url='https://www.douyin.com/aweme/v1/web/user/profile/other/',
                            params=params,
                            cookies=get_cookie(),
                            headers=headers_all())

    json_data = json.loads(response.text)
    return json_data


def show_user_info(selected_item, sec_uid):
    global current_bubble

    if current_bubble is not None:
        current_bubble.destroy()

    # selected_item = treeview.selection()
    if selected_item:
        user_data = user_message_search(sec_uid)
        print(user_data)
        gender_mapping = {0: '未知', 1: '男', 2: '女'}
        nickname = user_data['user']['nickname']
        signature = user_data['user']['signature']
        country = user_data['user']['country']
        province = user_data['user']['province']
        city = user_data['user']['city']
        ip_location = user_data['user'].get('ip_location', '无')
        ip_location = ip_location.split('：')[-1]
        max_follower_count = user_data['user']['max_follower_count']
        mplatform_followers_count = user_data['user']['mplatform_followers_count']
        user_age = user_data['user']['user_age']
        user_age = '未知' if user_age == -1 else user_age
        uid = user_data['user']['uid']
        unique_id = user_data['user']['unique_id']
        total_favorited = user_data['user']['total_favorited']
        following_count = user_data['user']['following_count']
        forward_count = user_data['user']['forward_count']
        gender = gender_mapping.get(user_data['user']['gender'], '未知')
        school_name = user_data['user']['school_name']
        aweme_count = user_data['user']['aweme_count']

        info = f"昵称: {nickname}\n" \
               f"个性签名: {signature}\n" \
               f"国家: {country}\n" \
               f"省份: {province}\n" \
               f"城市: {city}\n" \
               f"IP地址: {ip_location}\n" \
               f"最高粉丝数量: {max_follower_count}\n" \
               f"当前粉丝数: {mplatform_followers_count}\n" \
               f"年龄: {user_age}\n" \
               f"抖音ID: {uid}\n" \
               f"抖音号: {unique_id}\n" \
               f"获赞: {total_favorited}\n" \
               f"关注: {following_count}\n" \
               f"未知: {forward_count}\n" \
               f"性别: {gender}\n" \
               f"学校: {school_name}\n" \
               f"作品: {aweme_count}"


        current_bubble = tk.Toplevel(top_frame)
        current_bubble.wm_overrideredirect(True)

        root_x = treeview.winfo_rootx()
        root_y = treeview.winfo_rooty()

        bubble_frame = tk.Frame(current_bubble, background="#FFFFE0", borderwidth=0)
        bubble_frame.pack(fill='both', expand=True, padx=0, pady=0)


        label = tk.Label(bubble_frame, text=info, justify='left', background="#FFFFE0")
        label.pack(side='left', anchor='nw')


        close_button = tk.Button(bubble_frame, text="X", command=current_bubble.destroy,
                                 bg="#FFFFE0", fg="black", bd=0, font=("Arial", 12, "bold"))
        close_button.pack(side='right', anchor='ne', padx=5)
        label.pack()

        current_bubble.update_idletasks()


        bubble_width = current_bubble.winfo_width()
        bubble_height = current_bubble.winfo_height()
        print(f"气泡窗口宽度: {bubble_width}, 高度: {bubble_height}")

        if root.state() == 'zoomed':
            current_bubble.wm_geometry(f"+{root_x}+{root_y + 65}")
        else:
            current_bubble.wm_geometry(f"+{root_x - bubble_width}+{root_y + 65}")


def update_treeview(users):
    start_index = len(treeview.get_children()) + 1
    for idx, user in enumerate(users, start=start_index):
        treeview.insert('', tk.END, values=(
            idx, user['nickname'], user['sec_uid'], user['uid'], user['unique_id'], user['signature'],
            user['account_cert_info']))



def copy_media_url():
    selected_item = tree_user_video.selection()
    if selected_item:
        media_url = tree_user_video.item(selected_item, 'values')[3]
        root.clipboard_clear()
        root.clipboard_append(media_url)
        messagebox.showinfo("复制成功", "媒体链接已复制到剪贴板")
    else:
        messagebox.showwarning("未选择行", "请先选择一行再试")


@threaded
def clear_treeview():
    for i in tree_user_video.get_children():
        tree_user_video.delete(i)


def save_to_excel():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        wb = Workbook()
        ws = wb.active
        ws.title = "抖音视频信息"

        ws.append(columns)

        for item in tree_user_video.get_children():
            row = tree_user_video.item(item)["values"]
            ws.append(row)

        wb.save(file_path)
        messagebox.showinfo("保存成功", f"数据已保存到 {file_path}")


def sanitize_folder_name(title, max_length=50):

    invalid_chars = r'[\/:*?"<>|\n]'
    sanitized_title = re.sub(invalid_chars, '', title)


    if len(sanitized_title) > max_length:
        sanitized_title = sanitized_title[:max_length] + '_命名失败'

    return sanitized_title


@threaded
def download_media():

    save_dir = os.path.join(os.getcwd(), "抖音视频")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


    title_count = {}


    for item in tree_user_video.get_children():
        values = tree_user_video.item(item, "values")
        nickname = values[1]
        media_type = values[2]
        media_urls = values[3].split('、')
        caption = values[4]


        if not caption:
            caption = "无标题"


        safe_caption = sanitize_folder_name(caption)


        user_dir = os.path.join(save_dir, nickname)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        if media_type == "图文":
            image_dir = os.path.join(user_dir, safe_caption)
            if not os.path.exists(image_dir):
                os.makedirs(image_dir)


        if safe_caption in title_count:
            title_count[safe_caption] += 1
        else:
            title_count[safe_caption] = 1


        file_extension = "mp4" if media_type == "视频" else "jpg"

        for idx, media_url in enumerate(media_urls):

            if media_type == "图文":
                file_name = f"{safe_caption}_{idx + 1}.{file_extension}"
                file_path = os.path.join(image_dir, file_name)
            else:
                if title_count[safe_caption] > 1:
                    file_name = f"{safe_caption}_{title_count[safe_caption]}.{file_extension}"
                else:
                    file_name = f"{safe_caption}.{file_extension}"
                file_path = os.path.join(user_dir, file_name)

            try:

                response = requests.get(media_url, headers=headers_all(), stream=True)
                total_size = int(response.headers.get('content-length', 0))
                progress['maximum'] = total_size
                downloaded_size = 0

                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            progress['value'] = downloaded_size
                            root.update_idletasks()

                print(f"已下载 {file_name}")
                message_label.config(text=f"{file_name} 下载完成", fg="green")

            except Exception as e:
                print(f"下载 {file_name} 时出错: {e}")
                message_label.config(text=f"{file_name} 下载失败", fg="red")

            finally:
                progress['value'] = 0


    messagebox.showinfo("下载完成", "所有媒体文件已下载到 '抖音视频' 文件夹中")


@threaded
def fetch_data(mode="first"):
    global first_max_cursor, current_index
    selected_item = treeview.focus()

    sec_user_id = treeview.item(selected_item, 'value')[2]

    params = get_signature(user_video(sec_user_id=sec_user_id))
    params['need_time_list'] = 1

    if mode == "first":
        clear_treeview()
        params['max_cursor'] = 0
        first_max_cursor = None
        current_index = 1
    elif mode == "more":
        params['max_cursor'] = first_max_cursor
    elif mode == "all":
        clear_treeview()
        params['max_cursor'] = 0
        first_max_cursor = None
        current_index = 1

    while True:
        response = requests.get('https://www.douyin.com/aweme/v1/web/aweme/post/',
                                params=params, cookies=get_cookie(), headers=headers_all())

        json_data = json.loads(response.text)

        aweme_list = json_data.get('aweme_list', [])
        max_cursor = json_data.get('max_cursor', None)

        for video_data in aweme_list:
            aweme_id = video_data['aweme_id']
            nickname = video_data['author']['nickname']

            caption = video_data['desc']

            create_time = video_data['create_time']
            create_time = convert_timestamp_to_datetime(create_time)

            digg_count = video_data['statistics']['digg_count']
            comment_count = video_data['statistics']['comment_count']
            collect_count = video_data['statistics']['collect_count']
            share_count = video_data['statistics']['share_count']

            if video_data['video']['bit_rate'] is None:
                media_type = "图文"

                media_url = "、".join([img['url_list'][0] for img in video_data['images']])

                BGM = video_data.get('music', {}).get('title', "无")

                video_duration = "N/A"
            else:
                media_type = "视频"

                media_url = video_data['video']['play_addr']['url_list'][0]

                BGM = video_data.get('music', {}).get('title', "无")

                video_duration = video_data['video']['duration']
                total_seconds = video_duration // 1000
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                video_duration = f"{minutes:02}:{seconds:02}"

            tree_user_video.insert("", "end", values=(
                current_index, nickname, media_type, media_url, caption, create_time, BGM, video_duration, digg_count,
                comment_count, collect_count, share_count), tags=aweme_id)

            current_index += 1

        if not aweme_list or max_cursor is None or max_cursor == 0:
            break

        params['max_cursor'] = max_cursor

        if mode != "all":
            first_max_cursor = max_cursor
            break

    if mode == "all":
        first_max_cursor = None


def on_item_selected(event=None):
    selected_item = tree_user_video.selection()[0]
    tags = tree_user_video.item(selected_item, "tags")
    aweme_id = tags[0]
    print(f'视频标识符：{aweme_id}')


@threaded
def fetch_comments(mode="first"):
    global current_cursor, num

    selected_item = tree_user_video.focus()
    if not selected_item:
        comments_labal.config(text="未选择视频", fg="red")
        return

    aweme_id = tree_user_video.item(selected_item, 'tags')[0]
    if not aweme_id:
        comments_labal.config(text="未找到 aweme_id", fg="red")
        return

    if mode == "first":
        clear_treeview1(tree_comments)
        current_cursor = 0
        num = 1
    elif mode == "more":
        current_cursor += 50
    elif mode == "all":
        clear_treeview1(tree_comments)
        current_cursor = 0
        num = 1
    else:
        comments_labal.config(text="未知模式", fg="red")
        return

    while True:
        headers = headers_all()
        headers['user-agent'] = ''
        params = get_signature(params=video_comments(aweme_id, cursor=str(current_cursor), count=str(default_count)))
        response = requests.get('https://www.douyin.com/aweme/v1/web/comment/list/', params=params,
                                cookies=get_cookie(), headers=headers)

        response_text = response.text

        if response.status_code != 200:
            comments_labal.config(text=f"请求失败，状态码: {response.status_code}", fg="red")
            return

        try:
            json_comments = json.loads(response.text)
        except json.JSONDecodeError as e:
            comments_labal.config(text=f"JSON解析错误: {e}", fg="red")
            return

        awe_list = json_comments.get('comments', None)
        if awe_list is None:
            comments_labal.config(text="已加载所有评论", fg="green")
            break

        for comments_data in awe_list:
            nickname = comments_data['user']['nickname']
            ip_label = comments_data['ip_label']
            text = comments_data['text']
            create_time = comments_data['create_time']
            create_time = convert_timestamp_to_datetime(create_time)
            unique_id = comments_data['user']['unique_id']
            reply_comment_total = comments_data['reply_comment_total']
            sec_uid = comments_data['user']['sec_uid']
            comment_uid = comments_data['cid']

            tree_comments.insert('', tk.END,
                                 values=(num, nickname, ip_label, text, create_time, unique_id, reply_comment_total),
                                 tags=(sec_uid, comment_uid))
            num += 1

        new_cursor = json_comments.get('cursor', '0')
        if new_cursor == current_cursor:
            comments_labal.config(text="已加载所有评论", fg="green")
            break
        current_cursor = new_cursor

        if mode != "all":
            comments_labal.config(text=f"加载了{num - 1}条评论", fg="blue")
            break

    if mode == "all":
        current_cursor = '0'
        comments_labal.config(text=f"已加载所有{num - 1}条评论", fg="green")


@threaded
def tree_comments_level2(mode='first'):
    global cursor_level2, count_level2, num_level2

    selected_item = tree_user_video.focus()

    if not selected_item:
        messagebox.showwarning("未选中", "请先在用户视频表格中选中一行。")
        return

    aweme_id = tree_user_video.item(selected_item, 'tags')[0]

    selected_item = tree_comments.selection()

    if not selected_item:
        messagebox.showwarning("未选中", "请先选中一个评论内容。")
        return
    tags = tree_comments.item(selected_item, "tags")
    comment_uid = tags[1]

    if mode == 'first':
        clear_treeview1(tree_comments_level)
        cursor_level2 = '0'
        count_level2 = '50'
        num_level2 = 1
    elif mode == 'more':
        count_level2 = str(int(count_level2) + 50)
    elif mode == 'all':
        clear_treeview1(tree_comments_level)
        cursor_level2 = '0'
        num_level2 = 1

    while True:
        params = comments_level2(item_id=aweme_id, comment_id=comment_uid, cursor_level2=cursor_level2,
                                 count_level2=count_level2)

        if mode in ['more', 'all']:
            params['whale_cut_token'] = ""

        headers = headers_all()
        headers['user-agent'] = ''

        response = requests.get(
            'https://www.douyin.com/aweme/v1/web/comment/list/reply/',
            params=get_signature(params),
            cookies=get_cookie(),
            headers=headers,
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        response_text = response.text
        # print("响应内容:", response_text)
        json_data = json.loads(response.text)


        if not json_data.get('comments'):
            comments_labal.config(text="已加载所有二级评论", fg="green")
            break


        num = 1
        for comments_data in json_data['comments']:
            nickname = comments_data['user']['nickname']
            create_time = comments_data["create_time"]
            create_time = convert_timestamp_to_datetime(create_time)
            text = comments_data["text"]
            unique_id = comments_data['user']['unique_id']
            reply_to_reply_id = comments_data["reply_to_reply_id"]
            digg_count = comments_data["digg_count"]
            sec_uid = comments_data['user']['sec_uid']
            signature = comments_data['user']['signature']
            reply_to_username = None

            if reply_to_reply_id != "0":
                reply_to_username = comments_data["reply_to_username"]

            tree_comments_level.insert('', tk.END,
                                       values=(
                                           num_level2, nickname, create_time, text, reply_to_username, digg_count,
                                           unique_id,
                                           signature,),
                                       tags=(sec_uid, reply_to_reply_id))
            num_level2 += 1

        cursor_level2 = json_data.get('cursor', cursor_level2)

        if json_data.get('has_more') != 1:
            comments_labal.config(text="已加载所有二级评论", fg="green")
            break

        if mode != 'all':
            comments_labal.config(text=f"已加载{num_level2 - 1}条二级评论", fg="blue")
            break


def save_to_excel1():
    columns = [tree_comments.heading(col)['text'] for col in tree_comments['columns']]
    data = [tree_comments.item(row)['values'] for row in tree_comments.get_children()]

    df = pd.DataFrame(data, columns=columns)

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx")])

    if file_path:
        df.to_excel(file_path, index=False)


def export_to_excel():
    rows = []
    for item in tree_comments.get_children():
        row = tree_comments.item(item)['values']
        rows.append(row)

    columns = ['序号', '昵称', 'IP地址', '评论内容', '评论时间', '抖音号', '二级评论数量']

    df = pd.DataFrame(rows, columns=columns)

    selected_item = tree_user_video.selection()
    title_name = tree_user_video.item(selected_item, 'values')[4]

    title_name = re.sub(r'[<>:"/\\|?*]', '', title_name)
    save_path = f"{title_name}.xlsx"

    with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        cell_format = workbook.add_format({'align': 'left'})

        for col_num, _ in enumerate(df.columns):
            worksheet.set_column(col_num, col_num, None, cell_format)

    comments_labal.config(text=f"数据已导出到 {save_path}", fg="green")


def clear_treeview1(a):
    for item in a.get_children():
        a.delete(item)







root = tk.Tk()
root.title("小爪巴1.0")


center_window(root, 1200, 600)

button_frame = tk.Frame(root, width=200, bg="lightgray")
button_frame.pack(side="left", fill="y")

view_frame1 = tk.Frame(root, bg='white')
view_frame2 = tk.Frame(root, bg='black')
view_frame3 = tk.Frame(root, bg='pink')
view_frame4 = tk.Frame(root, bg='white')

frames = [view_frame1, view_frame2, view_frame3, view_frame4]

label1 = tk.Label(view_frame4, text="公告:\n\n小爪巴1.0\n本软件仅供学习交流, 严禁违法使用！",
                  font=('微软雅黑', 12),
                  fg="red", bg="white")
label1.pack(anchor='center', padx=20, pady=250)

top_frame = tk.Frame(view_frame1, bg="white")
top_frame.pack(side="top", fill="x")
under_frame = tk.Frame(view_frame1, bg='grey')
under_frame.pack(side='top', fill='both', expand=True)

current_offset = 0

image = Image.open("icon/log on.png")
photo = ImageTk.PhotoImage(image)

image_button = ttk.Button(top_frame, image=photo, command=lambda: login_and_save_cookies())
image_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

image_button.image = photo

selected_option = tk.StringVar()
combobox = ttk.Combobox(top_frame, textvariable=selected_option, width=15,
                        values=['用户搜索', '综合搜索', '视频搜索'], state='readonly')
combobox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
combobox.current(0)

print("默认选项:", selected_option.get())

search_entry = tk.Entry(top_frame, width=20)
search_entry.grid(row=0, column=2, padx=5, pady=5, sticky='w')

search_button = tk.Button(top_frame, text='搜索', bg="pink", command=on_search)
search_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

columns = ('序号', '昵称', '链接', '抖音ID', '抖音号', '个性签名', '认证')
treeview = ttk.Treeview(under_frame, columns=columns, show='headings')

scrollbar = tk.Scrollbar(under_frame, orient="vertical", command=treeview.yview)
treeview.configure(yscrollcommand=scrollbar.set)

treeview.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

treeview.column("序号", width=50, minwidth=50, anchor='center')
treeview.column("昵称", width=150, minwidth=100, anchor='center')
treeview.column("链接", width=150, minwidth=100, anchor='center')
treeview.column("抖音ID", width=130, minwidth=100, anchor='center')
treeview.column("抖音号", width=130, minwidth=100, anchor='center')
treeview.column("个性签名", width=200, minwidth=150, anchor='center')
treeview.column("认证", width=180, minwidth=150, anchor='center')

treeview.heading("序号", text="序号")
treeview.heading("昵称", text="昵称")
treeview.heading("链接", text="链接")
treeview.heading("抖音ID", text="抖音ID")
treeview.heading("抖音号", text="抖音号")
treeview.heading("个性签名", text="个性签名")
treeview.heading("认证", text="认证")

top_frame.grid_rowconfigure(1, weight=1)
top_frame.grid_columnconfigure(3, weight=1)

status_label = tk.Label(top_frame, text="检测中...", bg='white')
status_label.grid(row=0, column=4, padx=5, pady=5, sticky='w')
check_cookie_file()

get_more_button = tk.Button(top_frame, text="+10", bg='pink', command=on_get_10_more)
get_more_button.grid(row=0, column=5, padx=5, pady=5, sticky='w')

get_50_more_button = tk.Button(top_frame, text="+50", bg='pink', command=on_get_50_more)
get_50_more_button.grid(row=0, column=6, padx=5, pady=5, sticky='w')

right_click_menu = Menu(top_frame, tearoff=0)
right_click_menu.add_command(label="进入该博主的主页",
                             command=lambda: open_user_page(selected_item=treeview.selection(),
                                                            unique_id=treeview.item(treeview.selection()[0], 'values')[
                                                                2]))
right_click_menu.add_command(label="查看该博主详细信息",
                             command=lambda: show_user_info(selected_item=treeview.selection(),
                                                            sec_uid=treeview.item(treeview.selection(), 'values')[2]))

treeview.bind("<Button-3>", lambda event: show_right_click_menu(event, treeview, right_click_menu))

user_top_frame = tk.Frame(view_frame2, bg='white')
user_top_frame.pack(side="top", fill="both", expand=True)
user_under_frame = tk.Frame(view_frame2, bg='white')
user_under_frame.pack(side="bottom", fill="x")

vsb = ttk.Scrollbar(user_top_frame, orient="vertical")
hsb = ttk.Scrollbar(user_top_frame, orient="horizontal")

columns = (
    "序号", "昵称", "媒体类型", "媒体链接", "标题", "发布时间", "BGM", "时长", "点赞数",
    "评论数", "收藏数", "转发数")

tree_user_video = ttk.Treeview(user_top_frame, columns=columns, show="headings", yscrollcommand=vsb.set,
                               xscrollcommand=hsb.set)

tree_user_video.heading("序号", text="序号")
tree_user_video.heading("昵称", text="昵称")
tree_user_video.heading("媒体类型", text="媒体类型")
tree_user_video.heading("媒体链接", text="媒体链接")
tree_user_video.heading("标题", text="标题")
tree_user_video.heading("发布时间", text="发布时间")
tree_user_video.heading("BGM", text="BGM")
tree_user_video.heading("时长", text="时长")
tree_user_video.heading("点赞数", text="点赞数")
tree_user_video.heading("评论数", text="评论数")
tree_user_video.heading("收藏数", text="收藏数")
tree_user_video.heading("转发数", text="转发数")

for col in columns:
    tree_user_video.column(col, width=100, anchor="center")

tree_user_video.grid(row=0, column=0, sticky="nsew")
vsb.config(command=tree_user_video.yview)
hsb.config(command=tree_user_video.xview)

vsb.grid(row=0, column=1, sticky="ns")
hsb.grid(row=1, column=0, sticky="ew")

user_top_frame.grid_rowconfigure(0, weight=1)
user_top_frame.grid_columnconfigure(0, weight=1)

menu = Menu(view_frame2, tearoff=0)
menu.add_command(label="复制媒体链接", command=copy_media_url)
menu.add_command(label="清空表格", command=clear_treeview)
menu.add_command(label="查看aweme_id", command=lambda: on_item_selected())


def show_context_menu(event):
    selected_item = tree_user_video.identify_row(event.y)
    if selected_item:
        tree_user_video.selection_set(selected_item)
        menu.post(event.x_root, event.y_root)


def update_label(event):
    selected_item = treeview.selection()
    if selected_item:
        values = treeview.item(selected_item, 'values')
        nick_ = f'选中博主：{values[1]} '
    else:
        nick_ = ''

    message_label.config(text=nick_)


tree_user_video.bind("<Button-3>", show_context_menu)

message_label = tk.Label(user_under_frame, text='尚未选中博主', fg="green", bg='white')
message_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

treeview.bind("<<TreeviewSelect>>", update_label)

progress = ttk.Progressbar(user_under_frame, orient="horizontal", length=400, mode='determinate')
progress.grid(row=1, column=0, sticky="w", padx=5, pady=5)

user_under_frame.columnconfigure(1, weight=1)

btn_fetch = tk.Button(user_under_frame, text="获取信息", command=lambda: fetch_data(mode="first"))
btn_fetch.grid(row=0, column=2, sticky="e", padx=5, pady=5)

fetch_more_button = tk.Button(user_under_frame, text="获取更多", command=lambda: fetch_data(mode="more"))
fetch_more_button.grid(row=0, column=3, sticky="e", padx=5, pady=5)

fetch_all_button = tk.Button(user_under_frame, text="获取全部视频", command=lambda: fetch_data(mode="all"))
fetch_all_button.grid(row=0, column=4, sticky="e", padx=5, pady=5)

btn_save = tk.Button(user_under_frame, text="下载Excel", command=save_to_excel)
btn_save.grid(row=1, column=2, sticky="e", padx=5, pady=5)

btn_download = tk.Button(user_under_frame, text="下载视频", command=download_media)
btn_download.grid(row=1, column=3, sticky="e", padx=5, pady=5)

user_under_frame.grid_rowconfigure(0, weight=0)


comments_top_frame = tk.Frame(view_frame3, bg="white")
comments_top_frame.pack(side="top", fill="x")
comments_mid_frame = tk.Frame(view_frame3, bg="white")
comments_mid_frame.pack(side="top", fill="x")
comments_under_frame = tk.Frame(view_frame3, bg='white')
comments_under_frame.pack(side='top', fill='both', expand=True)


tree_comments = ttk.Treeview(comments_top_frame,
                             columns=('序号', '昵称', 'IP地址', '评论内容', '评论时间', '抖音号', '二级评论数量'),
                             show='headings')


tree_comments.column("序号", anchor="center", width=50)
tree_comments.column("昵称", anchor="center", width=200)
tree_comments.column("IP地址", anchor="center", width=100)
tree_comments.column("评论内容", anchor="center", width=350)
tree_comments.column("评论时间", anchor="center", width=100)
tree_comments.column("抖音号", anchor="center", width=150)
tree_comments.column("二级评论数量", anchor="center", width=150)


tree_comments.heading('序号', text='序号')
tree_comments.heading('昵称', text='昵称')
tree_comments.heading('IP地址', text='IP地址')
tree_comments.heading('评论内容', text='评论内容')
tree_comments.heading('评论时间', text='评论时间')
tree_comments.heading('抖音号', text='抖音号')
tree_comments.heading('二级评论数量', text='二级评论数量')


comments_menu = Menu(comments_top_frame, tearoff=0)
comments_menu.add_command(label="进入该播主主页",
                          command=lambda: open_user_page(selected_item=tree_comments.selection(),
                                                         unique_id=
                                                         tree_comments.item(tree_comments.selection(),
                                                                            'tags')[0]))
comments_menu.add_command(label="查看该博主详细信息",
                          command=lambda: show_user_info(selected_item=tree_comments.selection(), sec_uid=
                          tree_comments.item(tree_comments.selection(), 'tags')[0]))
comments_menu.add_command(label="获取该博主昵称", command=lambda: copy_nickname(tree_comments))
comments_menu.add_command(label="清空表格", command=lambda: clear_treeview1(tree_comments))


tree_comments.bind('<Button-3>', lambda event: show_right_click_menu(event, tree_comments, comments_menu))



scrollbar = ttk.Scrollbar(comments_top_frame, orient="vertical", command=tree_comments.yview)
tree_comments.configure(yscrollcommand=scrollbar.set)

tree_comments.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


comments_labal = tk.Label(comments_under_frame, text='', fg='green', bg='white', anchor='w')
comments_labal.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='we')


button_first = tk.Button(comments_under_frame, text='   搜索评论   ', command=lambda: fetch_comments("first"))
button_first.grid(row=1, column=0, padx=10, pady=10, sticky='w')

button_more = tk.Button(comments_under_frame, text='   +1组评论   ', command=lambda: fetch_comments("more"))
button_more.grid(row=1, column=1, padx=10, pady=10, sticky='w')

button_all = tk.Button(comments_under_frame, text='   获取全部评论   ', command=lambda: fetch_comments("all"))
button_all.grid(row=1, column=2, padx=10, pady=10, sticky='w')

button_first_levele2 = tk.Button(comments_under_frame, text='搜索二级评论',
                                 command=lambda: tree_comments_level2("first"))
button_first_levele2.grid(row=2, column=0, padx=10, pady=10, sticky='w')

button_more_levele2 = tk.Button(comments_under_frame, text='+1组二级评论', command=lambda: tree_comments_level2("more"))
button_more_levele2.grid(row=2, column=1, padx=10, pady=10, sticky='w')

button_all_levele2 = tk.Button(comments_under_frame, text='获取全部二级评论',
                               command=lambda: tree_comments_level2("all"))
button_all_levele2.grid(row=2, column=2, padx=10, pady=10, sticky='w')


export_button = tk.Button(comments_under_frame, text='导出为Excel', command=save_to_excel1)
export_button.grid(row=2, column=10, padx=10, pady=10, sticky='w')


comments_under_frame.grid_columnconfigure(0, weight=0)
comments_under_frame.grid_columnconfigure(1, weight=0)
comments_under_frame.grid_columnconfigure(2, weight=1)
comments_under_frame.grid_columnconfigure(10, weight=0)

tree_comments_level = ttk.Treeview(comments_mid_frame, columns=(
    "编号", "昵称", "评论时间", "回复内容", "回复给谁", "点赞数", "抖音号", "用户签名",), show="headings")
tree_comments_level.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(comments_mid_frame, orient="vertical", command=tree_comments_level.yview)
tree_comments_level.configure(yscrollcommand=scrollbar.set)

tree_comments_level.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tree_comments_level.heading("编号", text="编号")
tree_comments_level.heading("昵称", text="昵称")
tree_comments_level.heading("评论时间", text="评论时间")
tree_comments_level.heading("回复内容", text="回复内容")
tree_comments_level.heading("回复给谁", text="回复给谁")
tree_comments_level.heading("点赞数", text="点赞数")
tree_comments_level.heading("抖音号", text="抖音号")
tree_comments_level.heading("用户签名", text="用户签名")

tree_comments_level.column("编号", anchor="center", width=50)
tree_comments_level.column("昵称", anchor="center", width=100)
tree_comments_level.column("评论时间", anchor="center", width=150)
tree_comments_level.column("回复内容", width=300)
tree_comments_level.column("回复给谁", anchor="center", width=100)
tree_comments_level.column("点赞数", anchor="center", width=50)
tree_comments_level.column("抖音号", anchor="center", width=120)
tree_comments_level.column("用户签名", anchor="center", width=200)

level2_memu = Menu(comments_mid_frame, tearoff=0)
level2_memu.add_command(label="进入该播主主页",
                        command=lambda: open_user_page(selected_item=tree_comments_level.selection(),
                                                       unique_id=
                                                       tree_comments_level.item(tree_comments_level.selection(),
                                                                                'tags')[0]))
level2_memu.add_command(label="查看该博主详细信息",
                        command=lambda: show_user_info(selected_item=tree_comments_level.selection(), sec_uid=
                        tree_comments_level.item(tree_comments_level.selection(), 'tags')[0]))

level2_memu.add_command(label="获取该博主昵称", command=lambda: copy_nickname(tree_comments_level))
level2_memu.add_command(label="清空表格", command=lambda: clear_treeview1(tree_comments_level))

tree_comments_level.bind('<Button-3>', lambda event: show_right_click_menu(event, tree_comments_level, level2_memu))

view_frame4.pack(side="right", fill="both", expand=True)
for frame in frames[4:]:
    frame.pack_forget()


add_button(button_frame, frames)

root.mainloop()
