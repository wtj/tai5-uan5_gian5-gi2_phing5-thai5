# -*- coding: utf-8 -*-
from django.test import TestCase
import json


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 版權表
from 臺灣言語資料庫.欄位資訊 import 字詞
from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語資料庫.資料模型 import 語言腔口表

class 資料庫加意見試驗(TestCase):
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

	def tearDown(self):
		pass

# 	def test_加意見(self):
# 		平臺項目 = 平臺項目表.加外語資料(self.外語內容)
# 				
# 				'平臺項目編號':str(平臺項目.編號()),
# 				'意見內容':'誠好',
		
