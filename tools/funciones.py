import asyncio
from yt_dlp import YoutubeDL
import aiohttp
import requests
import json
from pathlib import Path
from time import localtime
from time import time
from io import BufferedReader
from py7zr import SevenZipFile
from py7zr import FILTER_COPY
from zipfile import ZipFile
from multivolumefile import MultiVolume
from pyrogram.types import Message, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaDocument, InputMediaPhoto, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto, InlineQueryResultCachedPhoto



#funciones de progreso
seg = 0
def download_progres(data,message,format):
	if data["status"] == "downloading":
		filename = data["filename"].split("/")[-1]
		_downloaded_bytes_str = data["_downloaded_bytes_str"]
		_total_bytes_str = data["_total_bytes_str"]
		if _total_bytes_str == "N/A":
			_total_bytes_str = data["_total_bytes_estimate_str"]		
		_speed_str = data["_speed_str"].replace(" ","")
		_format_str = format		
		msg = f"📦 𝐍𝐚𝐦𝐞: {filename}\n\n"
		msg+= f"▶️ 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐: {_downloaded_bytes_str} of {_total_bytes_str}\n\n"
		msg+= f"🎥Resolución: {_format_str}p\n\n"	
		global seg 
		if seg != localtime().tm_sec:
			try:message.edit(msg,reply_markup=message.reply_markup)
			except:pass
		seg = localtime().tm_sec

async def downloadmessage_progres(chunk,filesize,filename,start,message):
	now = time()
	diff = now - start
	mbs = chunk / diff
	barra = update_progress_bar(chunk,filesize)
	msg = f"🔽 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐\n\n𝐍𝐚𝐦𝐞: `{filename}`\n\n{barra} **{sizeof_fmt(mbs)}/s** \n\n▶️ **{sizeof_fmt(chunk)}** of **{sizeof_fmt(filesize)}**"
	global seg
	if seg != localtime().tm_sec:
		try: await message.edit(msg,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel",f"fcancel")]]))
		except:
			pass
	seg = localtime().tm_sec

def uploadfile_progres(chunk,filesize,start,filename,message):
    now = time()
    diff = now - start
    mbs = chunk / diff
    barra = update_progress_bar(chunk,filesize)
    msg = f"🔼 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 \n\n𝐍𝐚𝐦𝐞: `{filename}`\n\n{barra} **{sizeof_fmt(mbs)}/s** \n\n▶️ **{sizeof_fmt(chunk)}** of **{sizeof_fmt(filesize)}** "
    global seg
    if seg != localtime().tm_sec:
        try:
            message.edit(msg)
        except:pass
    seg = localtime().tm_sec

async def mediafiredownload(chunk,total,filename,start,message,did):
	try:
		now = time()
		diff = now - start
		mbs = chunk / diff
		barra = update_progress_bar(chunk,total)
		msg = f"🔽 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐\n\n𝐍𝐚𝐦𝐞: `{filename}`\n\n{barra} **{sizeof_fmt(mbs)}/s** \n\n▶️ **{sizeof_fmt(chunk)}** of **{sizeof_fmt(total)}**"
		global seg
		if seg != localtime().tm_sec:
			try: await message.edit(msg,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel",f"ccancel {did}")]]))
			except:pass
		seg = localtime().tm_sec
	except Exception as e:
		print(e)

def update_progress_bar(inte,max):
	percentage = inte / max
	percentage *= 100
	percentage = round(percentage)
	hashes = int(percentage / 5)
	spaces = 20 - hashes
	progress_bar = "[ " + "•" * hashes + "•" * spaces + " ]"
	percentage_pos = int(hashes / 1)
	percentage_string = "[" + str(percentage) + "%" + "]"
	progress_bar = progress_bar[:percentage_pos] + percentage_string + progress_bar[percentage_pos + len(percentage_string):]
	return(progress_bar)

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)


async def limite_msg_db(text,username,bot):
	lim_ch = 890
	text = text.splitlines() 
	msg = ''
	msg_ult = '' 
	c = 0
	for l in text:
		if len(msg +"\n" + l) > lim_ch:		
			msg_ult = msg
			await bot.send_message(username,msg)	
			msg = ''
		if msg == '':	
			msg+= l
		else:		
			msg+= "\n" +l	
		c += 1
		if len(text) == c and msg_ult != msg:
				await bot.send_message(username,msg)

async def limite_msg(text,username,bot):
	lim_ch = 1500
	text = text.splitlines() 
	msg = ''
	msg_ult = '' 
	c = 0
	for l in text:
		if len(msg +"\n" + l) > lim_ch:		
			msg_ult = msg
			await bot.send_message(username,msg)	
			msg = ''
		if msg == '':	
			msg+= l
		else:		
			msg+= "\n" +l	
		c += 1
		if len(text) == c and msg_ult != msg:
			await bot.send_message(username,msg)

def filezip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+"zip"), mode="wb", volume=volume, ext_digits=0) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

def sevenzip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)
    fsize = fpath.stat().st_size
    if not volume:
        volume = fsize + 1024
    ext_digits = len(str(fsize // volume + 1))
    if ext_digits < 3:
        ext_digits = 3
    with MultiVolume(
        fpath.with_name(fpath.name+".7z"), mode="wb", volume=volume, ext_digits=ext_digits
    ) as archive:
        with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
            if password:
                archive_writer.set_encoded_header_mode(True)
                archive_writer.set_encrypted_header(True)
            archive_writer.write(fpath, fpath.name)
    files = []
    for file in archive._files:
        files.append(file.name)
    return files

async def ytdlp_downloader(url,usid,msg,username,callback,format,j):
	class YT_DLP_LOGGER(object):
		def debug(self,msg):
			pass
		def warning(self,msg):
			pass
		def error(self,msg):
			pass
	#j = 
	resolution = str(format)	
	dlp = {"logger":YT_DLP_LOGGER(),"progress_hooks":[callback],"outtmpl":f"./{j}%(title)s.%(ext)s","format":f"best[height<={resolution}]"}
	downloader = YoutubeDL(dlp)
	loop = asyncio.get_running_loop()
	filedata = await loop.run_in_executor(None,downloader.extract_info, url)
	filepath = downloader.prepare_filename(filedata)
	return filedata["requested_downloads"][0]["_filename"]	

class Progress(BufferedReader):
    def __init__(self, filename, read_callback):
        f = open(filename, "rb")
        self.filename = Path(filename).name
        self.__read_callback = read_callback
        super().__init__(raw=f)
        self.start = time()
        self.length = Path(filename).stat().st_size

    def read(self, size=None):
        calc_sz = size
        if not calc_sz:
            calc_sz = self.length - self.tell()
        self.__read_callback(self.tell(), self.length,self.start,self.filename)
        return super(Progress, self).read(size)

def get_webservice_token(host,username,password,proxy=None): 
	try:
		pproxy = proxy 
		webserviceurl = f'{host}login/token.php?service=moodle_mobile_app&username={username}&password={password}' 
		resp = requests.get(webserviceurl, proxies=pproxy,timeout=10) 
		data = json.loads(resp.text) 
		if data['token']!='': 
			print(data['token'])
			return data['token'] 
		return None 
	except: return None

def files_formatter(path,username):
	try:
		rut = str(path)
		filespath = Path(str(path))
		result = []
		dirc = []
		final = []
		for p in filespath.glob("*"):
			if p.is_file():
				result.append(str(Path(p).name))
			elif p.is_dir():
				dirc.append(str(Path(p).name))
		result.sort()
		dirc.sort()
		msg = f'𝑫𝒊𝒓𝒆𝒄𝒕𝒐𝒓𝒊𝒐 𝒂𝒄𝒕𝒖𝒂𝒍\n\n `{str(rut).split("downloads/")[-1]}`\n\n'
		if result == [] and dirc == [] :
			return msg , final
		for k in dirc:
			final.append(k)
		for l in result:
			final.append(l)
		i = 0
		for n in final:
			try:
				size = Path(str(path)+"/"+n).stat().st_size
			except: pass
			if not "." in n:
				msg+=f"`➣ {i} 📂 {n}`\n"
			else:
				msg+=f"`➣ {i} 📄 {n} `[ {sizeof_fmt(size)} ]\n"
			i+=1
		msg+= f"\n𝑬𝒍𝒊𝒎𝒊𝒏𝒂𝒓 𝒅𝒊𝒓𝒆𝒄𝒕𝒐𝒓𝒊𝒐 𝒓𝒂𝒊𝒛\n**/deleteall**"
		return msg , final
	except Exception as e:
		print(str(e))

def descomprimir(archivo,ruta):
	archivozip = archivo
	with ZipFile(file = archivozip, mode = "r", allowZip64 = True) as file:
		archivo = file.open(name = file.namelist()[0], mode = "r")
		archivo.close()
		guardar = ruta
		file.extractall(path = guardar)