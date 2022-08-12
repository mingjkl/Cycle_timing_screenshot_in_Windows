

import os
from queue import Empty
import re
from shutil import copyfile
import time
import datetime
from pynput.keyboard import Key, Controller

print("hw")

save_path = "E:\\temp\\TrayIcon\\SavePath.pt"
save_path_ready = False

dir_target = ""
dir_orgin = ""
if os.path.exists(save_path) == True:
    save_file = open(save_path, 'r', encoding = "utf_8")
    save_file_lines = save_file.readlines()
    for line in save_file_lines:
        if line.startswith("SCREENSHOT_PATH:"):
            dir_target = line.replace("SCREENSHOT_PATH:", "")
            dir_target = dir_target.strip()
            dir_target = dir_target + "/"
            dir_target = dir_target.replace("/", "\\")
            print(dir_target)
        if line.startswith("SAVE_PATH:"):
            dir_orgin = line.replace("SAVE_PATH:", "")
            dir_orgin = dir_orgin.strip()
            dir_orgin = dir_orgin + "/"
            dir_orgin = dir_orgin.replace("/", "\\")
            print(dir_orgin)

if (dir_target != "") and (dir_orgin !=""):
    if os.path.exists(dir_target) and os.path.exists(dir_orgin):
        save_path_ready = True


# dir_orgin = "C:\\Users\\emmov\\OneDrive\\图片\\屏幕快照\\"  # 截屏文件保存路径
# dir_target = "E:\\temp\\TrayIcon\\screenshot\\"    # 截屏目标保存路径

if save_path_ready == True:

    keyboard = Controller()

    finish_screenshot = False

    while finish_screenshot == False: 
        screenshot_time = time.time()

        keyboard.press(Key.print_screen)    # 出发截屏按键
        time.sleep(0.5)
        keyboard.release(Key.print_screen)
        time.sleep(2)  # 等待截屏完成

        dt = datetime.datetime.now()  # 获取当前时间

        data_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H-%M-%S")

        if os.path.exists(dir_target + data_str) == False:
            os.makedirs(dir_target + data_str)

        dir_orgin_list = os.listdir(dir_orgin)  # 获取文件夹内所有文件名清单

        finish_screenshot = False
        newest_file_path = ""

        for item in dir_orgin_list:
            dir_orgin_out = dir_orgin + item
            if (os.path.getmtime(dir_orgin_out)) > screenshot_time:
                finish_screenshot = True
                newest_file_path = dir_orgin_out
                
    print(newest_file_path)

    # # ============================== 截图转存至设定目录 ============================

    png_target = dir_target  + data_str + "\\" + time_str + '.png'   # 生成保存位置路径

    copyfile(newest_file_path, png_target)     # 复制截图文件至目标文件夹
    os.remove(newest_file_path)    # 删除原截图文件

    # ============================== 清空 5 天以为的截图记录 ============================

    folder_path = dir_target
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




