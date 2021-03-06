import os
from datetime import datetime

from django.http import QueryDict
from django.conf import settings
from django.core.exceptions import ValidationError

from constance import LazyConfig

from .sms import AliYunSMS
from .exception import SmsError
import logging

logger = logging.getLogger("info")

config = LazyConfig()


def put_value(key, value):
    """
    更新数据库设置项
    :param key: 键名
    :param value: 值
    :return: 无返回
    """
    setattr(config, key, value)


def get_value(key):
    """
    获取数据库设置项值
    :param key: 键名
    :return: 键名对应的设置项值
    """
    return getattr(config, key)


def get_time_filename(filename):
    """
    将文件名修改为 年月日-时分秒-毫秒 格式
    :param filename: 原文件名
    :return: 年月日-时分秒-毫秒
    """
    # 文件拓展名
    ext = os.path.splitext(filename)[1]
    # 文件目录
    d = os.path.dirname(filename)
    # 自定义文件名,年月日-时分秒-毫秒
    current_time = datetime.now().strftime('%Y%m%d-%H%M%S-%f')[:-3]
    # 合成文件名
    filename = os.path.join(d, current_time + ext)
    return filename


def get_list(_dict, key):
    """
    :param _dict: QueryDict or dict
    :param key: list 键名
    :return: _dict中key对应的list
    """
    if isinstance(_dict, QueryDict):
        return _dict.getlist(key)
    else:
        return _dict[key]


def isdigit(string):
    """
    :param string:
    :return: 该字符是否是数字
    """
    if isinstance(string, int):
        return True
    else:
        return isinstance(string, str) and string.isdigit()


_true_set = {'yes', 'true', 't', 'y', '1'}
_false_set = {'no', 'false', 'f', 'n', '0'}


def str2bool(value, raise_exc=False):
    """
    str转bool
    :param value: 值
    :param raise_exc: 是否抛出异常
    :return: 转换后的值或者None
    """
    value = value.lower()
    if value in _true_set:
        return True
    if value in _false_set:
        return False
    if raise_exc:
        raise ValueError('Expected "%s"' % '", "'.join(_true_set | _false_set))
    return None


def str2bool_exc(value):
    """
    str转bool 抛出异常
    :param value: value: 值
    :return:转换后的值或者ValueError
    """
    return str2bool(value, raise_exc=True)


def send_sms(phone_number, template_code, template_param):
    try:
        response = AliYunSMS().send_single(phone_number, "Oasis绿洲", template_code, template_param)

        if response.status_code == 200:
            resp_json = response.json()
            code = resp_json['Code']
            if code == 'OK':
                pass
            else:
                raise SmsError(code)
        else:
            logger.error('{} {}'.format(response.status_code, response.text))
            raise SmsError('连接短信服务器失败')
    except Exception as e:
        raise SmsError(str(e))


def sizeof_fmt(num, suffix='B'):
    """
    :param num: 文件大小
    :param suffix:
    :return:可读str
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def validate_image_ext(ext):
    """
    :param ext: ext
    :return: 文件是否为图片类型
    """
    if ext and ext.lower() in ['jpg', 'png', 'svg', 'gif']:
        return True
    return False


def validate_video_ext(ext):
    """
    :param ext: ext
    :return: 文件是否为视频类型
    """
    if ext and ext.lower() in ['gif', 'mp4', 'rmvb', 'avi', 'wma', '3gp', 'flash', 'mid']:
        return True
    return False


def validate_file_size(value):
    """
    限制文件大小为20M 20M=20*1024KB=20*1024*1024Byte (Byte既字节)
    :param value:文件实例
    :return: raise 文件大小超过20MB
    """
    if value.size > settings.MAX_FILE_SIZE:
        raise ValidationError(u'文件{}大小超过{}'.format(value.name, sizeof_fmt(settings.MAX_FILE_SIZE)))
