# -*- coding: utf8 -*-

from colorama import Fore
import requests, random, string
import base64, json

class spotify:

    def __init__(self, profile, type, photo, proxy = None):
        self.session = requests.Session()
        self.profile = profile
        self.type = int(type)
        self.proxy = proxy
        self.photo = eval(photo)
    
    def replace_all(self, text, dic):
        for i, j in dic.items():
            text = text.replace(i, j)

            if i == "ı":
                break

            text = text.replace(i.upper(), j.upper())
        return text

    def register_account(self):
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "tr-TR,tr;q=0.9",
            "content-type": "application/json",
            "origin": "https://www.spotify.com",
            "referer": "https://www.spotify.com/",
            "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }
        email = ("").join(random.choices(string.ascii_letters + string.digits, k = 8)) + "@hizli.email"
        password = ("").join(random.choices(string.ascii_letters + string.digits, k = 8))

        response = requests.get('https://rp.burakgarci.net/api.php')

        gender = response.json()['cinsiyet']

        # tryna make names realistic
        scenario = random.randint(0,3)
        if scenario == 0:
            name = response.json()['isim']
        elif scenario == 1:
            name = response.json()['isim'].lower()
        elif scenario == 2:
            name = response.json()['tam_isim']
        elif scenario == 3:
            name = response.json()['tam_isim'].lower()

        name = self.replace_all(name, {"ş": "s", "ö": "o", "ç": "c", "İ": "I", "ğ": "g", "ü": "u", "ı": "i"})

        data = {
            "account_details": {
                "birthdate": "2001-06-23",
                "consent_flags": {
                    "eula_agreed": True,
                    "send_email": False,
                    "third_party_email": True
                },
                "display_name": name,
                "email_and_password_identifier": {
                    "email": email,
                    "password": password
                },
                "gender": 1
            },
            "callback_uri": "https://www.spotify.com/signup/challenge?locale=tr",
            "client_info": {
                "api_key": "a1e486e2729f46d6bb368d6b2bcda326",
                "app_version": "v2",
                "capabilities": [1],
                "installation_id": "07b84cda-709c-432e-af56-84245c6e4294",
                "platform": "www"
            },
            "tracking": {
                "creation_flow": "",
                "creation_point": "https://www.spotify.com/tr/",
                "referrer": ""
            }
        }

        #data = f"birth_day=1&birth_month=01&birth_year=1970&collect_personal_info=undefined&creation_flow=&creation_point=https://www.spotify.com/tr/&displayname={name}&email={email}&gender=neutral&iagree=1&key=a1e486e2729f46d6bb368d6b2bcda326&password={password}&password_repeat={password}&platform=www&referrer=&send-email=1&thirdpartyemail=0&fb=0"
    
        try:
            create = self.session.post("https://spclient.wg.spotify.com/signup/public/v2/account/create", headers = headers, json = data)
            if "login_token" in create.text:
                login_token = create.json()['success']['login_token']
                username = create.json()['success']['username']
                with open("hesaplar.txt", "a") as f:
                    f.write(f'{email}:{password}:{login_token}\n')

                image = self.session.get(f'https://kekn9ne.xyz/api.php?cinsiyet={gender}', headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"})

                return [login_token, username, image.text]
            elif "proxy" in create.json()['errors']['generic_error'].lower():
                return "Proxy", None, None
            else:
                return None, None, None
        except:
            return "error", None, None

    def get_csrf_token(self):
        try:
            r = self.session.get("https://www.spotify.com/tr/signup/?forward_url=https://accounts.spotify.com/en/status&sp_t_counter=1")
            return r.text.split('csrfToken":"')[1].split('"')[0]
        except:
            return f"{Fore.RED}CSRF Token alınırken hata oluştu."
        
    def get_token(self, login_token):
        headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRF-Token": self.get_csrf_token(),
            "Host": "www.spotify.com"
        }
        try:
            self.session.post("https://www.spotify.com/api/signup/authenticate", headers = headers, data = "splot=" + login_token)
        except:
            return None

        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "spotify-app-version": "1.1.52.204.ge43bc405",
            "app-platform": "WebPlayer",
            "Host": "open.spotify.com",
            "Referer": "https://open.spotify.com/"
        }
        try:
            r = self.session.get(
                "https://open.spotify.com/get_access_token?reason=transport&productType=web_player",
                headers = headers
            )
            return r.json()["accessToken"]
        except:
            return None

    def change_picture(self, auth_token, username, image_url):
        image = self.session.get(image_url, stream=True, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"})
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "access-control-request-headers": "authorization,content-type",
            "access-control-request-method": "post",
            "origin": "https://open.spotify.com",
            "referer": "https://open.spotify.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        }
        r = self.session.options("https://image-upload.spotify.com/v4/user-profile", headers = headers)
        
        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "content-type": "image/jpeg",
            "accept-language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "Referer": "https://open.spotify.com/",
            "sec-ch-ua": "\"Chromium\";v=\"104\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"104\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "authorization": "Bearer {}".format(auth_token),
        }

        # open("pp.png", "rb").read()
        try:
            r = self.session.post("https://image-upload.spotify.com/v4/user-profile", headers = headers, data = image.content)
            upload_token = r.json()['uploadToken']
        except:
            return "error"

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "access-control-request-headers": "app-platform,authorization,spotify-app-version",
            "access-control-request-method": "post",
            "origin": "https://open.spotify.com",
            "referer": "https://open.spotify.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        }
        try:
            r = self.session.options(f"https://spclient.wg.spotify.com/identity/v3/profile-image/{username}/{upload_token}", headers = headers)
        except:
            return "error"

        headers = {
            "accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "en",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
            "app-platform": "WebPlayer",
            "Referer": "https://open.spotify.com/",
            "spotify-app-version": "1.1.52.204.ge43bc405",
            "authorization": "Bearer {}".format(auth_token),
        }
        try:
            r = self.session.post(f"https://spclient.wg.spotify.com/identity/v3/profile-image/{username}/{upload_token}", headers = headers)
        except:
            return "error"
        
    def follow(self):
        if self.proxy != None:
            proxies = {
                'http': self.proxy,
                'https': self.proxy
            }
            self.session.proxies.update(proxies)

        if self.type == 0:
            if "/user/" in self.profile:
                self.profile = self.profile.split("/user/")[1]
            if "?" in self.profile:
                self.profile = self.profile.split("?")[0]
            login_token, username, image_url = self.register_account()
            if login_token == None:
                return "error"
            elif login_token == False:
                return "error"
            elif login_token == "Proxy":
                return "proxy_detected"
            elif login_token == "error":
                return "error"
                
            auth_token = self.get_token(login_token)
            if auth_token == None:
                return "error"

            if self.photo == True:
                img = self.change_picture(auth_token, username, image_url)
                if img == "error":
                    return "error"

            headers = {
                "accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "accept-language": "en",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                "app-platform": "WebPlayer",
                "Referer": "https://open.spotify.com/",
                "spotify-app-version": "1.1.52.204.ge43bc405",
                "authorization": "Bearer {}".format(auth_token),
            }
            try:
                self.session.put(
                    "https://api.spotify.com/v1/me/following?type=user&ids=" + self.profile,
                    headers = headers
                )
                return "success"
            except:
                return "error"
        elif self.type == 1:
            if "/playlist/" in self.profile:
                self.profile = self.profile.split("/playlist/")[1]
            if "?" in self.profile:
                self.profile = self.profile.split("?")[0]
            login_token, username, image_url = self.register_account()
            if login_token == None:
                return "error"
            elif login_token == False:
                return "error"
            elif login_token == "Proxy":
                return "proxy_detected"
            elif login_token == "error":
                return "error"
                
            auth_token = self.get_token(login_token)
            if auth_token == None:
                return "error"

            if self.photo == True:
                img = self.change_picture(auth_token, username, image_url)
                if img == "error":
                    return "error"

            headers = {
                "accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "accept-language": "en",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                "app-platform": "WebPlayer",
                "Referer": "https://open.spotify.com/",
                "spotify-app-version": "1.1.52.204.ge43bc405",
                "authorization": "Bearer {}".format(auth_token),
            }
            try:
                self.session.put(
                    f"https://api.spotify.com/v1/playlists/{self.profile}/followers",
                    headers = headers
                )
                return "success"
            except:
                return "error"
        elif self.type == 2:
            if "/artist/" in self.profile:
                self.profile = self.profile.split("/artist/")[1]
            if "?" in self.profile:
                self.profile = self.profile.split("?")[0]
            login_token, username, image_url = self.register_account()
            if login_token == None:
                return "error"
            elif login_token == False:
                return "error"
            elif login_token == "Proxy":
                return "proxy_detected"
            elif login_token == "error":
                return "error"
                
            auth_token = self.get_token(login_token)
            if auth_token == None:
                return "error"

            if self.photo == True:
                img = self.change_picture(auth_token, username, image_url)
                if img == "error":
                    return "error"

            headers = {
                "accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br",
                "accept-language": "en",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
                "app-platform": "WebPlayer",
                "Referer": "https://open.spotify.com/",
                "spotify-app-version": "1.1.52.204.ge43bc405",
                "authorization": "Bearer {}".format(auth_token),
            }
            try:
                self.session.put(
                    "https://api.spotify.com/v1/me/following?type=artist&ids=" + self.profile,
                    headers = headers
                )
                return "success"
            except:
                return "error"
