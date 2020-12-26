import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def check_token():
    load_dotenv()
    bitly_token = os.getenv("SECRET_TOKEN")
    return bitly_token


def get_shorten_link(bitly_token, long_url_or_bitlink):
    url = "https://api-ssl.bitly.com/v4/shorten"
    authorization_data = {
      "Authorization": "Bearer {}".format(bitly_token)
    }
    data = {
      "long_url": long_url_or_bitlink
    }
    response = requests.post(url, headers=authorization_data, json=data)
    if response.ok:
        short_url = response.json()
        link = short_url['id']
        return link
    else:
        print("Ссылка введена неверно!")


def get_count_clicks(bitly_token, netloc_and_path):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary".format(netloc_and_path)
    authorization_data = {
      "Authorization": "Bearer {}".format(bitly_token)
    }
    response = requests.get(url, headers=authorization_data)
    if response.ok:
        count_clicks = response.json()
        clicks = count_clicks['total_clicks']
        return clicks
    else:
        print("Ссылка введена неверно!")


def check_bitlink(bitly_token, netloc_and_path):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(netloc_and_path)
    authorization_data = {
      "Authorization": "Bearer {}".format(bitly_token)
    }
    response = requests.get(url, headers=authorization_data)
    return response.ok

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
    description='Описание что делает программа'
    )
    parser.add_argument('url_or_bitlink', help='Битлинк или ссылка')
    args = parser.parse_args()


    bitly_token = check_token()
    long_url_or_bitlink = args.url_or_bitlink
    parsed_url = urlparse(long_url_or_bitlink)
    netloc_and_path = (parsed_url.netloc + parsed_url.path)
    if check_bitlink(bitly_token, netloc_and_path):
        print('Количество переходов по битлинку -', get_count_clicks(bitly_token, netloc_and_path))
    else:
        print('сокращённая cсылка - ', get_shorten_link(bitly_token, long_url_or_bitlink))
