import os
import shutil
import time
from pathlib import Path
import winreg
from tkinter import simpledialog
import tkinter.messagebox
import sys


def get_next_file(dest_dir, file_name):
    dest = os.path.join(dest_dir, file_name)
    num = 0

    while os.path.exists(dest):
        num += 1

        period = file_name.rfind('.')
        if period == -1:
            period = len(file_name)

        new_file = f'{file_name[:period]}({num}){file_name[period:]}'

        dest = os.path.join(dest_dir, new_file)

    return dest

def get_input():
    input = None
    while input == None or input == '':
        input = simpledialog.askstring('WeChat Files Reset','                  首次运行请输入根目录                  ')
        if input == None:
            sys.exit(0)
        elif input == '':
            tkinter.messagebox.showerror('WeChat Files Reset', 'Path Cannot Be Blank! Please Try Again!')
    return input


try:
    global key_value
    reg_path = r"SOFTWARE\WeChat Files Reset"
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
    key_value = winreg.QueryValueEx(key,'path')
    winreg.CloseKey(key)

except FileNotFoundError as e:
        input = get_input()
        key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, 'path', 0, winreg.REG_SZ, input)
        key_value = [0]
        key_value[0] = input
        winreg.CloseKey(key)


file_path = os.path.join(key_value[0], 'FileStorage', 'MsgAttach')
out_path = os.path.join(key_value[0],'FileStorage', 'File')

for dirpath, dirnames, filenames in os.walk(file_path):

    file_list = os.listdir(dirpath)

    for file in file_list:

        if os.path.splitext(file)[1] != ".dat" and os.path.splitext(file)[1] != ".jpg" and os.path.splitext(file)[1] != "":
            info = os.stat(os.path.join(dirpath, file))
            time_path = str(time.localtime(info.st_mtime).tm_year)+"-"+str(time.localtime(info.st_mtime).tm_mon).zfill(2)
            new_path = Path(out_path)/time_path
            if not new_path.exists():
                new_path.mkdir()

            if os.path.exists(os.path.join(new_path, file)) :
                shutil.move(os.path.join(dirpath, file), get_next_file(new_path, file))

            else:
                shutil.move(os.path.join(dirpath, file), os.path.join(new_path, file))

os.startfile(out_path)







