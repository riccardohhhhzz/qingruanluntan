import unittest

from app.checkers.user import register_params_check


class BasicTestCase(unittest.TestCase):
    '''
    TODO: 在这里补充注册相关测试用例
    '''

    def test_register_params_check(self):
        content = {
            'username': 'asdA12312',
            'password': '123nasi_Asd',
            'nickname': 'huangzhengchao',
            'url': 'https://hzcportfolio.dora.run',
            'mobile': '+86.019801280171',
            'magic_number': 7
        }
        self.assertEqual(register_params_check(content), ("ok", True))
        content = {
            'username': '1a2vc',
            'password': '123nasi_Asd',
            'nickname': 'huangzhengchao',
            'url': 'https://hzcportfolio.dora.run',
            'mobile': '+86.019801280171',
        }
        self.assertEqual(register_params_check(content), ("username", False))
        content = {
            'username': 'aaaaaaaa',
            'password': '123nasi_Asd',
            'nickname': 'huangzhengchao',
            'url': 'https://hzcportfolio.dora.run',
            'mobile': '+86.019801280171',
        }
        self.assertEqual(register_params_check(content), ("username", False))
        content = {
            'username': 'HzC88',
            'password': ',,,,,,,,',
            'nickname': 'huangzhengchao',
            'url': 'https://hzcportfolio.dora.run',
            'mobile': '+86.019801280171',
        }
        self.assertEqual(register_params_check(content), ("password", False))
        content = {
            'username': 'Riccardo8888',
            'password': '_^*ABSa1239__88',
            'nickname': 'huangzhengchao',
            'url': 'https://hzcportfolio.dora.run',
            'mobile': '86019801280171',
        }
        self.assertEqual(register_params_check(content), ("mobile", False))
        content = {
            'username': 'Riccardo8888',
            'password': '_^*ABSa1239__88',
            'nickname': 'huangzhengchao',
            'url': 'https://hzcportfolio.dora.run',
            'mobile': '+1xs.019801280171',
        }
        self.assertEqual(register_params_check(content), ("mobile", False))
        content = {
            'username': 'Riccardo8888',
            'password': '_^*ABSa1239__88',
            'nickname': 'huangzhengchao',
            'url': 'https://hzcportfolio.dora.run',
            'mobile': '+98.019801280xd1',
        }
        self.assertEqual(register_params_check(content), ("mobile", False))
        content = {
            'username': 'yduAab17',
            'password': 'asiiQWE867_*',
            'nickname': 'huangzhengchao',
            'url': 'file://软工作业',
            'mobile': '+99.128301280171',
        }
        self.assertEqual(register_params_check(content), ("url", False))
        content = {
            'username': 'asdbjhA432',
            'password': 'asuiASyui_^1',
            'nickname': 'huangzhengchao',
            'url': 'https://www.bai-du.123.999',
            'mobile': '+99.128301280171',
        }
        self.assertEqual(register_params_check(content), ("url", False))
        content = {
            'username': 'asdbjhA432',
            'password': 'asuiASyui_^1',
            'nickname': 'huangzhengchao',
            'url': 'https://www.-google.123.com.asd31232d1241789m',
            'mobile': '+99.128301280171',
        }
        self.assertEqual(register_params_check(content), ("url", False))
        content = {
            'username': 'aA1111',
            'password': '1A1A1A1aA__^',
            'nickname': 'huangzhengchao',
            'url': 'https://1-23.12-3.123.12C',
            'mobile': '+99.128301280171',
            'magic_number': -1
        }
        self.assertEqual(register_params_check(content), ("magic_number", False))

if __name__ == '__main__':
    unittest.main()
