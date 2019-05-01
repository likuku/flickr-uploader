import flickrapi
import webbrowser
import os
import sys
import logging
import json
import time
import random

# # config
config_dict = json.load(open('instance/config.json', 'r'))
# # config

# # log
# create logger
logger = logging.getLogger('uploader_log')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler(config_dict['log_file'])
fh.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
logger.addHandler(fh)
# # log

# # flickr API init
api_key = config_dict['api_key']
api_secret = config_dict['api_secret']
flickr = flickrapi.FlickrAPI(api_key, api_secret)

print('Step 1: authenticate')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms='write'):

    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms='write')
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = str(input('Verifier code: '))

    # Trade the request token for an access token
    flickr.get_access_token(verifier)
# # flickr API init
print('Step 2: use Flickr')


def upload_to_flickr(_str_file_path, _str_title, _str_tags, _dict_private):
    try:
        _rsp = flickr.upload(filename=_str_file_path,
                             title=_str_title,
                             tags=_str_tags,
                             safety_level=_dict_private['safety_level'],
                             content_type=_dict_private['content_type'],
                             hidden=_dict_private['hidden'],
                             is_public=_dict_private['is_public'],
                             is_family=_dict_private['is_family'],
                             is_friend=_dict_private['is_friend'])
        logger.info('ok %s', _str_file_path)
    except Exception as e:
        pass
        logger.error('error %s', _str_file_path)


def get_str_date_from_filename_by_switch_screen(_str_input):
    try:
        _str_date = _str_input[0:8]
    except Exception as e:
        pass
        _str_date = None
    return(_str_date)


def make_str_tags(_tags_list_from_json, _file_name):
    _str_file_date_yyyymmdd = get_str_date_from_filename_by_switch_screen(_file_name)
    _str_file_date_yyyymm = _str_file_date_yyyymmdd[0:6]
    _tmp_list = _tags_list_from_json
    _tmp_list = list(set(_tmp_list))
    _tmp_list.append(_str_file_date_yyyymmdd)
    _tmp_list.append(_str_file_date_yyyymm)
    if len(_tmp_list) > 0:
        _str_tags = ' '.join(_tmp_list)
    else:
        _str_tags = ''
    return(_str_tags)


def get_str_raw_src_media_path_from_keyboard():
    _str_input_msg = '请输入素材图片目录路径 : '
    _str_raw_input = str(input(_str_input_msg))
    return(_str_raw_input)


def check_str_raw_src_media_path(_str_input):
    if len(_str_input) == 0:
        _bool_src_media_path = False
    else:
        _bool_src_media_path = os.path.isdir(_str_input.replace('"', '').strip())
    return(_bool_src_media_path)


def rebuild_str_src_media_path(_str_input):
    _str_src_input = _str_input.replace('"','').strip()
    # 路径里包含空格，则拖拽文件时，windows 会自动给首尾加一对双引号，subprocess 不需要
    return(_str_src_input)


def get_str_list_src_images(_str_dir_path):
    _str_list = []
    with os.scandir(_str_dir_path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                _str_list.append(entry.name)
    return(_str_list)


if __name__ == "__main__":
    pass
    _path_for_work = get_str_raw_src_media_path_from_keyboard()
    if check_str_raw_src_media_path(_path_for_work) is False:
        print('素材图片目录路径错误')
        sys.exit()
    _path_for_work = rebuild_str_src_media_path(_path_for_work)
    _list_media_input = get_str_list_src_images(_path_for_work)
    _tags_from_json = config_dict['tags']
    _dict_private = config_dict['private']
    for _media_name in _list_media_input:
        _file_path = '%s/%s' % (_path_for_work, _media_name)
        _title = _media_name.rsplit('.')[0]
        _tags = make_str_tags(_tags_from_json, _media_name)
        if _media_name.count('.mp4') is not 0:
            time.sleep(random.choice((10.0, 15.0, 20.0)))
        time.sleep(random.choice((0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)))
        upload_to_flickr(_file_path, _title, _tags, _dict_private)
