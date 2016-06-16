# -*- coding: utf-8 -*-
import json
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import resolve
from django.test import TestCase


from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語平臺.介面.加資料 import 加外語請教條
from 臺灣言語資料庫.資料模型 import 來源表


@patch('臺灣言語平臺.使用者模型.使用者表.判斷編號')
class 外語加成功試驗(TestCase):

    def setUp(self):
        self.鄉民 = 來源表.加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })
    def test_有對應函式(self, 登入使用者編號mock):
        對應 = resolve('/平臺項目/加外語')
        self.assertEqual(對應.func, 加外語請教條)

    def test_無登入(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = None
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '結果': '成功',
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
#         邏輯檢查
        登入使用者編號mock.assert_called_once_with(AnonymousUser())
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, True)
        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.收錄者.名, '匿名')
        self.assertEqual(外語.收錄者.屬性.count(), 0)
        self.assertEqual(外語.來源.名, '匿名')
        self.assertEqual(外語.來源.屬性.count(), 0)

    def test_有登入(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = self.鄉民.編號()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',  # 不設限，隨意增加
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '結果': '成功',
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
# 		邏輯檢查
        self.assertTrue(登入使用者編號mock.called)
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, True)
        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.收錄者, self.鄉民)

    def test_有來源(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = None
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
                '來源': json.dumps({'名': '阿媠', '職業': '學生'}),
            }
        )
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '結果': '成功',
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, True)
        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.來源.名, '阿媠')
        self.assertEqual(外語.來源.屬性.count(), 1)
        self.assertEqual(外語.來源.屬性.get().內容(), {'職業': '學生'})

    def test_預設欄位(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = self.鄉民.編號()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',  # 不設限，隨意增加
            }
        )
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '結果': '成功',
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
#         邏輯檢查
        self.assertTrue(登入使用者編號mock.called)
#         後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, True)
        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.版權.版權, '會使公開')
        self.assertEqual(外語.種類.種類, '字詞')
        self.assertEqual(外語.語言腔口, self.閩南語)
        self.assertEqual(外語.著作所在地.著作所在地, '臺灣')
        self.assertGreaterEqual(int(外語.著作年.著作年), 2015)
        self.assertEqual(外語.外語語言, self.華語)
        self.assertEqual(外語.外語資料, '漂亮')

    def test_來源預設是自己(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = self.鄉民.編號()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps('自己'),  # 可用「自己」，會把來源指向自己。一樣先轉成字串。
                '外語資料': '漂亮',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '結果': '成功',
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
# 		邏輯檢查
        self.assertTrue(登入使用者編號mock.called)
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, True)
        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.收錄者, self.鄉民)
        self.assertEqual(外語.來源, self.鄉民)

    def test_來源名自己(self, 登入使用者編號mock):
        登入使用者編號mock.return_value = self.鄉民.編號()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '來源': json.dumps({'名': '自己'}),  # 當作一个人叫做「自己」
                '外語資料': '漂亮',
            }
        )
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '結果': '成功',
            '平臺項目編號': 回應資料['平臺項目編號'],
        })
# 		邏輯檢查
        self.assertTrue(登入使用者編號mock.called)
# 		後端資料庫檢查
        編號 = int(回應資料['平臺項目編號'])
        self.assertEqual(平臺項目表.objects.get(pk=編號).是資料源頭, True)
        外語 = 平臺項目表.objects.get(pk=編號).外語
        self.assertEqual(外語.收錄者, self.鄉民)
        self.assertEqual(外語.來源.名, '自己')
        self.assertEqual(外語.來源.屬性.count(), 0)

    def test_仝款資料加兩擺(self, 登入使用者編號mock):
        # 種類、語言腔口、外語語言、外語資料，四个攏仝款就袂使閣加矣
        登入使用者編號mock.return_value = self.鄉民.編號()
        第一擺回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
        第一擺回應資料 = json.loads(第一擺回應.content.decode("utf-8"))
        外語表資料數 = 外語表.objects.all().count()
        回應 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        )
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = json.loads(回應.content.decode("utf-8"))
        self.assertEqual(回應資料, {
            '結果': '成功',
            '其他': '這個外語已經有了',
            '平臺項目編號': 第一擺回應資料['平臺項目編號'],
        })
        self.assertEqual(外語表資料數, 外語表.objects.all().count())
