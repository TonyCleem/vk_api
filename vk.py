import requests
import os
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(url):
    parse = urlparse(url)
    return parse.netloc == 'vk.cc'


def shorten_link(token, user_input):
    params = {
        'access_token': token,
        'url': user_input,
        'v': '5.131',
    }
    url = 'https://api.vk.com/method/utils.getShortLink'
    request_on_url = requests.get(url, params=params)
    request_on_url.raise_for_status()
    data_in_json = request_on_url.json()
    shortened_link = data_in_json['response']['short_url']
    return shortened_link


def get_clicks_count(token, user_input):
    parse = urlparse(user_input)
    params = {
        'access_token': token,
        'key': parse.path[1:],
        'interval': 'forever',
        'v': '5.131',
    }
    url = 'https://api.vk.com/method/utils.getLinkStats'
    request_on_url = requests.get(url, params=params)
    request_on_url.raise_for_status()
    data_in_json = request_on_url.json()
    clicks_count = data_in_json['response']['stats'][0]['views']
    return clicks_count


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['VK_TOKEN']
    parser = argparse.ArgumentParser(
        description='Укажите URL-адрес в качестве ключа'
    )
    parser.add_argument('url', help='Ваш URL-адрес')
    args = parser.parse_args()
    user_input = args.url
    if is_shorten_link(user_input):
        clicks_count = get_clicks_count(token, user_input)
        print('Clicks count: ', clicks_count)
    else:
        shortened_link = shorten_link(token, user_input)
        print(shortened_link)