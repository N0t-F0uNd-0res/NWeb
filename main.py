from colorama import Fore,Style
import os
import sys
import requests
from pystyle import Colors, Colorate
import socket
import time
import bs4
import webbrowser
import requests
import bs4
import time
import re

def phonenumber():
    target = input(Colorate.Diagonal(Colors.red_to_white,"Запрс: "))

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Информация о номере: {target}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #1a1a1a;
                color: #ffffff;
                margin: 20px;
                line-height: 1.6;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #2a2a2a;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
            }}
            h1 {{
                color: #ff4d4d;
                text-align: center;
                border-bottom: 2px solid #ff4d4d;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #ff9999;
                margin-top: 30px;
                border-left: 5px solid #ff4d4d;
                padding-left: 10px;
            }}
            .section {{
                margin-bottom: 20px;
                padding: 15px;
                background-color: #333333;
                border-radius: 5px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                background-color: #444444;
                margin: 5px 0;
                padding: 10px;
                border-radius: 5px;
            }}
            a {{
                color: #ffcccc;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .error {{
                color: #ff6666;
                font-weight: bold;
            }}
            .not-found {{
                color: #cccccc;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Информация о номере: {target}</h1>
    """

    html_content += "<h2>Информация с HTMLWeb</h2><div class='section'>"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    res = requests.get(f"https://htmlweb.ru/geo/api.php?json&telcod={target}", headers=headers).json()
    
    stack = [(res, 0)]
    while stack:
        current_dict, indent = stack.pop()
        keys = list(current_dict.keys())
        for key in reversed(keys):
            value = current_dict[key]
            if isinstance(value, dict):
                html_content += f"<p style='margin-left: {indent * 20}px; font-weight: bold;'>{key}:</p>"
                print(Colorate.Diagonal(Colors.red_to_white, '  ' * indent + f"{key}:"))
                stack.append((value, indent + 1))

            else:
                html_content += f"<p style='margin-left: {indent * 20}px;'>[{key}] - [{value}]</p>"
                print(Colorate.Diagonal(Colors.red_to_white, '  ' * indent + f"[{key}] - [{value}]"))
    html_content += "</div>"

    time.sleep(1)
    print("\n===========================================================\n")

    html_content += "<h2>Информация с ProxyNova</h2><div class='section'>"
    res = requests.get(f"https://api.proxynova.com/comb?query={target}&start=0&limit=15").json()
    lines = res.get('lines', [])
    count = res.get('count', 0)

    html_content += f"<p><strong>Найдено записей:</strong> {count}</p>"
    print(Colorate.Diagonal(Colors.red_to_white, f"Найдено записей: {count}"))

    for item in lines:
        html_content += f"<p>{item}</p>"
        print(Colorate.Diagonal(Colors.red_to_white, item))
    
    html_content += "</div>"
    print("\n===========================================================\n")    

    print(Colorate.Diagonal(Colors.red_to_white, "\ncheck leaks. . ."))
    time.sleep(1)
    res = requests.get(f"https://leakcheck.io/api/public?&check={target}").json()
    try:
        if res.get('success'):
            sources = [s for s in res.get('sources', []) if s.get('date')]
            print(Colorate.Diagonal(Colors.red_to_white, "Sources:"))

            fields = res.get('fields', [])
            print(Colorate.Diagonal(Colors.red_to_white, f"Fields: {fields}"))
            for source in sources:
                print(Colorate.Diagonal(Colors.red_to_white, f"[{source['name']}] - [{source['date']}]"))
        else:
            print(Colorate.Diagonal(Colors.red_to_white, "Error:", res.get('error', 'Unknown error')))
    except:
        print(Colorate.Diagonal(Colors.red_to_white, "Not Found"))
    print("\n===========================================================\n")
    html_content += "<h2>Информация с Leak Check</h2><div class='section'>"
    res = requests.get(f"https://leakcheck.io/api/public?&check={target}").json()
    try:
        if res.get('success'):
            sources = [s for s in res.get('sources', []) if s.get('date')]
            html_content += "<p><strong>Sources:</strong></p><ul>"
            for source in sources:
                html_content += f"<li>[{source['name']}] - [{source['date']}]</li>"
            html_content += "</ul>"
            fields = res.get('fields', [])
            html_content += f"<p><strong>Fields:</strong> {fields}</p>"
        else:
            html_content += f"<p class='error'>Error: {res.get('error', 'Unknown error')}</p>"
    except:
        html_content += "<p class='not-found'>Not Found</p>"
    html_content += "</div>"

    time.sleep(0.5)
    print(Colorate.Diagonal(Colors.red_to_white, "\ninfo phoneradar"))
    url = f"https://phoneradar.ru/phone/?number={target}"

    res = requests.get(url)

    html_cont = res.text
    soup = bs4.BeautifulSoup(html_cont,'html.parser')

    phone = soup.find("div",class_="card-body")

    inf = phone.find("p")
    if phone:
        p_tags = phone.find_all("p") 
        for p in p_tags[:2]:         
            print(Colorate.Diagonal(Colors.red_to_white, p.text.strip()))

    print(Colorate.Diagonal(Colors.red_to_white, "Oтзывы: "))
    p_tags = soup.select(".card.mb-2  .card-body p")
    for p in p_tags:
        print(Colorate.Diagonal(Colors.red_to_white, p.text.strip()))

    time.sleep(0.5)

    html_content += "<h2>ИнформацияPhoneRadar</h2><div class='section'>"
    url = f"https://phoneradar.ru/phone/?number={target}"
    res = requests.get(url)
    html_cont = res.text
    soup = bs4.BeautifulSoup(html_cont, 'html.parser')
    phone = soup.find("div", class_="card-body")
    if phone:
        p_tags = phone.find_all("p")
        for p in p_tags[:2]:
            html_content += f"<p>{p.text.strip()}</p>"
    html_content += "<p><strong>Reviews:</strong></p><ul>"
    p_tags = soup.select(".card.mb-2 .card-body p")
    for p in p_tags:
        html_content += f"<li>{p.text.strip()}</li>"
    html_content += "</ul></div>"
    time.sleep(0.5)
    print("\n===========================================================\n")
    print(Colorate.Diagonal(Colors.red_to_white, f"""\nSearch Engines:
[intelx] - [https://intelx.io/?s={target}]
[searx.tiekoetter] - [https://searx.tiekoetter.com/search?q={target}]
[aleph] - [https://aleph.occrp.org/search?q={target}]
[google] - [https://www.google.com/search?q={target}]
[yandex] - [https://yandex.ru/yandsearch?text={target}]\n"""))
    time.sleep(0.5)
    print("\n===========================================================\n")
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://www.instagram.com/accounts/password/reset] - [Поиск аккаунта в Instagram]'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://api.whatsapp.com/send?phone={target}] - [Поиск номера в WhatsApp]'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://facebook.com/login/identify/?ctx=recover&ars=royal_blue_bar] - [Поиск аккаунта FaceBook]'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://www.linkedin.com/checkpoint/rp/request-password-reset?] - [Поиск аккаунта Linkedin]'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://ok.ru/dk?st.cmd=anonymRecoveryStartPhoneLink] - [Поиск аккаунта OK]'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://twitter.com/account/begin_password_reset] - [Поиск аккаунта Twitter]'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://viber://add?number={target}] - Поиск номера в Viber]'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://skype:{target}?call] - [Звонок на номер с Skype]'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://t.me/{target}] - [Открыть аккаунт в Телеграмме]'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[https://www.sberbank.ru/ru/person/cybersecurity/antifraud] - проверка по базе мошенников'))
    print(Colorate.Diagonal(Colors.red_to_white, f'[tel:{target}] - [Звонок на номер с телефона]'))
    
    print("\n===========================================================\n")
    time.sleep(0.5)
    print(Colorate.Diagonal(Colors.red_to_white, "\ngoogle dorks"))
    print(Colorate.Diagonal(Colors.red_to_white, f'https://www.google.com/search?q=intext:"{target}"'))
    print(Colorate.Diagonal(Colors.red_to_white, f'https://www.google.com/search?q=intext:"{target}" filetype:txt'))
    print(Colorate.Diagonal(Colors.red_to_white, f'https://www.google.com/search?q=intext:"{target}" filetype:pdf'))
    print(Colorate.Diagonal(Colors.red_to_white, f'https://www.google.com/search?q=intext:"{target}" filetype:csv'))
    print(Colorate.Diagonal(Colors.red_to_white, "https://dorksearch.com/"))

    time.sleep(0.5)
    html_content += "<h2>Поисковые системы</h2><div class='section'><ul>"
    html_content += f"<li><a href='https://intelx.io/?s={target}' target='_blank'>[intelx] - [IntelX Search]</a></li>"
    html_content += f"<li><a href='https://searx.tiekoetter.com/search?q={target}' target='_blank'>[searx.tiekoetter] - [SearX Search]</a></li>"
    html_content += f"<li><a href='https://aleph.occrp.org/search?q={target}' target='_blank'>[aleph] - [Aleph Search]</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q={target}' target='_blank'>[google] - [Google Search]</a></li>"
    html_content += f"<li><a href='https://yandex.ru/yandsearch?text={target}' target='_blank'>[yandex] - [Yandex Search]</a></li>"
    html_content += "</ul></div>"

    time.sleep(0.5)
    html_content += "<h2>Дополнительные ссылки</h2><div class='section'><ul>"
    html_content += f"<li><a href='https://www.instagram.com/accounts/password/reset' target='_blank'>[Instagram] - [Поиск аккаунта в Instagram]</a></li>"
    html_content += f"<li><a href='https://api.whatsapp.com/send?phone={target}' target='_blank'>[WhatsApp] - [Поиск номера в WhatsApp]</a></li>"
    html_content += f"<li><a href='https://facebook.com/login/identify/?ctx=recover&ars=royal_blue_bar' target='_blank'>[Facebook] - [Поиск аккаунта FaceBook]</a></li>"
    html_content += f"<li><a href='https://www.linkedin.com/checkpoint/rp/request-password-reset?' target='_blank'>[LinkedIn] - [Поиск аккаунта Linkedin]</a></li>"
    html_content += f"<li><a href='https://ok.ru/dk?st.cmd=anonymRecoveryStartPhoneLink' target='_blank'>[OK] - [Поиск аккаунта OK]</a></li>"
    html_content += f"<li><a href='https://twitter.com/account/begin_password_reset' target='_blank'>[Twitter] - [Поиск аккаунта Twitter]</a></li>"
    html_content += f"<li><a href='https://viber://add?number={target}' target='_blank'>[Viber] - [Поиск номера в Viber]</a></li>"
    html_content += f"<li><a href='https://skype:{target}?call' target='_blank'>[Skype] - [Звонок на номер с Skype]</a></li>"
    html_content += f"<li><a href='https://t.me/{target}' target='_blank'>[Telegram] - [Открыть аккаунт в Телеграмме]</a></li>"
    html_content += f"<li><a href='https://www.sberbank.ru/ru/person/cybersecurity/antifraud' target='_blank'>[Sberbank] - [Gроверка по базе мошенников]</a></li>"
    html_content += f"<li><a href='tel:{target}' target='_blank'>[Phone] - [Звонок на номер с телефона]</a></li>"
    html_content += "</ul></div>"

    time.sleep(0.5)
    html_content += "<h2>Google Dorks</h2><div class='section'><ul>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\"' target='_blank'>intext:\"{target}\"</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\" filetype:txt' target='_blank'>intext:\"{target}\" filetype:txt</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\" filetype:pdf' target='_blank'>intext:\"{target}\" filetype:pdf</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\" filetype:csv' target='_blank'>intext:\"{target}\" filetype:csv</a></li>"
    
    html_content += "</ul></div>"

    html_content += """
        </div>
    </body>
    </html>
    """

    with open(f"{target}.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(Colorate.Diagonal(Colors.red_to_white, f"Запрос сохранен в {target}.html\nоткрыть в браузере?(y/n)"))
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    yon = input("")
    if yon == "y":
        webbrowser.open(f"{script_dir}/{target}.html")
    if yon == "n":
        main()
    else:
        time.sleep(1)
        main()

def IP():
    target = input(Colorate.Diagonal(Colors.red_to_white,"Запрос: "))

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Информация о IP: {target}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #1a1a1a;
                color: #ffffff;
                margin: 20px;
                line-height: 1.6;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #2a2a2a;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
            }}
            h1 {{
                color: #ff4d4d;
                text-align: center;
                border-bottom: 2px solid #ff4d4d;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #ff9999;
                margin-top: 30px;
                border-left: 5px solid #ff4d4d;
                padding-left: 10px;
            }}
            .section {{
                margin-bottom: 20px;
                padding: 15px;
                background-color: #333333;
                border-radius: 5px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                background-color: #444444;
                margin: 5px 0;
                padding: 10px;
                border-radius: 5px;
            }}
            a {{
                color: #ffcccc;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .error {{
                color: #ff6666;
                font-weight: bold;
            }}
            .not-found {{
                color: #cccccc;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Информация о IP: {target}</h1>
    """

    html_content += "<h2>Информация с HTMLWeb</h2><div class='section'>"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }

    res = requests.get(f"https://htmlweb.ru/geo/api.php?json&ip={target}", headers=headers).json()
    stack = [(res, 0)]
    while stack:
        current_dict, indent = stack.pop()
        keys = list(current_dict.keys())
        for key in reversed(keys):
            value = current_dict[key]
            if isinstance(value, dict):
                html_content += f"<p style='margin-left: {indent * 20}px; font-weight: bold;'>{key}:</p>"
                print(Colorate.Diagonal(Colors.red_to_white, '  ' * indent + f"{key}:"))
                stack.append((value, indent + 1))

            else:
                html_content += f"<p style='margin-left: {indent * 20}px;'>[{key}] - [{value}]</p>"
                print(Colorate.Diagonal(Colors.red_to_white, '  ' * indent + f"[{key}] - [{value}]"))
    html_content += "</div>"

    print("\n===========================================================\n")

    html_content += "<h2>Информация с ProxyNova</h2><div class='section'>"
    res = requests.get(f"https://api.proxynova.com/comb?query={target}&start=0&limit=15").json()
    lines = res.get('lines', [])
    count = res.get('count', 0)

    html_content += f"<p><strong>Найдено записей:</strong> {count}</p>"
    print(Colorate.Diagonal(Colors.red_to_white, f"Найдено записей: {count}"))

    for item in lines:
        html_content += f"<p>{item}</p>"
        print(Colorate.Diagonal(Colors.red_to_white, item))
    html_content += "</div>"

    print("\n===========================================================\n")

    print("leakcheck info")
    res = requests.get(f"https://leakcheck.io/api/public?&check={target}", headers=headers).json()
    try:
        if res.get('success'):
            sources = [s for s in res.get('sources', []) if s.get('date')]
            print(Colorate.Diagonal(Colors.red_to_white, "Sources:"))

            fields = res.get('fields', [])
            print(Colorate.Diagonal(Colors.red_to_white, f"Fields: {fields}"))
            for source in sources:
                print(Colorate.Diagonal(Colors.red_to_white, f"[{source['name']}] - [{source['date']}]"))
        else:
            print(Colorate.Diagonal(Colors.red_to_white, "Error:", res.get('error', 'Unknown error')))
    except:
        print(Colorate.Diagonal(Colors.red_to_white, "Not Found"))
    print("\n===========================================================\n")
    html_content += "<h2>Информация с Leak Check</h2><div class='section'>"
    res = requests.get(f"https://leakcheck.io/api/public?&check={target}").json()
    try:
        if res.get('success'):
            sources = [s for s in res.get('sources', []) if s.get('date')]
            html_content += "<p><strong>Sources:</strong></p><ul>"
            for source in sources:
                html_content += f"<li>[{source['name']}] - [{source['date']}]</li>"
            html_content += "</ul>"
            fields = res.get('fields', [])
            html_content += f"<p><strong>Fields:</strong> {fields}</p>"
        else:
            html_content += f"<p class='error'>Error: {res.get('error', 'Unknown error')}</p>"
    except:
        html_content += "<p class='not-found'>Not Found</p>"
    html_content += "</div>"
    time.sleep(1)

    ports = {
        20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet",
        25: "SMTP", 43: "WHOIS", 53: "DNS", 80: "HTTP",
        115: "SFTP", 123: "NTP", 143: "IMAP", 161: "SNMP",
        179: "BGP", 443: "HTTPS", 445: "MICROSOFT-DS",
        514: "SYSLOG", 515: "PRINTER", 993: "IMAPS",
        995: "POP3S", 1080: "SOCKS", 1194: "OpenVPN",
        1433: "SQL Server", 1723: "PPTP", 3128: "HTTP",
        3268: "LDAP", 3306: "MySQL", 3389: "RDP",
        5432: "PostgreSQL", 5900: "VNC", 8080: "Tomcat", 10000: "Webmin"
    }
    html_content += "<h2>Port Scan Results</h2><div class='section'><ul>"
    print(Colorate.Diagonal(Colors.red_to_white, "\nscanning ports..."))
    for port, service in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.7)
        try:
            result = sock.connect_ex((target, port))
            status = "open" if result == 0 else "closed"
            html_content += f"<li>port {port:5} [{service:15}]: {status}</li>"
            print(Colorate.Diagonal(Colors.red_to_white, f"port {port:5} [{service:15}]: {status}"))
        except Exception as e:
            html_content += f"<li class='error'>error {port}: {e}</li>"
            print(Colorate.Diagonal(Colors.red_to_white, f"error {port}: {e}"))
        finally:
            sock.close()

    print(Colorate.Diagonal(Colors.red_to_white,f"""===========================================================
                            
[https://www.virustotal.com/gui/ip-address/{target}] - [VirusTotal]
[https://intelx.io/?s={target}] - [IntelX Search]
[https://searx.tiekoetter.com/search?q={target}] - [searx.tiekoetter]
[https://aleph.occrp.org/search?q={target}] - [Aleph Search]
[https://www.google.com/search?q={target}] - [Google Search]
[https://yandex.ru/yandsearch?text={target}] - [Yandex Search]"""))
    
    print(Colorate.Diagonal(Colors.red_to_white,f"""===========================================================
                            
Дополнительные ссылки
[https://www.shodan.io/host/{target}] - [shodan]
[https://www.whois.com/whois/{target}] - [whois]
[https://www.iplocation.net/ip-lookup/{target}] - [iplocation]
[https://www.abuseipdb.com/check/{target}] - [abuseipdb]
[https://www.ipinfo.io/{target}] - [ipinfo]"""))
    
    print(Colorate.Diagonal(Colors.red_to_white,f"""===========================================================
                            
Google Dorks
https://www.google.com/search?q=intext:"{target}                            
https://www.google.com/search?q=intext:"{target}" filetype:txt'
https://www.google.com/search?q=intext:"{target}" filetype:pdf'
https://www.google.com/search?q=intext:"{target}" filetype:csv'
https://dorksearch.com/"""))
    html_content += "</ul></div>"

    html_content += "<h2>Поисковые системы</h2><div class='section'><ul>"
    html_content += f"<li><a href='https://www.virustotal.com/gui/ip-address/{target}' target='_blank'>[VirusTotal] - [VirusTotal IP Report]</a></li>"
    html_content += f"<li><a href='https://intelx.io/?s={target}' target='_blank'>[intelx] - [IntelX Search]</a></li>"
    html_content += f"<li><a href='https://searx.tiekoetter.com/search?q={target}' target='_blank'>[searx.tiekoetter] - [SearX Search]</a></li>"
    html_content += f"<li><a href='https://aleph.occrp.org/search?q={target}' target='_blank'>[aleph] - [Aleph Search]</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q={target}' target='_blank'>[google] - [Google Search]</a></li>"
    html_content += f"<li><a href='https://yandex.ru/yandsearch?text={target}' target='_blank'>[yandex] - [Yandex Search]</a></li>"
    html_content += "</ul></div>"

    html_content += "<h2>Дополнительные ссылки</h2><div class='section'><ul>"
    html_content += f"<li><a href='https://www.shodan.io/host/{target}' target='_blank'>[Shodan] - [Shodan IP Search]</a></li>"
    html_content += f"<li><a href='https://www.whois.com/whois/{target}' target='_blank'>[WHOIS] - [WHOIS Lookup]</a></li>"
    html_content += f"<li><a href='https://www.iplocation.net/ip-lookup/{target}' target='_blank'>[IP Location] - [IP Location Lookup]</a></li>"
    html_content += f"<li><a href='https://www.abuseipdb.com/check/{target}' target='_blank'>[AbuseIPDB] - [AbuseIPDB Check]</a></li>"
    html_content += f"<li><a href='https://www.ipinfo.io/{target}' target='_blank'>[IPInfo] - [IP Information]</a></li>"
    html_content += "</ul></div>"

    html_content += "<h2>Google Dorks</h2><div class='section'><ul>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\"' target='_blank'>intext:\"{target}\"</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\" filetype:txt' target='_blank'>intext:\"{target}\" filetype:txt</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\" filetype:pdf' target='_blank'>intext:\"{target}\" filetype:pdf</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\" filetype:csv' target='_blank'>intext:\"{target}\" filetype:csv</a></li>"
    
    html_content += "</ul></div>"

    html_content += "</div></body></html>"

    filename = f"{target}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(Colorate.Diagonal(Colors.red_to_white, f"Запрос сохранен в {filename}.html\nоткрыть в браузере?(y/n)"))
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    yon = input("")
    if yon == "y":
        webbrowser.open(f"{script_dir}/{target}.html")
    if yon == "n":
        main()
    else:
        time.sleep(1)
        main()


def mail():
    target = input(Colorate.Diagonal(Colors.red_to_white,"Запрс: "))

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Информация о почте: {target}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #1a1a1a;
                color: #ffffff;
                margin: 20px;
                line-height: 1.6;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #2a2a2a;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(255, 0, 0, 0.5);
            }}
            h1 {{
                color: #ff4d4d;
                text-align: center;
                border-bottom: 2px solid #ff4d4d;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #ff9999;
                margin-top: 30px;
                border-left: 5px solid #ff4d4d;
                padding-left: 10px;
            }}
            .section {{
                margin-bottom: 20px;
                padding: 15px;
                background-color: #333333;
                border-radius: 5px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                background-color: #444444;
                margin: 5px 0;
                padding: 10px;
                border-radius: 5px;
            }}
            a {{
                color: #ffcccc;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .error {{
                color: #ff6666;
                font-weight: bold;
            }}
            .not-found {{
                color: #cccccc;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Информация о Почте: {target}</h1>
    """

    html_content += "<h2>Информация с ipqualityscore.com</h2><div class='section'>"
    res = requests.get(f"https://ipqualityscore.com/api/json/email/lPnx5AhAUv4jgIFDXquYpe8CVBjmaTii/{target}").json()
    
    stack = [(res, 0)]
    while stack:
        current_dict, indent = stack.pop()
        keys = list(current_dict.keys())
        for key in reversed(keys):
            value = current_dict[key]
            if isinstance(value, dict):
                html_content += f"<p> style='margin-left: {indent * 20}px; font-weight: bold;'>{key}:</p>"
                print(Colorate.Diagonal(Colors.red_to_white, '  ' * indent + f"{key}:"))
                stack.append((value, indent + 1))
            else:
                html_content += f"<p style='margin-left: {indent * 20}px;'>[{key}] - [{value}]</p>"
                print(Colorate.Diagonal(Colors.red_to_white, '  ' * indent + f"[{key}] - [{value}]"))
    html_content += "</div>"

    time.sleep(1)
    print("\n===========================================================\n")

    html_content += "<h2>Информация с ProxyNova</h2><div class='section'>"
    res = requests.get(f"https://api.proxynova.com/comb?query={target}&start=0&limit=15").json()
    lines = res.get('lines', [])
    count = res.get('count', 0)

    html_content += f"<p><strong>Найдено записей:</strong> {count}</p>"
    print(Colorate.Diagonal(Colors.red_to_white, f"Найдено записей: {count}"))

    for item in lines:
        html_content += f"<p>{item}</p>"
        print(Colorate.Diagonal(Colors.red_to_white, item))
    
    html_content += "</div>"
    print("\n===========================================================\n")    

    print(Colorate.Diagonal(Colors.red_to_white, "\ncheck leaks. . ."))
    time.sleep(1)
    res = requests.get(f"https://leakcheck.io/api/public?&check={target}").json()
    try:
        if res.get('success'):
            sources = [s for s in res.get('sources', []) if s.get('date')]
            print(Colorate.Diagonal(Colors.red_to_white, "Sources:"))

            fields = res.get('fields', [])
            print(Colorate.Diagonal(Colors.red_to_white, f"Fields: {fields}"))
            for source in sources:
                print(Colorate.Diagonal(Colors.red_to_white, f"[{source['name']}] - [{source['date']}]"))
        else:
            print(Colorate.Diagonal(Colors.red_to_white, "Error:", res.get('error', 'Unknown error')))
    except:
        print(Colorate.Diagonal(Colors.red_to_white, "Not Found"))

    print("\n===========================================================\n")

    html_content += "<h2>Информация с Leak Check</h2><div class='section'>"
    res = requests.get(f"https://leakcheck.io/api/public?&check={target}").json()
    try:
        if res.get('success'):
            sources = [s for s in res.get('sources', []) if s.get('date')]
            html_content += "<p><strong>Sources:</strong></p><ul>"
            for source in sources:
                html_content += f"<li>[{source['name']}] - [{source['date']}]</li>"
            html_content += "</ul>"
            fields = res.get('fields', [])
            html_content += f"<p><strong>Fields:</strong> {fields}</p>"
        else:
            html_content += f"<p class='error'>Error: {res.get('error', 'Unknown error')}</p>"
    except:
        html_content += "<p class='not-found'>Not Found</p>"
    html_content += "</div>"
    time.sleep(0.5)
    print("\n===========================================================\n")
    print(Colorate.Diagonal(Colors.red_to_white, f"""\nSearch Engines:
[intelx] - [https://intelx.io/?s={target}]
[searx.tiekoetter] - [https://searx.tiekoetter.com/search?q={target}]
[aleph] - [https://aleph.occrp.org/search?q={target}]
[google] - [https://www.google.com/search?q={target}]
[yandex] - [https://yandex.ru/yandsearch?text={target}]\n"""))
    print("\n===========================================================\n")

    time.sleep(0.5)
    print(Colorate.Diagonal(Colors.red_to_white, "\ngoogle dorks"))
    print(Colorate.Diagonal(Colors.red_to_white, f'https://www.google.com/search?q=intext:"{target}"'))
    print(Colorate.Diagonal(Colors.red_to_white, f'https://www.google.com/search?q=intext:"{target}" filetype:txt'))
    print(Colorate.Diagonal(Colors.red_to_white, f'https://www.google.com/search?q=intext:"{target}" filetype:pdf'))
    print(Colorate.Diagonal(Colors.red_to_white, f'https://www.google.com/search?q=intext:"{target}" filetype:csv'))
    print(Colorate.Diagonal(Colors.red_to_white, "https://dorksearch.com/"))
    
    time.sleep(0.5)
    html_content += "<h2>Поисковые системы</h2><div class='section'><ul>"
    html_content += f"<li><a href='https://intelx.io/?s={target}' target='_blank'>[intelx] - [IntelX Search]</a></li>"
    html_content += f"<li><a href='https://searx.tiekoetter.com/search?q={target}' target='_blank'>[searx.tiekoetter] - [SearX Search]</a></li>"
    html_content += f"<li><a href='https://aleph.occrp.org/search?q={target}' target='_blank'>[aleph] - [Aleph Search]</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q={target}' target='_blank'>[google] - [Google Search]</a></li>"
    html_content += f"<li><a href='https://yandex.ru/yandsearch?text={target}' target='_blank'>[yandex] - [Yandex Search]</a></li>"
    html_content += "</ul></div>"

    time.sleep(0.5)
    html_content += "<h2>Google Dorks</h2><div class='section'><ul>"

    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\"' target='_blank'>intext:\"{target}\"</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\" filetype:txt' target='_blank'>intext:\"{target}\" filetype:txt</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\" filetype:pdf' target='_blank'>intext:\"{target}\" filetype:pdf</a></li>"
    html_content += f"<li><a href='https://www.google.com/search?q=intext:\"{target}\" filetype:csv' target='_blank'>intext:\"{target}\" filetype:csv</a></li>"
    
    html_content += "</ul></div>"

    html_content += """
        </div>
    </body>
    </html>
    """

    with open(f"{target}.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(Colorate.Diagonal(Colors.red_to_white, f"Запрос сохранен в {target}.html\nоткрыть в браузере?(y/n)"))
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    yon = input("")
    if yon == "y":
        webbrowser.open(f"{script_dir}/{target}.html")
    if yon == "n":
        main()
    else:
        time.sleep(1)
        main()
def source():
    os.system("cls||clear")
    print(Colorate.Diagonal(Colors.red_to_white, """
                            
                                             ╔════════════════════════════╗
                                        ╠════╣         ИСТОЧНИКИ          ╠═══╣
                                        ║    ╚════════════════════════════╝   ║
                                        ║                                     ║
  ╔═════════════════════════════════════╬═════════════════════════════════════╬═════════════════════════════════════╗                        
  ║       По номеру телефона            ║                 ПО IP               ║              ПО ПОЧТЕ               ║
  ╠═════════════════════════════════════╬═════════════════════════════════════╬═════════════════════════════════════╣ 
  ║[1] - https://htmlweb.ru/            ║ [1] - https://htmlweb.ru/           ║ [1] - https://ipqualityscore.com    ║
  ║[2] - https://leakcheck.io/          ║ [2] - https://leakcheck.io/         ║ [2] - https://api.proxynova.com/    ║
  ║[3] - https://phoneradar.ru/         ║ [3] - Port scan                     ║ [3] - https://leakcheck.io/         ║
  ║[4] - https://intelx.io/             ║ [4] - https://www.virustotal.com/   ║ [4] - https://intelx.io/            ║
  ║[5] - https://searx.tiekoetter.com/  ║ [5] - https://intelx.io/            ║ [5] - https://searx.tiekoetter.com/ ║
  ║[6] - https://aleph.occrp.org/       ║ [6] - https://searx.tiekoetter.com/ ║ [6] - https://aleph.occrp.org/      ║
  ║[7] - https://www.google.com/        ║ [7] - https://aleph.occrp.org/      ║ [7] - https://www.google.com/       ║
  ║[8] - https://yandex.ru/             ║ [8] - https://www.google.com/       ║ [8] - https://yandex.ru/            ║
  ║[9] - https://www.instagram.com/     ║ [9] - https://yandex.ru/            ║ [9] - google dorks                  ║
  ║[10] - https://api.whatsapp.com/     ║ [10] - https://www.shodan.io/       ║                                     ║ 
  ║[11] - https://facebook.com/         ║ [11] - https://www.whois.com/       ║                                     ║
  ║[12] - https://www.linkedin.com/     ║ [12] - https://www.iplocation.net/  ║                                     ║
  ║[13] - https://ok.ru/                ║ [13] - https://www.abuseipdb.com/   ║                                     ║
  ║[14] - https://www.sberbank.ru       ║ [14] - https://www.ipinfo.io/       ║                                     ║
  ║[15] - https://twitter.com/          ║ [15] - https://api.proxynova.com/   ║                                     ║   
  ║[16] - https://viber://add?number=   ║ [16] - google dorks                 ║                                     ║
  ║[17] - https://skype:                ║                                     ║                                     ║
  ║[18] - https://t.me/                 ║                                     ║                                     ║
  ║[19] - https://api.proxynova.com/    ║                                     ║                                     ║
  ║[20] - google dorks                  ║                                     ║                                     ║
  ╚═════════════════════════════════════╩═════════════════════════════════════╩═════════════════════════════════════╝
          
          """))

def main():
    os.system("cls||clear")
    print(Colorate.Diagonal(Colors.red_to_white, """   
             ▄▄   ▄                               ▄      ▀                             █      
             █▀▄  █  ▄▄▄    ▄▄▄    ▄ ▄▄   ▄▄▄   ▄▄█▄▄  ▄▄▄     ▄▄▄      ▄     ▄  ▄▄▄   █▄▄▄  
             █ █▄ █ █▀  █  █▀  ▀   █▀  ▀ █▀ ▀█    █      █    █▀  ▀     ▀▄ ▄ ▄▀ █▀  █  █▀ ▀█ 
             █  █ █ █▀▀▀▀  █       █     █   █    █      █    █          █▄█▄█  █▀▀▀▀  █   █ 
             █   ██ ▀█▄▄▀  ▀█▄▄▀   █     ▀█▄█▀    ▀▄▄  ▄▄█▄▄  ▀█▄▄▀       █ █   ▀█▄▄▀  ██▄█▀ 
                    ║                                                           ║
                    ║           [github]:[https://github.com/N0t-F0uNd-0res]    ║
                    ║           [source]:[Посмотреть все источники] - 26        ║         
                    ║           [00]:[ВЫХОД]                                    ║
                    ║               ╔═══════════════════════╗                   ║
                    ║               ║ [1] - Номер телефона  ║                   ║
                    ╚═══════════════╣ [2] - IP              ╠═══════════════════╝
                                    ║ [3] - Почта           ║    
                                    ╚═══════════════════════╝        
"""))
    try:
        choice = input(Colorate.Diagonal(Colors.red_to_white, "> > > "))
        if choice == "1":
            phonenumber()
            try:
                input(Colorate.Diagonal(Colors.red_to_white, "Enter. . ."))
                main()
            except KeyboardInterrupt:
                sys.exit()
            except:
                main()
        elif choice == "2":
            IP()
            try:
                input(Colorate.Diagonal(Colors.red_to_white, "Enter. . ."))
                main()
            except KeyboardInterrupt:
                sys.exit()
            except:
                main()
        elif choice == "3":
            mail()
            try:
                input(Colorate.Diagonal(Colors.red_to_white, "Enter. . ."))
                main()
            except KeyboardInterrupt:
                sys.exit()
            except:
                main()
        elif choice == "00":
            sys.exit()
        elif choice == "source":
            source()
            try:
                input(Colorate.Diagonal(Colors.red_to_white, "Enter. . ."))
                main()
            except KeyboardInterrupt:
                sys.exit()
            except:
                main()
        else:
            print(Colorate.Diagonal(Colors.red_to_white, "Неправильный ввод"))
            time.sleep(1)
            main()
    except KeyboardInterrupt:
        sys.exit()
    except:
        main()
main()