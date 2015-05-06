# -*- coding: utf-8 -*-
from django.test import TestCase
import json
from unittest.mock import patch


from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語資料庫.資料模型 import 語言腔口表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語平臺.項目模型 import 平臺項目表

class 意見介面試驗(TestCase):
	def setUp(self):
		版權表.objects.create(版權='會使公開')
		種類表.objects.create(種類=字詞)
		語言腔口表.objects.create(語言腔口='客語')
		使用者 = 使用者表.加使用者('sui2@pigu.tw', {"名":'鄉民', '出世年':'1950', '出世地':'臺灣', },)
		self.外語內容 = {
					'收錄者':使用者.編號(),
					'來源':json.dumps({'名':'阿媠', '職業':'學生'}),
					'版權': '會使公開',
					'種類':'字詞',
					'語言腔口':'閩南語',
					'著作所在地':'花蓮',
					'著作年':'2014',
					'屬性':json.dumps({'詞性':'形容詞', '字數':'2'}),
					'外語語言':'華語',
					'外語資料':'水母',
				}

		self.登入使用者編號patcher = patch('臺灣言語平臺.使用者模型.使用者表.判斷編號')
		self.登入使用者編號mock = self.登入使用者編號patcher.start()
		self.登入使用者編號mock.return_value = 使用者.編號()
	def tearDown(self):
		self.登入使用者編號patcher.stop()
	
	@patch('臺灣言語平臺.項目模型.平臺項目表.加意見')
	def test_加意見(self, 加意見mock):
		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
		加意見mock.return_value = 15277
		
		回應 = self.client.post(
			'/資料/加意見', {
				'平臺項目編號':str(平臺項目.編號()),
				'意見內容':'誠好',
			}
		)
		self.assertEqual(回應.status_code, 200)
		回應資料 = json.loads(回應.content.decode("utf-8"))
		self.assertEqual(回應資料['結果'], '成功')
		self.assertEqual(回應資料['意見編號'], 15277)
		
		加意見mock.assert_called_once_with(平臺項目.編號(), '誠好')