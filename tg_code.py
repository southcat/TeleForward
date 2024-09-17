# Copyright (c) Shrimadhav U K
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# https://t.me/ThankTelegram/802953
# Ported to a Simple script by: https://github.com/pokurt

import requests
from bs4 import BeautifulSoup
from pyrogram import Client


def req_tgcode(input_phone_number):
    resp = requests.post(
        "https://my.telegram.org/auth/send_password",
        data={
            "phone": input_phone_number
        }
    )
    return resp.json()["random_hash"]


def extract_code(message):
    telegram__web_login_code = None
    incoming_message_text_in_lower_case = message.lower()
    if "web login code" in incoming_message_text_in_lower_case:
        parted_message_pts = message.split("\n")
        if len(parted_message_pts) >= 2:
            web_login_code = parted_message_pts[1]
    else:
        web_login_code = message
    return web_login_code


def final_txt(r):
    parse_txt = "App Configuration:\n"
    parse_txt += "APP ID: {}\n".format(r["App Configuration"]["app_id"])
    parse_txt += "API HASH: {}\n\n".format(r["App Configuration"]["api_hash"])
    parse_txt += "Available MTProto Servers: \n"
    parse_txt += "Production Configuration: "
    parse_txt += "{}\n".format(
        r["Available MTProto Servers"]["production_configuration"]
    )
    parse_txt += "Test Configuration: "
    parse_txt += "{}\n\n".format(
        r["Available MTProto Servers"]["test_configuration"]
    )
    parse_txt += "Disclaimer: "
    parse_txt += "{}".format(
        r["Disclaimer"]
    )
    return parse_txt


def login_cookie(input_phone_number, tg_random_hash, tg_cloud_password):
    resp = requests.post(
        "https://my.telegram.org/auth/login",
        data={
            "phone": input_phone_number,
            "random_hash": tg_random_hash,
            "password": tg_cloud_password
        }
    )
    #
    re_val = None
    re_status_id = None
    if resp.text == "true":
        re_val = resp.headers.get("Set-Cookie")
        re_status_id = True
    else:
        re_val = resp.text
        re_status_id = False
    return re_status_id, re_val


def scrap_tgweb(token):
    resp = requests.get("https://my.telegram.org/apps", headers={"Cookie": token})
    soup = BeautifulSoup(resp.text, features="html.parser")
    title_of_page = soup.title.string
    re_dict_vals = {}
    re_status_id = None
    if "configuration" in title_of_page:
        g_inputs = soup.find_all("span", {"class": "input-xlarge"})
        app_id = g_inputs[0].string
        api_hash = g_inputs[1].string
        test_configuration = g_inputs[4].string
        production_configuration = g_inputs[5].string
        re_dict_vals = {
            "App Configuration": {
                "app_id": app_id,
                "api_hash": api_hash
            },
            "Available MTProto Servers": {
                "test_configuration": test_configuration,
                "production_configuration": production_configuration
            },
            "Disclaimer": "It is forbidden to pass this value to third parties."
        }
        re_status_id = True
    else:
        tg_app_hash = soup.find("input", {"name": "hash"}).get("value")
        re_dict_vals = {
            "tg_app_hash": tg_app_hash
        }
        re_status_id = False
    return re_status_id, re_dict_vals


def create_new_tg_app(
        token,
        tg_app_hash,
        app_title,
        app_shortname,
        app_url,
        app_platform,
        app_desc
):
    return requests.post(
        "https://my.telegram.org/apps/create",
        data={
            "hash": tg_app_hash,
            "app_title": app_title,
            "app_shortname": app_shortname,
            "app_url": app_url,
            "app_platform": app_platform,
            "app_desc": app_desc
        },
        headers={"Cookie": token}
    )


def main():
    input_phone_number = input("Enter phone number: ")
    random_hash = req_tgcode(input_phone_number)
    login_code = input("Enter https://my.telegram.org login code: ")
    provided_code = extract_code(login_code)
    _, cookie = login_cookie(input_phone_number, random_hash, provided_code)
    s_telegram, responded = scrap_tgweb(cookie)
    if not s_telegram:
        create_new_tg_app(
            cookie,
            responded.get("tg_app_hash"),
            "Example Telegram App",
            "pyro-bot",
            "https://pyrogram-bot.com",
            "other",
            "some app description"
        )
    s_telegram, responded = scrap_tgweb(cookie)

    if s_telegram:
        app = Client(
            "pyrosession",
            api_id=int(responded["App Configuration"]["app_id"]),
            api_hash=str(responded["App Configuration"]["api_hash"]),
            phone_number=input_phone_number
        )
        #finally start pyrogram Client
        with app:
            print(app.get_me())
            print(final_txt(responded))


if __name__ == "__main__":
    main()
