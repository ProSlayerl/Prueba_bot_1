import aiohttp
from tools.funciones import Progress
from json import loads
from random import randint
from urllib.parse import quote_plus , quote
import re

class MoodleClient:
    def __init__(self,username,password,moodle,proxy):
        self.url = moodle
        self.username = username
        self.password = password
        self.session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True),connector=proxy)
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"}		
    
    async def uploadtoken(self,f,progress,token):
        try:
            print(self.url)
            url = self.url+"webservice/upload.php"
            print(0)
            file = Progress(f,progress)
            query = {"token":token,"file":file}
            print(query)
            async with self.session.post(url,data=query,headers=self.headers,ssl=False) as response:
                text = await response.text()
            print(1)
            print(text)
            print(token)
            dat = loads(text)[0]
            url = self.url+"draftfile.php/"+str(dat["contextid"])+"/user/draft/"+str(dat["itemid"])+"/"+str(quote(dat["filename"]))
            print(url)
            urlw = self.url+"webservice/rest/server.php?moodlewsrestformat=json"
            query = {"formdata":f"name=Event&eventtype=user&timestart[day]=31&timestart[month]=9&timestart[year]=3786&timestart[hour]=00&timestart[minute]=00&description[text]={quote_plus(url)}&description[format]=1&description[itemid]={randint(100000000,999999999)}&location=&duration=0&repeat=0&id=0&userid={dat['userid']}&visible=1&instance=1&_qf__core_calendar_local_event_forms_create=1","moodlewssettingfilter":"true","moodlewssettingfileurl":"true","wsfunction":"core_calendar_submit_create_update_form","wstoken":token}
            async with self.session.post(urlw,data=query,headers=self.headers,ssl=False) as response:
                text = await response.text()	
            try:
                a = re.findall("https?://[^\s\<\>]+[a-zA-z0-9]",loads(text)["event"]["description"])[-1].replace("pluginfile.php/","webservice/pluginfile.php/")+"?token="+token		
                #return a , url		
                return {'calendario': a , 'draft': url}
            except:	
                return False
        except Exception as ex:
            print(ex)
            return False