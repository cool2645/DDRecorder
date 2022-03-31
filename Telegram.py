import abc
import datetime
import logging
import traceback
import requests
import urllib3
from requests.adapters import HTTPAdapter

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TelegramBotApi:

    def __init__(self, config: dict):

        default_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36 '
        }
        self.headers = default_headers
        self.session = requests.session()
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.room_id = ''
        self.site_name = ''
        self.site_domain = ''
        self.config = config

    def common_request(self, method: str, url: str, params: dict = None, data: dict = None) -> requests.Response:
        url = self.config.get('root', {}).get('telegram_url', '/') + url
        try:
            connection = None
            if method == 'GET':
                connection = self.session.get(
                    url, headers=self.headers, params=params, verify=False, timeout=5)
            if method == 'POST':
                connection = self.session.post(
                    url, headers=self.headers, params=params, data=data, verify=False, timeout=5)
            return connection
        except requests.exceptions.RequestException as e:
            logging.error("Telegram Request Error"+str(e)+traceback.format_exc())
