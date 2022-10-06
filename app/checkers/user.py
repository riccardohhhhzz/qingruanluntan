# -*- coding: utf-8 -*-
import re


def register_params_check(content):
    """
    TODO: 进行参数检查
    """
    # 字段检查
    if 'username' not in content:
        return "username", False
    if 'password' not in content:
        return "password", False
    if 'nickname' not in content:
        return "nickname", False
    if 'url' not in content:
        return "url", False
    if 'mobile' not in content:
        return "mobile", False
    if 'magic_number' not in content:
        content['magic_number'] = 0

    # 用户账号检查
    username = content['username']
    usernameLength = len(username)
    if usernameLength < 5 or usernameLength > 12:
        return "username", False
    if not (str.isalnum(username) and not str.isdigit(
            username) and not str.isalpha(username)):
        return "username", False
    charEndIndex = 0
    for i in range(usernameLength - 1):
        if str.isalpha(username[i]) and str.isdigit(username[i + 1]):
            charEndIndex = i + 1
            break
    expectedCharString = username[:charEndIndex]
    expectedNumString = username[charEndIndex:]
    if not str.isdigit(expectedNumString) or not str.isalpha(
            expectedCharString):
        return "username", False
    if str.isupper(expectedCharString) or str.islower(expectedCharString):
        return "username", False

    # 用户密码检查
    password = content['password']
    # 限制只能有数字、大小写字母、指定字符，并且长度限制为{8，15}
    pattern1 = r"^[A-Za-z0-9\-_\*\^]{8,15}$"
    # 保证数字、大小写、特殊字符都存在
    pattern2 = r"^(?![A-Za-z0-9]+$)(?![a-z0-9\-_\*\^]+$)"
    pattern2 += r"(?![A-Za-z\-_\*\^]+$)(?![A-Z0-9\-_\*\^]+$)"
    pwdOk = False
    if re.match(pattern1, password) and re.match(pattern2, password):
        pwdOk = True
    if not pwdOk:
        return "password", False

    # 用户手机号检查
    mobile = content['mobile']
    if not mobile.startswith('+') or '.' not in mobile:
        return "mobile", False
    areaCode = mobile.split('.')[0][1:]
    if not (len(areaCode) == 2 and str.isdigit(areaCode)):
        return "mobile", False
    phoneNumber = mobile.split('.')[1]
    if not (len(phoneNumber) == 12 and str.isdigit(phoneNumber)):
        return "mobile", False

    # 用户url检查
    url = content['url']
    protocolEndIndex = url.rfind('/')
    if protocolEndIndex == -1:
        return "url", False
    protocol = url[:protocolEndIndex + 1]
    if not (protocol == "http://" or protocol == "https://"):
        return "url", False
    domain = url[protocolEndIndex + 1:]
    if len(domain) < 1 or len(domain) > 48 or '.' not in domain:
        return "url", False
    tags = domain.split('.')
    if str.isdigit(tags[-1]):
        return "url", False
    for i in range(len(tags)):
        if not re.match(r"^[A-Za-z0-9\-]{,47}$", tags[i]
                        ) or tags[i][0] == '-' or tags[i][-1] == '-':
            return "url", False

    # 幸运数字检查
    if content['magic_number'] < 0 or not isinstance(
            content['magic_number'], int):
        return "magic_number", False

    return "ok", True
