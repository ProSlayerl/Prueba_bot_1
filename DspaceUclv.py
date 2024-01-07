import requests
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoderMonitor
from requests_toolbelt import MultipartEncoder
from functools import partial
import uuid
import json
import time
import requests_toolbelt as rt
import mimetypes
from json import loads
from time import sleep

class DspaceClient(object):
	def __init__(self,user,password,ids):
		self.host = "https://dspace.uclv.edu.cu/"
		self.user = user
		self.ids = ids
		self.password = password
		self.session = requests.session()
		self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
		self.X_CORRELATION_ID = None
		self.X_XSRF_TOKEN = None
		self.authorization = None

	def login(self):
		resp = self.session.get(self.host+"home",headers=self.headers)
		CORRELATION = str(resp.text).split("correlationId&q;:&q;")[1].split("&")[0]
		self.X_CORRELATION_ID = CORRELATION
		resp = self.session.get(self.host+"server/api",headers=self.headers)
		XSRF = str(resp.cookies).split("=")[1].split(" ")[0]
		self.X_XSRF_TOKEN = XSRF
		#post
		payload = {
			"password": self.password,
			"user": self.user
		}
		resp = self.session.post(self.host+"server/api/authn/login",data=payload,headers={"X-REFERRER":"/home","X-CORRELATION-ID":CORRELATION,"X-XSRF-TOKEN":XSRF,**self.headers})
		self.X_XSRF_TOKEN = resp.headers["dspace-xsrf-token"] #resp.cookies["DSPACE-XSRF-COOKIE"]
		self.authorization = resp.headers["authorization"]
		print(resp.status_code)
		#verify_login
		if resp.status_code==200:
			return True
		else:
			return False

	def upload(self,file):
		of = open(file,'rb')
		b = uuid.uuid4().hex
		mime_type, _ = mimetypes.guess_type(file)
		if not mime_type:
			mime_type = "application/x-7z-compressed"
		upload_file = {'file':(file,of,mime_type)}
		encoder = rt.MultipartEncoder(upload_file,boundary=b)
		monitor = MultipartEncoderMonitor(encoder)
		resp = self.session.post(self.host+"server/api/submission/workspaceitems/"+self.ids,data=monitor,headers={"Authorization":self.authorization,"X-XSRF-TOKEN":self.X_XSRF_TOKEN,"Content-Type":"multipart/form-data; boundary="+b,**self.headers})
		data = loads(resp.text)
		uid = data["sections"]["upload"]["files"][-1]["uuid"]
		u = data["sections"]["upload"]["files"][-1]["url"]
		url = f"{self.host}bitstreams/{uid}/download"
		return {"name":file.split("/")[-1],"url":url}