import requests
from secret_config import download_api_url
import json
from app_config import wechat
import time
import re

temp_message = {}
temp_return_message = {}


def torrentkitty_search_by_keyword(keyword, **kwargs):
    if re.findall('^[a-zA-Z]{1,5}[\-\s]{0,3}[0-9]{1,5}$', keyword):
        return "答应我,不要搜毛片好吗?"

    user_ID = kwargs.get('user_ID')
    if temp_return_message.get(user_ID):
        returm_message = temp_return_message[user_ID]
        del temp_return_message[user_ID]

        handler = kwargs.get('handler')
        handler[user_ID] = torrentkitty_get_download_url
        return returm_message

    r = requests.get(download_api_url + '/torrent/search/' + keyword)
    results = json.loads(r.text)
    temp_message[user_ID] = results
    content = ""
    for index, result in enumerate(results):
        content += str(index)
        content += '. '
        movie_name = result.get('name')
        movie_name = movie_name[0:50]
        content += movie_name
        content += '\n'
    content += '请输入序号获取'
    temp_return_message[user_ID] = content

    return


def torrentkitty_get_download_url(id, **kwargs):
    user_ID = kwargs.get('user_ID')
    if temp_return_message.get(user_ID):
        returm_message = temp_return_message[user_ID]
        del temp_return_message[user_ID]
        handler = kwargs.get('handler')
        del handler[user_ID]
        return returm_message

    detail_url = temp_message.get(user_ID)[int(id)].get('detail_url')

    r = requests.get(download_api_url + '/torrent/get_download_url/', params={'url': detail_url})

    result = json.loads(r.text).get('url')
    temp_return_message[user_ID] = result

    return


def clear_temp(user_ID):
    if temp_return_message.get(user_ID):
        del temp_return_message[user_ID]
    if temp_message.get(user_ID):
        del temp_message[user_ID]
