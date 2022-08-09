'''
Author: emmovo mingjkl@live.com
Date: 2022-08-09 01:02:18
LastEditors: emmovo mingjkl@live.com
LastEditTime: 2022-08-09 21:11:32
FilePath: \screenshot\Timed_screenshots.py
'''

import os
import re
from shutil import copyfile
import time
import datetime
from pynput.keyboard import Key, Controller

last_data_max_num = 0
current_data_max_num = 0


dir_orgin = "C:\\Users\\mingj\\OneDrive\\图片\\屏幕快照\\"  # 截屏文件保存路径
dir_target = "D:\\Git\\screenshot\\screenshot\\"    # 截屏目标保存路径

screenshot_time = 1;
screenshot_file_mtime = 0;
keyboard = Controller()

# ============================== 通过按键模拟截图 ============================

while screenshot_file_mtime < screenshot_time:      # 对比截图时间和最大序号文件创建时间

    screenshot_time = time.time();
    
    # keyboard.press(Key.shift_l)
    keyboard.press(Key.print_screen)    # 出发截屏按键
    time.sleep(0.5)
    keyboard.release(Key.print_screen)
    # keyboard.release(Key.shift_l)
    time.sleep(2)  # 等待截屏完成

    dt = datetime.datetime.now()  # 获取当前时间


    # 截图源文件日期格式    eg.2022-08-09 (34).png => 2022-08-09
    orgin_dir_str = dt.strftime("%Y-%m-%d")
    # 保存文件格式  04-41-08.png
    target_dir_str = dt.strftime("%H-%M-%S")


    if os.path.exists(dir_target + orgin_dir_str) == False:
        os.makedirs(dir_target + orgin_dir_str)



    dir_orgin_list = os.listdir(dir_orgin)  # 获取文件夹内所有文件名清单
    data_str_pat = re.compile(orgin_dir_str)    # 筛选当日文件的正则表达式


    # 提出文件名序号的正则表达式    eg.2022-08-09 (34).png => 34
    value_pat_str = re.compile("\(\d+\)")

    for line in dir_orgin_list:     # 变量文件名列表
        if(re.search(data_str_pat, line)):       # 筛选出当日的文件 eg.2022-08-09 (34).png => 2022-08-09
            current = int(str(value_pat_str.findall(line)).replace(
                "['(", '').replace(")']", ''))  # 获取当前遍历到的文件序号 eg.2022-08-09 (34).png => 34
            if current > current_data_max_num:      # 捕获最大的序号
                current_data_max_num = current      # 保存最大序号
                max_date_file_name = line            # 保存最大序号的文件文件名
    
    dir_orgin_out = dir_orgin + max_date_file_name          # 生成目标路径
    screenshot_file_mtime = os.path.getmtime(dir_orgin_out)     # 获取最大序号文件的创建时间

    # print("st:", screenshot_time, "fmt:", screenshot_file_mtime)


# ============================== 截图转存至设定目录 ============================

dir_target = dir_target + orgin_dir_str + '\\' + target_dir_str + '.png'   # 生成保存位置路径

copyfile(dir_orgin_out, dir_target)     # 复制截图文件至目标文件夹
os.remove(dir_orgin_out)    # 删除原截图文件

# ============================== 清空 5 天以为的截图记录 ============================

folder_path = ".\\screenshot"
folder_list = []
folder_list = os.listdir(folder_path)

for file in folder_list:
    file_path = folder_path + "\\" + file
    # print(os.path.getmtime(file_path), screenshot_time)
    if os.path.getmtime(file_path) < (screenshot_time - 432000):
        file_list = os.listdir(file_path)
        # print(file_list)
        for file_d in file_list:
            os.remove(file_path + '\\' + file_d)
        os.rmdir(file_path)


