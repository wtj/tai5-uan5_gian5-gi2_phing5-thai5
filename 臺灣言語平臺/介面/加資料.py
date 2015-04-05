# -*- coding:utf-8 -*-
from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
import json


from 臺灣言語資料庫.資料模型 import 種類表
from 臺灣言語平臺.使用者模型 import 使用者表
from 臺灣言語平臺.項目模型 import 平臺項目表

_自己json字串 = json.dumps('自己')

class 失敗的json回應(JsonResponse):
	def __init__(self, 失敗原因):
		super(失敗的json回應, self).__init__({
				'結果':'失敗',
				'原因':失敗原因,
			})
class 成功的json回應(JsonResponse):
	def __init__(self, 平臺項目編號):
		super(成功的json回應, self).__init__({
			'結果':'成功',
			'平臺項目編號':str(平臺項目編號),
		})

def 加外語請教條(request):
	欄位表 = ['來源',
		'種類',
		'語言腔口',
		'著作所在地',
		'著作年',
		'屬性',
		'外語語言',
		'外語資料',
	]
	內容 = {
		'收錄者': 使用者表 .判斷編號(request.user),
		'版權': '會使公開',
		}
	try:
		for 欄位 in 欄位表:
			內容[欄位] = request.POST[欄位]
	except MultiValueDictKeyError:
		return 失敗的json回應('資料欄位有缺')
	if 內容['來源'] == _自己json字串:
		內容['來源'] = 內容['收錄者']
		
	try:
		平臺項目 = 平臺項目表.加外語資料(內容)
	except TypeError:
		return 失敗的json回應('無登入')
	except ValueError:
			return 失敗的json回應('來源抑是屬性無轉json字串')
	except KeyError:
		return 失敗的json回應('來源沒有「名」的欄位')
	except 種類表.DoesNotExist:
		return 失敗的json回應('種類欄位不符規範')
	except ValidationError:
		return 失敗的json回應('請教條已經有了')
	else:
		return 成功的json回應(平臺項目.編號())
	
def 加新詞影音(request):
	if '影音資料' in request.POST:
		return 失敗的json回應('影音資料不是檔案')
	欄位表 = [
		'來源',
		'種類',
		'語言腔口',
		'著作所在地',
		'著作年',
		'屬性',
	]
	內容 = {
		'收錄者': 使用者表 .判斷編號(request.user),
		'版權': '會使公開',
		}
	try:
		for 欄位 in 欄位表:
			內容[欄位] = request.POST[欄位]
		內容['原始影音資料'] = request.FILES['影音資料']
		外語請教條項目編號 = int(request.POST['外語請教條項目編號'])
	except MultiValueDictKeyError:
		return 失敗的json回應('資料欄位有缺')
	except ValueError:
		return 失敗的json回應('編號欄位不是數字字串')
	if 內容['來源'] == _自己json字串:
		內容['來源'] = 內容['收錄者']
		
	try:
		平臺項目 = 平臺項目表.外語錄母語(外語請教條項目編號, 內容)
	except TypeError:
		return 失敗的json回應('無登入')
	except ValueError as 錯誤:
		錯誤資訊 = 錯誤.args[0]
		if '新資料的種類' in 錯誤資訊 and '原本資料的種類' in 錯誤資訊:
			return 失敗的json回應('種類和外語請教條不一樣')
		elif '新資料的語言腔口' in 錯誤資訊 and '原本資料的語言腔口' in 錯誤資訊:
			return 失敗的json回應('語言腔口和外語請教條不一樣')
		else: 
			return 失敗的json回應('來源抑是屬性無轉json字串')
	except KeyError:
		return 失敗的json回應('來源沒有「名」的欄位')
	except 平臺項目表.DoesNotExist:
		return 失敗的json回應('編號號碼有問題')
	else:
		return 成功的json回應(平臺項目.編號())
		
def 加新詞文本(request):
	欄位表 = [
		'來源',
		'種類',
		'語言腔口',
		'著作所在地',
		'著作年',
		'屬性',
		'文本資料',
	]
	內容 = {
		'收錄者': 使用者表 .判斷編號(request.user),
		'版權': '會使公開',
		}
	try:
		for 欄位 in 欄位表:
			內容[欄位] = request.POST[欄位]
		新詞影音項目編號 = int(request.POST['新詞影音項目編號'])
	except MultiValueDictKeyError:
		return 失敗的json回應('資料欄位有缺')
	except ValueError:
		return 失敗的json回應('編號欄位不是數字字串')
	if 內容['來源'] == _自己json字串:
		內容['來源'] = 內容['收錄者']
		
	try:
		平臺項目 = 平臺項目表.影音寫文本(新詞影音項目編號, 內容)
	except TypeError:
		return 失敗的json回應('無登入')
	except ValueError as 錯誤:
		錯誤資訊 = 錯誤.args[0]
		if '新資料的種類' in 錯誤資訊 and '原本資料的種類' in 錯誤資訊: 
			return 失敗的json回應('種類和新詞影音不一樣')
		elif '新資料的語言腔口' in 錯誤資訊 and '原本資料的語言腔口' in 錯誤資訊: 
			return 失敗的json回應('語言腔口和新詞影音不一樣')
		else: 
			return 失敗的json回應('來源抑是屬性無轉json字串')
	except KeyError:
		return 失敗的json回應('來源沒有「名」的欄位')
	except 平臺項目表.DoesNotExist:
		return 失敗的json回應('編號號碼有問題')
	else:
		return 成功的json回應(平臺項目.編號())

def 外語加新詞文本(request):
	欄位表 = [
		'來源',
		'種類',
		'語言腔口',
		'著作所在地',
		'著作年',
		'屬性',
		'文本資料',
	]
	內容 = {
		'收錄者': 使用者表 .判斷編號(request.user),
		'版權': '會使公開',
		}
	try:
		for 欄位 in 欄位表:
			內容[欄位] = request.POST[欄位]
		外語請教條項目編號 = int(request.POST['外語請教條項目編號'])
	except MultiValueDictKeyError:
		return 失敗的json回應('資料欄位有缺')
	except ValueError:
		return 失敗的json回應('編號欄位不是數字字串')
	if 內容['來源'] == _自己json字串:
		內容['來源'] = 內容['收錄者']
		
	try:
		平臺項目 = 平臺項目表.外語翻母語(外語請教條項目編號, 內容)
	except TypeError:
		return 失敗的json回應('無登入')
	except ValueError as 錯誤:
		錯誤資訊 = 錯誤.args[0]
		if '新資料的種類' in 錯誤資訊 and '原本資料的種類' in 錯誤資訊: 
			return 失敗的json回應('種類和外語請教條不一樣')
		elif '新資料的語言腔口' in 錯誤資訊 and '原本資料的語言腔口' in 錯誤資訊: 
			return 失敗的json回應('語言腔口和外語請教條不一樣')
		else: 
			return 失敗的json回應('來源抑是屬性無轉json字串')
	except KeyError:
		return 失敗的json回應('來源沒有「名」的欄位')
	except 平臺項目表.DoesNotExist:
		return 失敗的json回應('編號號碼有問題')
	else:
		return 成功的json回應(平臺項目.編號())
