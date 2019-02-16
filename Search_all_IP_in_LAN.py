#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Time    : 2019/2/16 8:59
# @Author : Jackie Yang
# File    : Search_all_IP_in_LAN.py
# Project : Search_all_IP_in_LAN
# Version : v0.1

from progressbar import *
import os
import re
import time


def arp_del():
    with open("./temp.bat", "w", newline='') as bat:
        bat.write(
            '''@echo off\r\n%1 %2\r\nver|find "5.">nul&&goto :st\r\nmshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :st","","runas",1)(window.close)&goto :eof\r\n:st\r\ncopy "%~0" "%windir%\system32\\"\r\narp -d''')
    os.system('cmd.exe /c ' + os.path.dirname(os.path.abspath(__file__)) + r'\temp.bat')
    os.remove('temp.bat')


def run():
    arp_del()
    # noinspection PyBroadException
    try:
        var = os.popen("arp -a").read()
        ip_address = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", var, flags=0).group()
        print("本机IP: ", ip_address)
        var = ip_address.split(".")
        ip = var[0] + "." + var[1] + "." + var[2] + "."
    except Exception as e:
        print(e)
        return
    # noinspection PyBroadException
    try:
        mac = input("请输入MAC地址(以‘-’间隔)：").lower()
        mac = re.search(r"[a-zA-Z0-9]{1,2}\-[a-zA-Z0-9]{1,2}\-[a-zA-Z0-9]{1,2}\-"
                        r"[a-zA-Z0-9]{1,2}\-[a-zA-Z0-9]{1,2}\-[a-zA-Z0-9]{1,2}", mac, flags=0).group()
    except Exception as e:
        print("输入错误！")
        return
    print("MAC: %s" % mac)
    progress = ProgressBar()
    for i in progress(range(1, 256)):
        os.popen("ping -n 1 " + ip + str(i))
        time.sleep(0.01)
    var = os.popen("arp -a").read()
    l = var.split(" ")
    for i in range(len(l)):
        if l[i] == mac:
            for j in range(1, 20):
                if l[i - j] != "":
                    print("IP地址:", l[i - j])
                    break
            break
    else:
        print("MAC不在局域网中!")


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(e)
    finally:
        input("输入 Enter 退出")
