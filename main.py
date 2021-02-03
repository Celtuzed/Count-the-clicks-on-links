import requests
import os
import logging
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


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


def check_bitlink(bitly_token, netloc_and_path):
    url = "https://api-ssl.bitly.com/v4/bitlinks/{}".format(netloc_and_path)
    authorization_data = {
        "Authorization": "Bearer {}".format(bitly_token)
    }
    response = requests.get(url, headers=authorization_data)
    return response.ok

if __name__ == '__main__':
    load_dotenv()
    bitly_token = os.getenv("BITLY_TOKEN")
    parser = argparse.ArgumentParser(
        description='Этот код нужен для создания коротких ссылок (битлинков), а также для того чтобы узнать сколько раз перешли по сокращённой ссылке.'
    )
    parser.add_argument('url_or_bitlink', help='Битлинк или ссылка')
    args = parser.parse_args()
    long_url_or_bitlink = args.url_or_bitlink
    parsed_url = urlparse(long_url_or_bitlink)
    netloc_and_path = (parsed_url.netloc + parsed_url.path)
    if check_bitlink(bitly_token, netloc_and_path):
        print('Количество переходов по битлинку -', get_count_clicks(bitly_token, netloc_and_path))
    elif get_shorten_link(bitly_token, long_url_or_bitlink):
        print('сокращённая cсылка - ', get_shorten_link(bitly_token, long_url_or_bitlink))
