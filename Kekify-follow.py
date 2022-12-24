# -*- coding: utf8 -*-

from colorama import Fore
import configparser
import threading
import os
from spotify import spotify
import random
import requests

os.system('title Kekify - Takipçi Botu')

version = 4

parser = configparser.ConfigParser()
parser.read('ayarlar.ini')

settings = parser['Ayarlar']

print(f"""
    {Fore.MAGENTA}
 _   __     _    _  __       
| | / /    | |  (_)/ _|      
| |/ /  ___| | ___| |_ _   _ 
|    \ / _ \ |/ / |  _| | | |
| |\  \  __/   <| | | | |_| |
\_| \_/\___|_|\_\_|_|  \__, |
                        __/ |
                       |___/  {Fore.RESET}

""")

print(f"{Fore.YELLOW}Kekn9ne tarafından yapıldı. | https://discord.gg/B5qETBUGQ6")

result = requests.get('?')

if settings['FotografKullan'] != "True" and settings['FotografKullan'] != "False":
    settings['FotografKullan'] = "True"

error = 0
proxy = 0
success = 0

def start():
    global error
    global proxy
    global success
    if os.path.getsize("proxyler.txt") != 0:
        proxy = random.choice(open("proxyler.txt").readlines())
        result = spotify(settings['Baglanti'], settings['TakipTuru'], settings['FotografKullan'], proxy).follow()
        if result == "error":
            error = error + 1
        elif result == "proxy_detected":
            proxy = proxy + 1
        if result == "success":
            success = success + 1
        else:
            print(result)

        print(f"{Fore.GREEN}Başarılı: {success} {Fore.RESET}| {Fore.YELLOW}Hata: {error} {Fore.RESET}| {Fore.RED}Proxy Tespiti: {proxy} {Fore.RESET}", end="\r")
    else: 
        result = spotify(settings['Baglanti'], settings['TakipTuru'], settings['FotografKullan']).follow()
        if result == "error":
            error = error + 1
        elif result == "proxy_detected":
            proxy = proxy + 1
        elif result == "success":
            success = success + 1
        else:
            print(result)
        print(f"{Fore.GREEN}Başarılı: {success} {Fore.RESET}| {Fore.YELLOW}Hata: {error} {Fore.RESET}| {Fore.RED}Proxy Tespiti: {proxy} {Fore.RESET}", end="\r")

if result.json()['status'] == False:
    print(f"{Fore.RED}Botu kullanabilmeniz için Discord sunucumuzdan IP adresinizi onaylamanız gerekmektedir.")
    while True:
        input()
elif result.json()['version'] > version:
    print(f"{Fore.RED}Kullandığınız sürüm eski. Lütfen Discord sunucumuzdan yeni sürümü indirin.")
    while True:
        input()
else:    
    while True:
        if threading.active_count() < int(settings['ThreadSayisi']) + 1:
            threading.Thread(target = start).start()