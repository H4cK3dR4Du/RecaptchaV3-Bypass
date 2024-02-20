from urllib.parse import urlparse, parse_qs
import re, os, json, time, requests

class RecaptchaV3:
    def __init__(self) -> None:
        self.anchor_url = "" # Test: https://www.google.com/recaptcha/enterprise/anchor?ar=1&k=6LeMrv8ZAAAAAIcvo5HKvdj1lxtUdHnS13jUCulQ&co=aHR0cHM6Ly9wbGF5Lmhib21heC5jb206NDQz&hl=en&v=MuIyr8Ej74CrXhJDQy37RPBe&size=invisible&cb=f9q60qxahq1b
        self.reload_url = "" # Test: https://www.google.com/recaptcha/enterprise/reload?k=6LeMrv8ZAAAAAIcvo5HKvdj1lxtUdHnS13jUCulQ
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0"
        }

    def recaptchav3_bypass(self) -> str:
        url_var = parse_qs(urlparse(self.anchor_url).query)

        r = requests.get(self.anchor_url, headers=self.headers)
        anchor_token = re.search(r'type="hidden" id="recaptcha-token" value="([^"]+)"', r.text).group(1)

        value1 = url_var['v'][0]
        value2 = url_var['k'][0]
        value3 = url_var['co'][0]

        data = f"v={value1}&reason=q&c={anchor_token}&k={value2}&co={value3}&hl=en&size=invisible"

        self.headers.update({
            "Referer": r.url,
            "Content-Type": "application/x-www-form-urlencoded"
        })

        r = requests.post(self.reload_url, headers=self.headers, data=data)
        return r.text.split('["rresp","')[1].split('"')[0]

if __name__ == "__main__":
    i = RecaptchaV3()
    print("Bypassed RecaptchaV3:", i.recaptchav3_bypass())