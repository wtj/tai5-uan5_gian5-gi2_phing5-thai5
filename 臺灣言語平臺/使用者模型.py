# -*- coding: utf-8 -*-
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.utils import valid_email_or_none
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from allauth.account.adapter import get_adapter as get_account_adapter


from 臺灣言語資料庫.資料模型 import 來源表
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 資料類型表

class	使用者接口(DefaultAccountAdapter):
# allauth.account.adapter.DefaultAccountAdapter:
# 	def new_user(self, request):
# # 		 Instantiates a new, empty User.
# 		pass
	def save_user(self, request, user, form, commit=True):
		"""
		Saves a new `User` instance using information provided in the
		signup form.
		"""
# 		from .utils import user_username, user_email, user_field
		
		data = form.cleaned_data
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		username = data.get('username')
		user_email(user, email)
		if len(username) != 0:
			來源名 = username
		elif len(last_name + first_name) != 0:
			來源名 = last_name + first_name
		else:
			來源名 = email
		try:
			user.來源
		except:
			user.來源 = 來源表. 加來源({ '名':來源名})

		if 'password1' in data:
			user.set_password(data["password1"])
		else:
			user.set_unusable_password()
		self.populate_username(request, user)
		if commit:
			# Ability not to commit makes it easier to derive from
			# this adapter by adding
			user.save()
		return user
	def populate_username(self, request, user):
		"""
		Fills in a valid username, if required and missing.  If the
		username is already present it is assumed to be valid
		(unique).
		"""
		email = user_email(user)
		try:
			user.來源
		except:
			user.來源 = 來源表. 加來源({ '名':email})
# 			user_field(user.來源, 來源)
# 	def confirm_email(self, request, email_address):
# # 		Marks the email address as confirmed and saves to the db.
# 		pass
# 	def generate_unique_username(self,txts, regex=None):
# # 		Returns a unique username from the combination of strings present in txts iterable. A regex pattern can be passed to the method to make sure the generated username matches it.
# 		pass
class 社接口(DefaultSocialAccountAdapter):
# 	allauth.socialaccount.adapter.DefaultSocialAccountAdapter:
# 	def new_user(self, request, sociallogin):
# # 		Instantiates a new, empty User.
# 		pass
	def save_user(self, request, sociallogin, form=None):
		"""
		Saves a newly signed up social login. In case of auto-signup,
		the signup form is not available.
		"""
		u = sociallogin.user
		u.set_unusable_password()
		if form:
			get_account_adapter().save_user(request, u, form)
		else:
			get_account_adapter().populate_username(request, u)
		print(sociallogin)
		sociallogin.save(request)
		return u
	def populate_user(self, request, sociallogin, data):
# 		Hook that can be used to further populate the user instance (sociallogin.account.user). Here, data is a dictionary of common user properties (first_name, last_name, email, username, name) that the provider already extracted for you.
		"""
		Hook that can be used to further populate the user instance.
		
		For convenience, we populate several common fields.
		
		Note that the user instance being populated represents a
		suggested User instance that represents the social user that is
		in the process of being logged in.
		
		The User instance need not be completely valid and conflict
		free. For example, verifying whether or not the username
		already exists, is not a responsibility.
  	  """
		user = sociallogin.user

		email = data.get('email')
		user_email(user, valid_email_or_none(email) or '')

		name = data.get('name')
		username = data.get('username')
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		
		if name :
			來源名 = name
		elif username:
			來源名 = username
		elif last_name and first_name:
			來源名 = last_name + first_name
		else:
			來源名 = email
		try:
			user.來源
		except:
			user.來源 = 來源表. 加來源({ '名':來源名})
		return user

class MyMgr(BaseUserManager):
	def create_user(self, email, password=None, **other):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')
		
		user = self.model.加使用者(
			email=self.normalize_email(email),
			來源內容={'名':'3'},
			)
		
		user.set_password(password)
		user.save(using=self._db)
		return user
	def create_superuser(self, email, password, **other):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(email,
		    password=password,
		)
		user.is_admin = True
		user.save(using=self._db)
		return user

class 使用者表(AbstractBaseUser):
	來源 = models.OneToOneField(來源表, related_name='a', primary_key=True, null=False)
	email = models.EmailField(unique=True)  # null=False
	密碼 = models.CharField(max_length=16, blank=True)
# 	服務 = models.CharField(max_length=50)  # ??
# 	編號 = models.IntegerField()  # ??
	分數 = models.IntegerField(default=0)
	REQUIRED_FIELDS = ()  # for auth
	USERNAME_FIELD = 'email'  # for auth
# 	階級 = models.IntegerField() 用函式算好矣
	objects = MyMgr()
	is_admin = models.BooleanField(default=False)
	def 編號(self):
		return self.來源.編號()
	@classmethod
	def 加使用者(cls, email, 來源內容):
		來源 = 來源表. 加來源(來源內容)
		return cls.objects.create(來源=來源, email=email)
	@classmethod
	def 判斷編號(cls, 使用者物件):
		if 使用者物件.is_authenticated():
			return 使用者物件.編號()
		return None
	
	def get_full_name(self):
		# The user is identified by their email address
		return self.email
	
	def get_short_name(self):
		# The user is identified by their email address
		return self.email
	
	def __str__(self):  # __unicode__ on Python 2
		return self.email
	@property
	def is_staff(self):
		return True

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return self.is_admin

class 評分狀況表(models.Model):
	使用者 = models.ForeignKey(來源表, related_name='+')
	項目 = models.ForeignKey(平臺項目表, related_name='+')
	分數 = models.IntegerField()

class 評分總合表(models.Model):
	'敢有需要這個表？'
	項目 = models.OneToOneField(平臺項目表, related_name='評分總合表')
	正規化結果 = models.BooleanField(default=False)
	分數 = models.IntegerField()

class 意見表(models.Model):
	使用者 = models.ForeignKey(來源表, related_name='+')
	項目 = models.ForeignKey(平臺項目表, related_name='意見')
	發表時間 = models.DateTimeField(auto_now_add=True)
	內容 = models.TextField()
	
class 代誌列表(models.Model):
# 	產生資料、意見、評分、…
	代誌名 = models.CharField(unique=True, max_length=20)
	
class 做代誌的分數表(models.Model):
	資料類型 = models.ForeignKey(資料類型表, related_name='+')
	代誌 = models.ForeignKey(代誌列表, related_name='+')
	上少分數 = models.IntegerField()
	做了分數變化 = models.IntegerField()
