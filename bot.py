from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery , ReplyKeyboardMarkup, ForceReply , InputMediaDocument , MessageEntity
from pyrogram import Client , filters 
from config import API_HASH,API_ID,BOT_TOKEN,ID_DB,ID_ACC,ID_DB_data,ID_DB_user,FILE_DB,MSG_LOG
import os
from os.path import exists
from time import localtime,sleep
from json import loads, dumps
from random import randint
from pathlib import Path
import aiohttp
import asyncio
from urllib.parse import unquote_plus
from time import time,sleep
import bs4
import uuid
import re
import urllib
import urllib.parse
import random
import threading
from io import BufferedReader
import mimetypes
import requests
import json
from tools.funciones import filezip,descomprimir,limite_msg,files_formatter,mediafiredownload, download_progres , downloadmessage_progres , sevenzip, uploadfile_progres , ytdlp_downloader
from clients.token import MoodleClient
import aiohttp_socks
from clients.draft import MoodleClient2
import shutil 
from bs4 import BeautifulSoup
from verify_user import VerifyUserData
from pyshortext import short
from xdlink import xdlink
from datetime import datetime
import base64

admins = ["Pro_Slayerr","raydel0307"]
Temp_dates = {}
DB_global = {}
Config_temp = {}

cancel_list = {}
download_list = {}

DB_accs = {'accesos':[]}
seg = 0
SCT = {}

bot = Client("bot",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)

nubes = {}
backup_file = "backup.json"
account_file = "account.json"
backup_interval = 3

def save_backup():
    global nubes
    while True:
        with open(backup_file, 'w') as f:
            json.dump(nubes, f)
        sleep(backup_interval)
def load_backup():
    with open(backup_file, 'r') as f:
        return json.load(f)
if exists(backup_file):
    nubes = load_backup()
    print("BACKUP IMPORTADO")
else:
    nubes = {}

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

async def send_db():
    datos = datetime.now()
    nueva_media = InputMediaDocument("usuarios.db",caption=str(datos))
    await bot.edit_message_media(chat_id=ID_DB,message_id=FILE_DB,media=nueva_media)
    return

async def save_logs(text):
    message = await bot.get_messages(ID_DB,message_ids=int(MSG_LOG))
    texto = message.text+"\n"+str(text)
    await message.edit(texto[-600:])
    return

async def file_renamer(file):
    filename = file.split("/")[-1]
    path = file.split(filename)[0]
    if len(filename)>21:
        p = filename[:10]
        f = filename[-11:]
        filex = p + f
    else:
         filex = filename
    filename = path + re.sub(r'[^A-Za-z0-9.]', '', filex)
    os.rename(file,filename)
    return filename

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)

@bot.on_message(filters.private)
async def start(client: Client, message: Message):
    async def worker(client: Client, message: Message):
        username = message.from_user.username
        user_id = message.from_user.id
        send = message.reply
        out_message = message.text
        fecha_actual = localtime().tm_mday
        
        #! Crear carpeta download si no existe
        if exists('downloads/'+str(username)+'/'):pass
        else:os.makedirs('downloads/'+str(username)+'/')
        try: Temp_dates[username]
        except: Temp_dates[username] = {'downlist' : [],'file':''}
        try: Config_temp[username]
        except: Config_temp[username] = {'host':'','user':'','passw':'','zips':5,'proxy_pv':'','proxy': True,'repo':5,'token':None}

        #await bot.edit_message_text(ID_DB,message_id=2,text=dumps(xd,indent=4))
        msg = await bot.get_messages(ID_DB,message_ids=ID_DB_data)
        DB_global.update(loads(msg.text))
        #msg_conf = await bot.get_messages(ID_ACC,message_ids=ID_DB_user)
        #DB_accs.update(loads(msg_conf.text))
        msg_conf = await bot.get_messages(ID_ACC,message_ids=ID_DB_user)
        DB_accs.update(loads(msg_conf.text))

        m = await bot.get_messages(ID_DB, message_ids=FILE_DB)
        try:
            os.unlink("usuarios.db")
        except:pass
        try:
            os.unlink("downloads/usuarios.db")
        except:pass
        p = 'downloads/uploads/'
        if not str(user_id) in nubes:
            nubes[str(user_id)] = []
        if not exists(p):
            os.makedirs(p)
        await m.download(file_name=f"usuarios.db")
        os.rename("downloads/usuarios.db","usuarios.db")

        if not DB_global['Estado_del_bot'] and username not in admins:
            await send('''**⏰BOT APAGADO⏰**

**⛔️Horario pico**
8:00PM a 12:00PM

**‼️Solo espere a que se encienda**''')
            return
        if username not in DB_accs['accesos']:
            await send('**⛔️No tienes acceso al BOT⛔️**')
            return

        if message.audio or message.document or message.animation or message.sticker or message.photo or message.video:
            if not username in download_list:
                download_list[username] = []

            download_list[username].append(message)
            msg = await bot.send_message(username,"𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")

            for i in download_list[username]:
                filesize = int(str(i).split('"file_size":')[1].split(",")[0])
                try:
                    filename = str(i).split('"file_name": ')[1].split(",")[0].replace('"',"")   
                except:
                    filename = str(randint(11111,999999))+".mp4"
                start = time()      
                await msg.edit(f"𝑷𝒓𝒆𝒑𝒂𝒓𝒂𝒏𝒅𝒐 𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂\n\n`{filename}`")
                if not os.path.exists(f'downloads/{username}/{filename}'):
                    try:
                        a = await i.download(file_name=f'downloads/{username}/{filename}',progress=downloadmessage_progres,progress_args=(filename,start,msg))
                        if Path(f'downloads/{username}/{filename}').stat().st_size == filesize:
                            await msg.edit("𝑫𝒆𝒔𝒄𝒂𝒓𝒈𝒂 𝒆𝒙𝒊𝒕𝒐𝒔𝒂")
                            download_list[username] = []
                            #Temp_dates[username]['file'] = f'downloads/{username}/{filename}'
                            path = f"downloads/{username}/"
                            msg = files_formatter(path,username)
                            await limite_msg(msg[0],username,bot)
                            #await uploads_options(f'downloads/{username}/{filename}',filesize,username)
                            return
                    except Exception as ex:
                        if "[400 MESSAGE_ID_INVALID]" in str(ex):
                            print("400")
                            await  bot.cancel_download(a)
                            download_list[username] = []
                            pass     
                        else:
                            print("Bad")
                            download_list[username] = []
                            await bot.send_message(username,ex) 
                            return
                else:
                    path = f"downloads/{username}/"
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                    return
        if out_message.startswith('/start'):
            button1 = InlineKeyboardButton("📝 Mi Plan ","plan")
            button2 = InlineKeyboardButton("👨🏻‍💻 Propietario",url = "https://t.me/Pro_Slayerr")
            button3 = InlineKeyboardButton("🗣 Soporte",url = "https://t.me/soportebota")
            buttons = [[button1,button2,button3]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await bot.send_photo(username,'start.jpg',reply_markup=reply_markup,caption='''Hola 👋🏻  Bienvenido, 
Bienvenido a este sistema de Descargas, estoy simpre para tí, y ayudarte a descagar cualquier archivo multimedia que desees☺️
Para empezar envié un archivo o enlaces para procesar(Youtube, Twich, mediafire entre otros soportes)''')
            return
        if out_message.startswith("/lsc"):
            files_cloud = ""
            current = 0
            for nub in nubes[str(user_id)]:
                files_cloud += f'➣ {current} 📄 `{nub["filename"]}`\n'
                current += 1
            if len(nubes[str(user_id)]) == 0:
                files_cloud += "\n"
            m = "**Archivos Subidos**\n\n"
            m+= files_cloud+"\n"
            await bot.send_message(user_id,m)

        elif out_message.startswith('/ls'):
            path = f"downloads/{username}/"
            msg = files_formatter(path,username)
            await limite_msg(msg[0],username,bot)
            return

        if out_message.startswith("/bitzero"):
            lista = out_message.split(' ')
            try:
                SCT["host"] = lista[1]
                SCT["user"] = lista[2]
                SCT["passw"] = lista[3]
                SCT["id"] = lista[4]
                SCT["zips"] = int(lista[5])
                SCT["mode"] = lista[6]
                await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            except:
                await bot.send_message(username,"Error en el comando\n/bitzero host user passw id zips mode")
                return

        if out_message.startswith('/c_uclv'):
            lista = out_message.split(' ')
            DB_global["UCLVC"] = {}
            DB_global["UCLVC"]["X"] = True
            DB_global["UCLVC"]["user"] = lista[1]
            DB_global["UCLVC"]["passw"] =  lista[2]
            DB_global["UCLVC"]["time"] = "2020-12-10 16:47:42.695000"
            DB_global["UCLVC"]["XZimbraCsrfToken"] = ""
            DB_global["UCLVC"]["cookies"] = {}
            await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            return

        if out_message.startswith("/my"):
            data = VerifyUserData().data_user(user_id)
            data = json.loads(data[2])
            msg = "📝 Datos:\n\n"
            msg+= f"📌 Plan: {data['plan']}"
            msg+= f"📌 Limite: {sizeof_fmt(data['limite'])}n"
            msg+= f"📌 Subido: {sizeof_fmt(data['total'])} GiB"
            await bot.send_message(username,msg)
            return

        if out_message.startswith('/files'):
            msg = await bot.send_message(username,"♠️ Buscando archivos")
            await webmailuclv_api('',user_id,msg,username,myfiles=True,deleteall=False)
            return

        if out_message.startswith('/clear'):
            msg = await bot.send_message(username,"♠️ Borrando Archivos")
            await webmailuclv_api('',user_id,msg,username,myfiles=True,deleteall=True)
            return

        if out_message.startswith('/up'):
            path = f"downloads/{username}/"
            if "_" in out_message:
                list = int(out_message.split("_")[1])
            else:
                list = out_message.split(" ")
            msgh = files_formatter(path,username)
            start = time()
            if len(list)==2:
                l = list[1]
                file = path+msgh[1][int(l)]
                filename = str(file).split("/")[-1]
                filesize = os.path.getsize(file)
                #msg = await bot.send_message(username,f"𝑺𝒆𝒍𝒆𝒄𝒄𝒊𝒐𝒏𝒂𝒅𝒐 **{filename}**")
                Temp_dates[username]['file'] = file
                await uploads_options(file,filesize,username)
            else:
                await bot.send_message(username,f"❌ **Error en el comando /up**\n**La forma correcta de usar /up 1 (o el número que corresponda a su archivo)**")
            return

        if out_message.startswith("/rename"):
            h = f"downloads/{username}/"
            lista = out_message.split(" ",2)
            name1 = int(lista[1])
            name2 = lista[2]
            msgh = files_formatter(h,username)
            actual = h+msgh[1][name1]
            shutil.move(actual,h+name2)
            await bot.send_message(username,f"𝑹𝒆𝒏𝒐𝒎𝒃𝒓𝒂𝒅𝒐 𝒄𝒐𝒓𝒓𝒆𝒄𝒕𝒂𝒎𝒆𝒏𝒕𝒆\n\n `{msgh[1][name1]}` ➥ `{name2}`")
            msg = files_formatter(h,username)
            await limite_msg(msg[0],username,bot)
            return

        if out_message.startswith("/deleteall"):
            path = f"downloads/{username}/"
            shutil.rmtree("downloads/"+username+"/")
            os.mkdir(f"downloads/{username}/")
            msg = files_formatter(path,username)
            await limite_msg(msg[0],username,bot)
            return

        if out_message.startswith("/mkdir"):
            name = out_message.split(" ")[1]
            if "." in name or "/" in name or "*" in name:
                await bot.send_message(username,"💢𝑬𝒍 𝒏𝒐𝒎𝒃𝒓𝒆 𝒏𝒐 𝒑𝒖𝒆𝒅𝒆 𝒄𝒐𝒏𝒕𝒆𝒏𝒆𝒓 . , * /")
                return
            rut = f"downloads/{username}/"
            os.mkdir(f"{rut}/{name}")
            await bot.send_message(username,f"𝙎𝙚 𝙘𝙧𝙚𝙤 𝙡𝙖 𝙘𝙖𝙧𝙥𝙚𝙩𝙖\n\n /{name}")
            msg = files_formatter(rut,username)
            await limite_msg(msg[0],username,bot)
            return

        if out_message.startswith("/rmdir"):
            path = f"downloads/{username}/"
            if "_" in out_message:
                list = out_message.split("_")[1]
            else:
                list = out_message.split(" ")[1] 
            filespath = Path(path)
            msgh = files_formatter(path,username)
            try:
                shutil.rmtree(path+msgh[1][int(list)])
                msg = files_formatter(path,username)
                await limite_msg(msg[0],username,bot)
            except Exception as ex:
                await bot.send_message(username,ex)
            return

        if out_message.startswith("/rmc"):
            try:
                host = SCT["host"]
                user = SCT["user"]
                passw = SCT["passw"]
                ids = SCT["id"]
            except:
                await bot.send_message(username,"Ingrese sus Datos")
                return
            text = out_message
            msg = await bot.send_message(username,f"[•] #rm #cloud #enproceso\n\n<code>Conectando nube...</code>")
            if "-" in text:
                lisc = list(range(int(text.split("-")[0].split(" ")[1]),int(text.split("-")[1].split(" ")[0])+1))
                text =  "/rmc "+' '.join(map(str,lisc))
            elif "all" in text:
                   text = "/rmc "+' '.join(map(str,list(range(0,len(nubes[str(user_id)])))))
            files = text.replace("/rmc ","").split(" ")
            menos = 0
            for f in files:
                try:
                    fids_split = nubes[str(user_id)][int(f)-menos]['token'].split("-")
                    total = len(fids_split)
                    current = 0
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"}
                    connector = aiohttp.TCPConnector(ssl=False)
                    async with aiohttp.ClientSession(connector=connector) as session:
                        async with session.get(host+"/login",headers=headers) as resp:
                            html = await resp.text()
                        token = BeautifulSoup(html,"html.parser").find('input',{'name':'csrfToken'})["value"]
                        login_data = {"password": passw,"remember": 1,"source": "","username": user,"csrfToken":token}
                        async with session.post(f"{host}/login/signIn", data=login_data, headers=headers) as resp:
                            print(0)
                        for t in fids_split:
                            await msg.edit(f"[•] #rm #cloud #enproceso\n\n<code>Eliminando {round((current/total)*100,1)}%</code>")
                            csrfToken = token
                            async with session.post(f"{host}/api/v1/submissions/{ids}/files/{t}?stageId=1",headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36","x-http-method-override": "DELETE","x-requested-with":"XMLHttpRequest","x-csrf-token":csrfToken}) as resp:
                                print(resp.status)
                            current += 1
                        nubes[str(user_id)].pop(int(f)-menos)
                        menos += 1
                        await msg.edit(f"[✓] #rm #cloud #finalizado\n\n<code>Eliminado</code>")
                except Exception as e:
                    print(e)
                    await msg.edit(f"[✓] #rm #cloud #error\n\n<code>Error desconocido</code>")

        elif out_message.startswith("/rm"):
            path = f"downloads/{username}/"
            if "_" in out_message:
                list = out_message.split("_")[1]
            else:
                list = out_message.split(" ")[1]
            msgh = files_formatter(path,username)
            if "-" in list:
                v1 = int(list.split("-")[-2])
                v2 = int(list.split("-")[-1])
                for i in range(v1,v2+1):
                    try:
                        os.unlink(path+msgh[1][i])
                    except Exception as ex:
                        await bot.send_message(username,ex)
                msg = files_formatter(path,username)
                await limite_msg(msg[0],username,bot)
            else:
                try:
                    os.unlink(path+msgh[1][int(list)])
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                except Exception as ex:
                    await bot.send_message(username,ex)
            return

        if out_message.startswith("/unzip"):
            path = f"downloads/{username}/"
            archivo = out_message.split(" ")[1]
            ruta = path
            msgh = files_formatter(path,username)
            archivor = path+msgh[1][int(archivo)]
            a = await bot.send_message(username,"𝑫𝒆𝒔𝒄𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐 𝒂𝒓𝒄𝒉𝒊𝒗𝒐")
            try:
                descomprimir(archivor,ruta)
                await a.edit("𝑨𝒓𝒄𝒉𝒊𝒗𝒐 𝒅𝒆𝒔𝒄𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒅𝒐")
                msg = files_formatter(path,username)
                await limite_msg(msg[0],username,bot)
                return
            except Exception as ex:
                await a.edit("Error: ",ex)
                return

        if out_message.startswith("/seven"):
            path = f"downloads/{username}/"
            if "_" in out_message:
                lista = out_message.split("_")
            else:
                lista = out_message.split(" ")
            msgh = files_formatter(path,username)
            if len(lista) == 2:
                i = int(lista[1])
                j = str(msgh[1][i])
                if not "." in j:
                    h = await bot.send_message(username,"𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
                    g = path+msgh[1][i]
                    p = shutil.make_archive(j, format = "zip", root_dir=g)
                    await h.delete()
                    shutil.move(p,path)    
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                    return
                else:
                    g = path+msgh[1][i]
                    o = await bot.send_message(username,"𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
                    a = filezip(g,volume=None)
                    await o.delete()
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                    return

            elif len(lista) == 3:
                i = int(lista[1])
                j = str(msgh[1][i])
                t = int(lista[2])
                g = path+msgh[1][i]
                h = await bot.send_message(username,"𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐")
                if not "." in j:
                    p = shutil.make_archive(j, format = "zip", root_dir=g)
                    await h.edit("𝑫𝒊𝒗𝒊𝒅𝒊𝒆𝒏𝒅𝒐 𝒆𝒏 𝒑𝒂𝒓𝒕𝒆𝒔")
                    a = sevenzip(p,password=None,volume = t*1024*1024)
                    os.remove(p)
                    for i in a :
                        shutil.move(i,path)
                    await h.edit("𝑪𝒐𝒎𝒑𝒓𝒆𝒔𝒊𝒐𝒏 𝒓𝒆𝒂𝒍𝒊𝒛𝒂𝒅𝒂")
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                    return
                else:
                    a = sevenzip(g,password=None,volume = t*1024*1024)
                    await h.edit("𝑪𝒐𝒎𝒑𝒓𝒆𝒔𝒊𝒐𝒏 𝒓𝒆𝒂𝒍𝒊𝒛𝒂𝒅𝒂")
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                    return

        if out_message.startswith('http'):
            msg = await send('**Preparando descarga**')
            url = out_message
            if "youtu.be/" in out_message or "youtube.com/" in out_message or "twitch.tv/" in out_message:
                Temp_dates[username]['streaming_list'] = url
                await msg.edit(f"`💻 Elija una de las calidades disponibles`",reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("360p","360")], 
                    [InlineKeyboardButton("480p","480")],
                    [InlineKeyboardButton("720p","720")],
                    [InlineKeyboardButton("1080p","1080")]
                    ]))
                return
            
            elif "mediafire.com" in out_message:
                session = aiohttp.ClientSession()
                page = bs4.BeautifulSoup(requests.get(url).content, 'lxml')
                info = page.find('a', {'aria-label': 'Download file'})
                url = info.get('href') 
                download = await session.get(url,timeout=aiohttp.ClientTimeout(total=1800)) 
                file_size = int(download.headers.get("Content-Length")) 
                file_name = download.headers.get("Content-Disposition").split("filename=")[1]
                downloaded = 0
                file_path = f"downloads/{username}/{file_name}"
                start = time()
                did = str(randint(1000,99999))
                print(did)
                cancel_list[did]==True
                await asyncio.sleep(1)
                with open(file_path,"wb") as file:
                    while True:
                        if cancel_list[did]==True:
                            chunk = await download.content.read(1024*1024)
                            downloaded+=len(chunk)
                            if not chunk:
                                break
                            await mediafiredownload(downloaded,file_size,file_name,start,msg,did)
                            file.write(chunk)
                        else:
                            try:
                                os.unlink(file)
                            except:pass
                            return
                    file.close()
                Temp_dates[username]['file'] = f'downloads/{username}/{file_name}'
                await msg.delete()
                await uploads_options(file_name,file_size,username)
                return
            
            else:
                timeout = aiohttp.ClientTimeout(total=60 * 60)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.get(url,ssl=False,timeout=timeout) as r:
                        try:filename = unquote_plus(url.split("/")[-1])
                        except:filename = r.content_disposition.filename	
                        if "?" in filename:filename = filename.split("?")[0]
                        fsize = int(r.headers.get("Content-Length"))
                        file_path = f"downloads/{username}/{filename}"
                        did = str(randint(10000,999999))
                        cancel_list[did] = True
                        f = open(file_path,"wb")
                        newchunk = 0
                        start = time()
                        await asyncio.sleep(1)
                        async for chunk in r.content.iter_chunked(1024*1024):
                            if cancel_list[did]:
                                newchunk+=len(chunk)
                                await mediafiredownload(newchunk,fsize,filename,start,msg,did)
                                f.write(chunk)
                            else:
                                try:
                                    os.unlink(f)
                                except:pass
                                return
                        f.close()
                    Temp_dates[username]['file'] = f'downloads/{username}/{filename}'
                    await msg.delete()
                    await uploads_options(filename,fsize,username)
                    return
        
        if out_message.startswith('/private_set'):
            lista = out_message.split(' ')
            if lista[1]=="p":
	            Config_temp[username]['host'] = lista[2]
	            Config_temp[username]['user'] = lista[3]
	            Config_temp[username]['passw'] = lista[4]
	            Config_temp[username]['repo'] = lista[5]
	            Config_temp[username]["token"] = None
            elif lista[1]=="t":
            	Config_temp[username]["host"] = lista[2] 
            	Config_temp[username]["token"] = lista[3]
            elif lista[1]!="t" or lista[1]!="l":
            	await send('Comado incorrecto, debe ser utilizado asi:\n\n/private_set p host user passw repo\n/private_set t host token')
            	return
            await send('**Operacion realizada**')
            return       
        
        if out_message.startswith('/private_proxy'):
            proxy = out_message.split(' ')[1]
            Config_temp[username]['proxy'] = proxy
            await send('**Operacion realizada**')
            return

        if out_message.startswith('/zips'):
            zips = out_message.split(' ')[1]
            Config_temp[username]['zips'] = zips
            await send('**Operacion realizada**')
            return

        #Admins 
        if out_message.startswith('/status_bot') and username in admins:  #ok
            DB_global['Estado_del_bot'] = False if DB_global['Estado_del_bot'] else True
            await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            await send('**Operacion realizada**')
            return

        if out_message.startswith('/status_uclv') and username in admins: #ok
            print(DB_global['Estado_de_uclv'])
            DB_global['Estado_de_uclv'] = False if DB_global['Estado_de_uclv'] else True
            await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            await send('**Operacion realizada**')
            return

        if out_message.startswith('/set') and username in admins:
            clouds = ['GTM', 'UCM','UCCFD','VCL','UCLV','LTU','EDUVI','GRM,AULAENSAP, EDICIONES']
            lista = out_message.split(' ')
            if len(lista) == 3:
                Nube = lista[1] 
                Token = lista[2]
                mode = 'token'
            elif len(lista) == 4:
                Nube = lista[1] 
                Username =  lista[2]
                Passw = lista[3]  
                mode = 'login'
            else:
                await send('Configuracion incorrecta')
                return    
            if Nube in clouds:
                if mode == 'token': DB_global[Nube]['token'] = Token
                else: 
                    DB_global[Nube]['username'] = Username
                    DB_global[Nube]['pass'] = Passw
                
                await send('Operacion realizada')
                await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            else: await send('Esta nube no existe');return

        if out_message.startswith('/add') and username in admins:
            d = out_message.split(" ")
            if len(d)==2:
                msg = f"🗣 Elige un plan para `@{d[1]}`\n"
                button1 = InlineKeyboardButton("🌀 Básico",f"add {d[1]} b")
                button2 = InlineKeyboardButton("🌀 Estándar",f"add {d[1]} e")
                button3 = InlineKeyboardButton("🌀 Avanzado",f"add {d[1]} a")
                button4 = InlineKeyboardButton("🌀 Premium",f"add {d[1]} p")
                button5 = InlineKeyboardButton("⚜️ NUBE UO ⚜️",f"add {d[1]} uo")
                button6 = InlineKeyboardButton("⚜️ NUBE UCLV ⚜️",f"add {d[1]} uclv")
                buttons = [[button1,button2],[button3,button4],[button5],[button6]]
                reply_markup = InlineKeyboardMarkup(buttons)
                await bot.send_message(username,msg,reply_markup=reply_markup)
            return
        if out_message.startswith('/vip') and username in admins:
            planes = {"b":"basico","e":"estandar","a":"avanzado","p":"premium"}
            d = out_message.split(" ")
            if len(d)==3:
                uname = d[1]
                pl = d[2]
                user = await bot.get_chat(uname)
                usid = user.id
                if pl=="r":
                    VerifyUserData().delete_user(usid)
                    await bot.send_message(username,f"**@{uname} Deleted**")
                    await bot.send_message(uname,f"**@{uname} Deleted**")
                v = VerifyUserData().verify_already_exists(usid)
                if v:
                    await bot.send_message(username,"Este usuario ya es vip")
                    return
                if pl in planes:
                    plan = planes[pl]
                    v = VerifyUserData().agg_new_user(usid,plan)
                    await bot.send_message(username,f"**Plan {plan} activado @{uname}**")
                    await bot.send_message(uname,f"**Plan {plan} activado @{uname}**")
            DB_accs['accesos'].append(uname)
            await bot.edit_message_text(ID_ACC,message_id=ID_DB_user,text=dumps(DB_accs,indent=4))
            return

        if out_message.startswith('/ban') and username in admins: #ok
            lista = out_message.split(' ')
            if username==admins:
                await bot.send_message(username,"😂 No te puedes dar ban so mongólico")
                return
            DB_accs['accesos'].remove(lista[1])
            await bot.edit_message_text(ID_ACC,message_id=ID_DB_user,text=dumps(DB_accs,indent=4))
            user = await bot.get_chat(lista[1])
            usid = user.id
            v = VerifyUserData().verify_already_exists(usid)
            if v:
                VerifyUserData().delete_user(usid)
                await send_db()
            await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            return

        if out_message.startswith('/proxy_global') and username in admins:
            proxy = out_message.split(' ')[1]
            DB_global['Proxy_Global'] = proxy
            try:
                await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            except:
                await send('**Failed: está ingresando el mismo proxy**')
            await send('**Operacion realizada**')
            return

    bot.loop.create_task(worker(client, message))

def split_file(file_path: Path, split_size: int, username : str) :#-> list[str]:
    files = []
    part_number = 0
    with open(file_path, "rb") as file:
        while (data := file.read(split_size)):
            name = f"{file_path.name}-{part_number}.zip"
            with open('downloads/' + username + '/' + name, "wb") as writer:
                writer.write(data)
            part_number += 1
            files.append(f"downloads/{username}/{name}")
    return files


async def get_():
    resp = requests.post("http://apiserver.alwaysdata.net/session",json={"type":"uo","id":"7002"},headers={'Content-Type':'application/json'})
    return resp.text

def generate():
    prefix = "web-file-upload-"
    random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))
    unique_id = str(uuid.uuid4().time_low)

    random_name = f"{prefix}{random_string}-{unique_id}"
    return random_name

async def bitzero_uploader(file,usid,msg,username):
    try:
        host = SCT["host"]
        user = SCT["user"]
        passw = SCT["passw"]
        ids = SCT["id"]
        zips = SCT["zips"]
        mode = SCT["mode"]
        zipssize=int(zips)*1024*1024
        filename = file.split("/")[-1]
        filesize = Path(file).stat().st_size
        proxy = None
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
        #login
        msg = await msg.edit("🔴 Conectando ... 🔴")
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(host+"/login",headers=headers) as resp:
                html = await resp.text()
            soup = BeautifulSoup(html,"html.parser")
            csrftoken = soup.find('input',{'name':'csrfToken'})["value"]
            payload = {"password": passw,"remember": 1,"source": "","username": user,"csrfToken":csrftoken}
            async with session.post(f"{host}/login/signIn", data=payload, headers=headers) as resp:
                print(222)
            #upload
            if filesize-1048>zipssize:
                parts = round(filesize / zipssize)
                await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐\n\n🏷 Total: {parts} partes\n")
                files = sevenzip(file,volume=zipssize)
            else:
                files = [file]
            print(24)
            links = []
            token = ""
            for file in files:
                filename = file.split("/")[-1]
                try:
                    if mode=="1":
                        spypng = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf6\x178U\x00\x00\x00\x00IEND\xaeB`\x82'
                        path = f"downloads/{username}/{filename}_#{usid}@bitzero.png"
                        with open(path,"wb") as nref:
                            nref.write(spypng+open(file,"rb").read())
                    elif mode=="2":
                        path = file
                        spypng = '<!DOCTYPE html>\n<html lang="es">\n<bytes>'
                        spypng2 = '</bytes></html>'
                        with open(path, 'rb') as file:
                            bytes_data = file.read()
                        base64_data = base64.b64encode(bytes_data).decode('utf-8')
                        open(path+f"_#{usid}@bitzero.html","w").write(spypng+base64_data+spypng2)
                        os.unlink(path)
                        path = path+f"_#{usid}@bitzero.html"
                        filename = path.split("/")[-1]
                    try:os.unlink(file)
                    except:pass
                    fi = Progress(path,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,path,msg))
                    post_file_url = f"{host}/api/v1/submissions/{ids}/files"
                    payload = {
                        "fileStage": "2",
                        "name[es_ES]": path,
                        "name[en_US]": path
                    }
                    query = {"file":fi,**payload}
                    headers["X-Csrf-Token"] = csrftoken
                    async with session.post(post_file_url,data=query,headers=headers) as resp:
                        html = await resp.text()
                    data = json.loads(html)
                    try:token+= f'{data["id"]}-'
                    except:await msg.edit(f"Archivo no subido ... {str(e)}")
                except Exception as e:
                    await bot.send_message(username,str(e))
            token+= "/"
            token = token.replace("-/","")
            key = ""
            key+= base64.b64encode(host.encode("utf-8")).decode("utf-8").replace("==","@").replace("=","#")+"-"
            key+= base64.b64encode(user.encode("utf-8")).decode("utf-8").replace("==","@").replace("=","#")+"-"
            key+= base64.b64encode(passw.encode("utf-8")).decode("utf-8").replace("==","@").replace("=","#")+"-"
            key+= base64.b64encode(str(ids).encode("utf-8")).decode("utf-8").replace("==","@").replace("=","#")
            nubes[str(usid)].append({"filename":filename,"token":token, "size":filesize})
            await bot.send_message(username,f"[✓] #upload #local #finalizado\n\n<code>Subido a la nube!\n\n{filename}</code>\n\n<b>Comando: </b><code>bitzero https://bitzero.techdev.cu/{filesize}-{ids}/{token}/{mode}/{key}/{urllib.parse.quote(filename.replace(' ','_'))}</code>")
            await msg.edit(f"✅ Finalizado ✅")
    except Exception as e:
        print(str(e))

async def webdav(file,usid,msg,username):
    try:
        host = "https://nube.uo.edu.cu/"
        proxy = aiohttp.TCPConnector()
        file = await file_renamer(file)
        filename = file.split("/")[-1]
        filesize = Path(file).stat().st_size
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
        async with aiohttp.ClientSession(connector=proxy) as session:
            await msg.edit(f"Conectando 🔴...")
            html = await get_()
            try:data = json.loads(html)
            except:
                await msg.edit("Datos no válidos o servidor deshabilitado [...]")
                return
            ids = data["nc_username"]
            session.cookie_jar.update_cookies(data)
            async with session.get(host+"index.php/apps/files/") as resp:
                html = await resp.text()
            soup = BeautifulSoup(html,'html.parser')
            requesttoken = soup.find('head')['data-requesttoken']
            webdav_url = host+"remote.php/dav/uploads/"+ids+"/"+ generate()
            try:
                async with session.request("MKCOL", webdav_url,headers={"requesttoken":requesttoken,**headers}) as resp:
                    print("MKCOL "+str(resp.status))
            except:
                await msg.edit("Este servidor está temporalmente fuera de servicio [await_please]")
                return
            mime_type, _ = mimetypes.guess_type(file)
            if not mime_type:
                mime_type = "application/x-7z-compressed"
            complete = True
            await msg.edit(f"⬆️ Uploading 0 de {sizeof_fmt(filesize)}")
            with open(file, 'rb') as f:
                offset = 0
                vchunk = 10
                while True:
                    file_chunk = f.read(vchunk*1024*1024)
                    if not file_chunk:
                        break
                    async with session.put(f"{webdav_url}/{offset}",data=file_chunk,headers={'Content-Type': mime_type,"requesttoken":requesttoken}) as resp:
                        try:
                            await msg.edit(f"⬆️ Uploading {sizeof_fmt(offset)} de {sizeof_fmt(filesize)}")
                        except:pass
                    offset+= len(file_chunk)
                u = webdav_url+"/{11}/"+str(filesize)+"/"+filename
                await msg.edit(f"📂  [{filename}]({u})\n❄️ **Tamaño:** {sizeof_fmt(filesize)}")
                complete = False
    except Exception as ex:
        print(str(ex))

@bot.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    username = callback_query.from_user.username
    user_id = callback_query.from_user.id
    input_mensaje: str = str(callback_query.data)
    
    if input_mensaje=="plan":
        try:
            msg = callback_query.message
            await msg.delete()
            data = VerifyUserData().data_user(user_id)
            data = json.loads(data[2])
            msg = "📝 Datos:\n\n"
            msg+= f"📌 Plan: {data['plan']}\n"
            msg+= f"📌 Limite: {data['limite']} GiB\n"
            msg+= f"📌 Subido: {data['total']} GiB"
            await bot.send_message(username,msg)
        except Exception as e:
            await bot.send_message(username,f"🔥Elige tu Plan🔥\n\n➡️ Plan Básico:\n💎15 GB de transferencia diaria\n📱 110 CUP\n\n➡️ Plan Estándar:\n💎25 GB de transferencia diaria\n📱 170 CUP\n\n➡️ Plan Avanzado:\n💎50 GB de transferencia diaria\n📱 250 CUP\n\n➡️Plan Premium:\n💎100 GB de transferencia diaria\n📱 280 CUP\n\n➡️Plan UCLV:\n💎20 GB  de trasferencia diaria\n📲250 CUP")
            await save_logs(e)
        return
    if "add" in input_mensaje:
        message = callback_query.message
        await message.delete()
        planes = {"b":"basico","e":"estandar","a":"avanzado","p":"premium","uo":"uo","uclv":"uclv"}
        d = input_mensaje.split(" ")
        uname = d[1]
        pl = d[2]
        user = await bot.get_chat(uname)
        usid = user.id
        v = VerifyUserData().verify_already_exists(usid)
        if v:
            await bot.send_message(username,f"**No se puede agregar, @{user.username} ya es vip**")
            return
        if pl in planes:
            plan = planes[pl]
            v = VerifyUserData().agg_new_user(usid,plan)
            await send_db()
            await bot.send_message(username,f"**Plan {plan} activado @{uname}**")
            await bot.send_message(uname,f"**Plan `{plan}` activado**")
        if not uname in DB_accs['accesos']:
            DB_accs['accesos'].append(uname)
            await bot.edit_message_text(ID_ACC,message_id=ID_DB_user,text=dumps(DB_accs,indent=4))
        return
    if "ccancel" in input_mensaje:
        did = input_mensaje.split(" ")[1]
        cancel_list[did] = False
        msg = callback_query.message
        await msg.edit("❌ **𝐃𝐞𝐬𝐜𝐚𝐫𝐠𝐚 𝐂𝐚𝐧𝐜𝐞𝐥𝐚𝐝𝐚** ❌")
        cancel_list.pop(did)
        return
    if "fcancel" in input_mensaje:
        download_list[username] = []
        await callback_query.message.delete()
        await bot.send_message(username,"❌ **𝐃𝐞𝐬𝐜𝐚𝐫𝐠𝐚 𝐂𝐚𝐧𝐜𝐞𝐥𝐚𝐝𝐚** ❌")
        return
    if input_mensaje == "144" or input_mensaje == "240" or input_mensaje == "360"  or input_mensaje == "480"  or input_mensaje == "720" or input_mensaje == "1080":
        msg = callback_query.message
        url = Temp_dates[username]['streaming_list']
        await msg.delete()
        msg = await client.send_message(username,"__Descargando__")
        download = await ytdlp_downloader(url,user_id,msg,username,lambda data: download_progres(data,msg,input_mensaje),input_mensaje,f'downloads/{username}/')
        size = os.path.getsize(download)
        await msg.delete()
        Temp_dates[username]['streaming_list'] = ''
        Temp_dates[username]['file'] = download
        await uploads_options('Youtube Video',size,username)
        return  
    
    clouds = ['GTM', 'UCM','UCCFD','VCL','UCLV','LTU','EDUVI','Privada','GRM', 'TESISLS','REVISTAS.UDG', 'EVEAUH', 'AULAENSAP', 'MEDISUR', 'EDICIONES','UCLVC',"UO","BitZero"]
    token_u = ['GTM', 'UCM','UCCFD','VCL','UCLV','LTU','GRM','EVEAUH']
    login = ['EDUVI','Privada','AULAENSAP','EVEAUH', 'EDICIONES']
    
    if input_mensaje in clouds:
        if input_mensaje == 'UCLV' and not DB_global['Estado_de_uclv']:
            await bot.send_message(username,'''**⛔️Moodle Uclv apagada⛔️**

**Horario:**
🟢 12:00AM
🔴 6:00AM

**✅ La Uclv solo trabajara 6 horas por motivos de precaución**''')
            return
        
        await callback_query.message.delete()
        msg = await bot.send_message(username,"𝑹𝒆𝒄𝒐𝒑𝒊𝒍𝒂𝒏𝒅𝒐 𝒊𝒏𝒇𝒐𝒓𝒎𝒂𝒄𝒊ó𝒏")
        filename = Path(Temp_dates[username]['file']).name
        filesize = Path(Temp_dates[username]['file']).stat().st_size
        up_mode = "zips"
        if VerifyUserData().verify_already_exists(user_id):
            d = VerifyUserData().data_user(user_id)
            d = json.loads(d[2])
            if (d['total']+filesize)>d['limite']:
                await msg.edit("🚷 **Este archivo sobrepasa el limite permitido** 🚷")
                return
            else:
                d['total']+=filesize
                VerifyUserData().update_user(user_id,d)
                await send_db()
                if input_mensaje == "TESISLS":
                    await tesisld_api(Temp_dates[username]['file'],user_id,msg,username)
                    return
                if input_mensaje == "UO":
                    await webdav(Temp_dates[username]['file'],user_id,msg,username)
                    return
                if input_mensaje == "BitZero":
                    if not "host" in SCT:
                        await msg.edit("Ingrese las credenciales")
                    else:
                        await bitzero_uploader(Temp_dates[username]['file'],user_id,msg,username)
                    return
                if input_mensaje == "UCLVC":
                    if d["plan"]!="uclv":
                        await msg.edit("💢 No puede usar este Servidor 💢\n\n🗣 Disponible con el plan Nube UCLV")
                        return
                    else:
                        await webmailuclv_api(Temp_dates[username]['file'],user_id,msg,username)
                        return
                if input_mensaje == "EVEAUH":
                    Config_temp[username]['host'] = "https://evea.uh.cu/"
                    Config_temp[username]['user'] = "alanis.dfelix1@estudiantes.fq.uh.cu"
                    Config_temp[username]['passw'] = "Petardo#6"
                    Config_temp[username]['repo'] = "4"
                    Config_temp[username]['zips'] = 100
                    Config_temp[username]["token"] = None
                    input_mensaje = "Privada"
                    up_mode = "chunk"
                if input_mensaje == "REVISTAS.UDG":
                    await rudg_api(Temp_dates[username]['file'],user_id,msg,username)
                    return  
                if input_mensaje == "MEDISUR":
                    await medisur_api(Temp_dates[username]['file'],user_id,msg,username)
                    return
                if input_mensaje == 'Privada':
                    zipssize = 1024*1024*int(Config_temp[username]['zips'])
                else:
                    zipssize = 1024*1024*int(DB_global[input_mensaje]['zips'])

                pv_proxy = Config_temp[username]['proxy_pv']
                proxy = DB_global['Proxy_Global']
                active_proxy = Config_temp[username]['proxy']
                
                if not active_proxy :
                    connector = aiohttp.TCPConnector()
                    pprx = None
                else:
                    if pv_proxy != '':
                        connector = aiohttp_socks.ProxyConnector.from_url(f"{pv_proxy}")
                        pprx = pv_proxy
                    else:
                        connector = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
                        pprx = proxy
                #pprx = DB_global['Proxy_Global']
                #connector = aiohttp_socks.ProxyConnector.from_url(f"{pprx}")
                print("Proxy_Global")
                if filesize-1048>zipssize:
                    if up_mode=="zips":
                        await msg.edit(f"📦 **Comprimiendo en zips**")
                        files = await bot.loop.run_in_executor(None, sevenzip, Temp_dates[username]['file'], None, zipssize)
                    else:
                        await msg.edit(f"📦 **Haciendo Chunks sea paciente**")
                        files = await bot.loop.run_in_executor(None, split_file , Path(Temp_dates[username]['file']), zipssize, username)
                else:
                    files = []
                    files.append(Temp_dates[username]['file'])  

                logslinks = []

                for path in files:
                    filenamex = Path(path).name
                    logerrors = 0
                    while logerrors < 5:
                        try:
                            if input_mensaje in token_u:
                                if Config_temp[username]["token"]:
                                    print("funcion activada")
                                    token = Config_temp[username]["token"]
                                    host = Config_temp[username]["host"]
                                    client = MoodleClient('x','x',host,connector)
                                else:
                                    print(DB_global[input_mensaje])
                                    client = MoodleClient('x','x',DB_global[input_mensaje]['url'],connector)
                                    token = DB_global[input_mensaje]['token']
                                upload = await client.uploadtoken(path,lambda chunk,total,start,filen: uploadfile_progres(chunk,total,start,filen,msg),token)
                                if upload == False:
                                    logerrors += 1
                                    continue
                                else:
                                    upload = upload['calendario']
                                    logslinks.append(upload)
                                    if Config_temp[username]["host"]=="https://moodle.uclv.edu.cu/":
                                        await bot.send_message(username,f'[{filenamex}]({upload})')
                                    elif input_mensaje == 'UCLV':
                                        await bot.send_message(username,f'[{filenamex}]({upload})')
                                    break
                            if input_mensaje in login:
                                if not Config_temp[username]["token"]:
                                    print("funcion desactivada")
                                    if input_mensaje == 'Privada':
                                        host = Config_temp[username]['host']
                                        user = Config_temp[username]['user']
                                        password = Config_temp[username]['passw']
                                        repoid = Config_temp[username]['repo']
                                    else:
                                        host = DB_global[input_mensaje]['url']
                                        user = DB_global[input_mensaje]['username']
                                        password = DB_global[input_mensaje]['pass']
                                        repoid = DB_global[input_mensaje]['repo']
                                    client = MoodleClient2(host,user,password,repoid,pprx)
                                    upload = await client.LoginUpload(path,lambda chunk,total,start,filen: uploadfile_progres(chunk,total,start,filen,msg))
                                    if upload == False:
                                        logerrors += 1
                                        continue
                                    else:
                                        logslinks.append(upload)
                                        if up_mode == "zips":
                                            await bot.send_message(username,f'[{filenamex}]({upload})')
                                        break
                        except Exception as ex:
                            await bot.send_message(username,str(ex))
                            return
                        
                if len(files) == len(logslinks):
                    with open(filename+".txt","w") as f:
                        message = ""
                        for li in logslinks:
                            message+=li+"\n"
                        if up_mode=="zips":
                            f.write(message)
                        else:
                            dictt = {"h":short(Config_temp[username]['host']),"urls":short(message),"fn":filename,"fs":filesize,"u":short(Config_temp[username]['user']),"p":short(Config_temp[username]['passw'])}
                            await msg.edit('**Finalizado correctamente**')
                            await bot.send_message(username,f"`{json.dumps(dictt)}`")
                            return
                    await bot.send_document(username,filename+".txt",thumb="thumb.jpg")
                    await msg.edit('**Finalizado correctamente**')
                    os.unlink(filename+".txt")
                else:
                    await msg.edit('**Ha ocurrido un error**')
                shutil.rmtree(f'downloads/{username}')
                return

def uploadfile_progres(chunk,filesize,start,filename,message):
    try:
        now = time()
        diff = now - start
        mbs = chunk / diff
        msg = f"✴️ 𝐍𝐚𝐦𝐞: {filename}\n\n"
        try:
            msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
        except:pass
        msg+= f"🔷 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐: {sizeof_fmt(chunk)} of {sizeof_fmt(filesize)}\n\n"
        global seg
        if seg != localtime().tm_sec:
            message.edit(msg)
        seg = localtime().tm_sec
    except Exception as e:
        print(str(e))

async def medisur_api(file,usid,msg,username):
	try:
		zipssize=19*1024*1024
		filename = file.split("/")[-1]
		host = "https://medisur.sld.cu/index.php/medisur/"
		filesize = Path(file).stat().st_size
		print(21)
		proxy = None #Configs[username]["gp"]
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
		#login
		msg = await msg.edit("🔴 Conectando ... 🔴")
		connector = aiohttp.TCPConnector()
		async with aiohttp.ClientSession(connector=connector) as session:
			payload = payload = {}
			payload["source"] = "/index.php/medisur/user/profile"
			payload["username"] = "daironvf"
			payload["password"] = "Dairon2005#"
			async with session.post(host+"login/signIn", data=payload) as e:
				print(222)
			#upload
			if filesize-1048>zipssize:
				parts = round(filesize / zipssize)
				await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐\n\n🏷 Total: {parts} partes\n")
				files = sevenzip(file,volume=zipssize)
				print(24)
				links = []
				for file in files:
					try:
						#editar
						async with session.get(host+"author/submit") as resp:
							print(1)
						async with session.get(host+"author/submit/1") as resp:
							print(2)
						payload = {
							"submissionChecklist": "1",
							"sectionId": "17",
							"locale": "es_ES",
							"checklist[]": [
								"0",
								"1",
								"2",
								"3",
								"4",
								"5"
							],
							"copyrightNoticeAgree": "1",
							"commentsToEditor": ""
						}
						async with session.post(host+"author/saveSubmit/1",data=payload) as resp:
							print(3)
							ids = str(resp.url).split("Id=")[1]
						mime_type, _ = mimetypes.guess_type(file)
						if not mime_type:
							mime_type = "application/x-7z-compressed"

						upload_data = {}
						upload_data["articleId"] = ids
						upload_data["uploadSubmissionFile"] = "Cargar"

						post_file_url = host+"author/saveSubmit/2"
						fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
						query = {"submissionFile":fi,**upload_data}
						async with session.post(post_file_url,data=query) as resp:
							text = await resp.text()
							url = str(text).split('"controls"><a href="')[1].split('">')[0]
							await bot.send_message(username,url)
							links.append(url)
					except:
						pass
				await msg.edit(f"✅ Finalizado ✅ \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
				txtname = file.split('.')[0].replace(' ','_')+'.txt'
				with open(txtname,"w") as t:
					message = ""
					for li in links:
						message+=li+"\n"
					t.write(message)
					t.close()
				await bot.send_document(usid,txtname,thumb="thumb.jpg")
			else:
				await msg.edit("💠 Subiendo 💠")
				async with session.get(host+"author/submit") as resp:
					print(1)
				async with session.get(host+"author/submit/1") as resp:
					print(2)
				payload = {
					"submissionChecklist": "1",
					"sectionId": "17",
					"locale": "es_ES",
					"checklist[]": [
						"0",
						"1",
						"2",
						"3",
						"4",
						"5"
					],
					"copyrightNoticeAgree": "1",
					"commentsToEditor": ""
				}
				async with session.post(host+"author/saveSubmit/1",data=payload) as resp:
					print(3)
					ids = str(resp.url).split("Id=")[1]
				mime_type, _ = mimetypes.guess_type(file)
				if not mime_type:
					mime_type = "application/x-7z-compressed"

				upload_data = {}
				upload_data["articleId"] = ids
				upload_data["uploadSubmissionFile"] = "Cargar"

				post_file_url = host+"author/saveSubmit/2"
				fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
				query = {"submissionFile":fi,**upload_data}
				async with session.post(post_file_url,data=query) as resp:
					text = await resp.text()
					url = str(text).split('"controls"><a href="')[1].split('">')[0]
					await bot.send_message(username,url)
					await msg.edit(f"✅ Finalizado ✅ \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
					txtname = file.split('.')[0].replace(' ','_')+'.txt'
					with open(txtname,"w") as t:
						t.write(url)
						t.close()
					await bot.send_document(usid,txtname,thumb="thumb.jpg")
	except Exception as e:
		print(str(e))

async def webmailuclv_api(file,usid,msg,username,myfiles=False,deleteall=False):
    try:
        await save_logs("webmailuclv_api")
        await msg.edit("📡 **Buscando Servidor ...**")
        try:
            timer = DB_global["UCLVC"]["time"]
            user = DB_global["UCLVC"]["user"]
            passw = DB_global["UCLVC"]["passw"]
        except:
            await msg.edit("‼️ Ingrese las credenciales mediante /c_uclv")
            return
        await save_logs("timer: "+timer)
        expiration_date = datetime.strptime(timer, "%Y-%m-%d %H:%M:%S.%f")
        current_date = datetime.now()
        connector = aiohttp.TCPConnector()
        host = "https://correo.uclv.edu.cu/"
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0","Upgrade-Insecure-Requests":"1"}
        async with aiohttp.ClientSession(connector=connector) as session:
            if current_date < expiration_date:
                session.cookie_jar.update_cookies(DB_global["UCLVC"]["cookies"])
                XZimbraCsrfToken = DB_global["UCLVC"]["XZimbraCsrfToken"]
            else:
                async with session.get(host,headers=headers) as resp:
                    html = await resp.text()
                soup = BeautifulSoup(html,"html.parser")
                XZimbraCsrfToken = soup.find("input",{"name":"login_csrf"})["value"]
                payload = {
                    "loginOp": "login",
                    "login_csrf": XZimbraCsrfToken,
                    "username": user,
                    "password": passw,
                    "client": "preferred"
                }
                async with session.post(host,data=payload,headers=headers) as resp:
                    html = await resp.text()
                XZimbraCsrfToken = str(html).split('localStorage.setItem("csrfToken" , "')[1].split('");')[0]
                await save_logs(XZimbraCsrfToken)
                milliseconds = int(str(html).split('window.authTokenExpires     = ')[1].split(";")[0])
                EXPIRE_COOKIE = datetime.fromtimestamp(milliseconds / 1000.0)
                await save_logs(EXPIRE_COOKIE)
                DB_global["UCLVC"]["time"] = str(EXPIRE_COOKIE)
                DB_global["UCLVC"]["XZimbraCsrfToken"] = XZimbraCsrfToken
                cookies = session.cookie_jar
                v = {}
                for cookie in cookies:
                    v[cookie.key] = cookie.value
                DB_global["UCLVC"]["cookies"] = v
                await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            if myfiles:
                payload = {
                    "Body": {
                        "SearchRequest": {
                            "_jsns": "urn:zimbraMail",
                            "limit": 100,
                            "locale": {
                                "_content": "es"
                            },
                            "needExp": 1,
                            "offset": 0,
                            "query": "in:briefcase",
                            "sortBy": "subjAsc",
                            "types": "document",
                            "tz": {
                                "id": "Europe/Berlin"
                            }
                        }
                    },
                    "Header": {
                        "context": {
                            "_jsns": "urn:zimbra",
                            "account": {
                                "_content": user,
                                "by": "name"
                            },
                            "csrfToken": XZimbraCsrfToken,
                            "session": {
                                "_content": 1664,
                                "id": 1664
                            },
                            "userAgent": {
                                "name": "ZimbraWebClient - FF115 (Win)",
                                "version": "8.8.15_GA_4508"
                            }
                        }
                    }
                }
                async with session.post(host+"service/soap/SearchRequest",json=payload,headers=headers) as resp:
                    html = await resp.text()
                data = json.loads(html)
                ftotal = 0
                mg = ""
                try:
                    for i in data["Body"]["SearchResponse"]["doc"]:
                        DID = i["id"]
                        name = i["name"]
                        fsize = sizeof_fmt(i["s"])
                        ftotal+=i["s"]
                        if not deleteall:
                            mg+=f"➣ /r_{DID} 📄 {name} [ {fsize} ]\n"
                        else:
                            await msg.edit(f"🔴 Borrando {name}")
                            payload = {
                                "Body": {
                                    "ItemActionRequest": {
                                        "_jsns": "urn:zimbraMail",
                                        "action": {
                                            "id": DID,
                                            "op": "trash"
                                        }
                                    }
                                },
                                "Header": {
                                    "context": {
                                        "_jsns": "urn:zimbra",
                                        "account": {
                                            "_content": user,
                                            "by": "name"
                                        },
                                        "csrfToken": XZimbraCsrfToken,
                                        "notify": {
                                            "seq": 1
                                        },
                                        "session": {
                                            "_content": 1418,
                                            "id": 1418
                                        },
                                        "userAgent": {
                                            "name": "ZimbraWebClient - FF115 (Win)",
                                            "version": "8.8.15_GA_4508"
                                        }
                                    }
                                }
                            }
                            async with session.post(host+"service/soap/ItemActionRequest",json=payload,headers=headers) as resp:
                                await save_logs("Deleted "+name+" "+str(resp.status))
                except:pass
                if not deleteall:
                    await msg.edit(f"💭 Archivos subidos {sizeof_fmt(ftotal)} | 2 GiB\n\n{mg}\n\n**Eliminar todo**\n/clear")
                else:
                    await msg.edit("♦️ **TODOS LOS ARCHIVOS FUERON BORRADOS**")
                    await webmailuclv_api('',usid,msg,username,myfiles=True,deleteall=False)
                return
            filesize = Path(file).stat().st_size
            filename = file.split("/")[-1]
            ttotal_t = filesize
            tfilename = filename
            init_time = time()
            links = ""
            links2 = ""
            ttotal = 0
            partes = 0
            zipssize = 36*1024*1024
            headers["X-Zimbra-Csrf-Token"] = XZimbraCsrfToken
            headers["X-Requested-With"] = "XMLHttpRequest"
            await save_logs("a Cargar")
            file = await file_renamer(file)
            filename = file.split("/")[-1]
            if filesize-1048>zipssize:
                await msg.edit(f"📦 **Comprimiendo en zips**")
                files = await bot.loop.run_in_executor(None, sevenzip, file, None, zipssize)
            else:
                files = [file]
            linksz = []
            timeout = aiohttp.ClientTimeout(total=600)
            for file in files:
                try:
                    current = Path(file).stat().st_size
                    fname = file.split("/")[-1]
                    fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres_medisur(current,total,timestart,filename,msg,ttotal,ttotal_t,tfilename))
                    async with session.post(host+"service/upload?lbfums=",data=fi,headers={"Content-Disposition":f'attachment; filename="{fname}"',**headers}) as resp:
                        html = await resp.text()
                        await save_logs(resp.status)
                        ttotal+=current
                        partes+=1
                    await msg.edit("🛠 **Construyendo Enlace*")
                    id = str(html).split("'null','")[1].split("'")[0]
                    await save_logs(id)
                    payload = {
                        "Body": {
                            "BatchRequest": {
                                "_jsns": "urn:zimbra",
                                "onerror": "continue",
                                "SaveDocumentRequest": {
                                    "_jsns": "urn:zimbraMail",
                                    "doc": {
                                        "l": "16",
                                        "upload": {
                                            "id": id
                                        }
                                    },
                                    "requestId": 0
                                }
                            }
                        },
                        "Header": {
                            "context": {
                                "_jsns": "urn:zimbra",
                                "account": {
                                    "_content": user,
                                    "by": "name"
                                },
                                "csrfToken": XZimbraCsrfToken,
                                "notify": {
                                    "seq": 1
                                },
                                "session": {
                                    "_content": 1277,
                                    "id": 1277
                                },
                                "userAgent": {
                                    "name": "ZimbraWebClient - FF115 (Win)",
                                    "version": "8.8.15_GA_4508"
                                }
                            }
                        }
                    }
                    async with session.post(host+"service/soap/BatchRequest",json=payload,headers={"Content-Type":"application/soap+xml; charset=utf-8",**headers},timeout=timeout) as resp:
                        await save_logs(resp.status)
                        html = await resp.text()
                        if resp.status==200:
                            try:
                                data = json.loads(html)
                                name = data["Body"]["BatchResponse"]["SaveDocumentResponse"][0]["doc"][0]["name"]
                                await save_logs(name)
                                DID = data["Body"]["BatchResponse"]["SaveDocumentResponse"][0]["doc"][0]["id"]
                                await save_logs(DID)
                                url = f"{host}home/{user}/Briefcase/{name}?disp=a"
                                await save_logs(url)
                                linksz.append(url)
                            except Exception as ex:
                                if 'SaveDocumentResponse' in str(ex):
                                    await msg.edit(f"💢 __EL ARCHIVO {fname} YA ESTÁ SUBIDO A LA NUBE__ 💢")
                                    return
                                else:
                                    await save_logs("UP0 "+str(ex))
                except Exception as e:
                    await save_logs("UP "+str(e))
            await msg.delete()
            m = f"🎖 **FINALIZADO** 🎖 \n\n 🎬 `{filename}`\n📦 **Tamaño:** {sizeof_fmt(ttotal_t)}\n"
            await bot.send_message(username,m)
            message = ""
            if DB_global["UCLVC"]["X"]:
                message = await xdlink(session,linksz)
            else:
                for link in linksz:
                    message+=f"{link}\n"
            with open(filename+".txt","w") as txt:
                txt.write(message)
            await bot.send_document(usid,filename+".txt",thumb="thumb.png",caption="😊 **Gracias Por Usar Nuestro Servicio**\n#rayserverdl #superinlinesearch\n")
            os.unlink(filename+".txt")
    except Exception as ex:
        await save_logs("WebM "+str(ex))
        return

async def tesisld_api(file,usid,msg,username):
	try:
		zipssize=149*1024*1024
		filename = file.split("/")[-1]
		host = "https://tesis.sld.cu/"
		filesize = Path(file).stat().st_size
		print(21)
		headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"}
		proxy = None #Configs[username]["gp"]
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
		#login
		msg = await msg.edit("🔴 Conectando ... 🔴")
		connector = aiohttp.TCPConnector()
		if proxy:
			connector = aiohttp_socks.ProxyConnector.from_url(proxy)
		async with aiohttp.ClientSession(connector=connector) as session:
			payload = payload = {}
			payload["F_UserName"] = "lazaro03"
			payload["F_Password"] = "Michel03."
			async with session.post(host+"index.php?P=UserLogin", data=payload,headers=headers) as e:
				print(222)
				print(e.url)
			#upload
			if filesize-1048>zipssize:
				parts = round(filesize / zipssize)
				await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐\n\n🏷 Total: {parts} partes\n")
				files = sevenzip(file,volume=zipssize)
				print(24)
				links = []
				for file in files:
					try:
						async with session.get(host+"index.php?P=EditResource&ID=NEW",headers=headers) as resp:
							raw_data = await resp.read()
							text = raw_data.decode('utf-8', errors='replace')
						soup = BeautifulSoup(text,"html.parser")
						f_ids = soup.find("form",attrs={"name":"EditForm"})["action"]
						url_id = f_ids.split("-")[1]
						payload = {}
						payload["F_RecordStatus"] = "3"
						payload["F_Title"] = ""
						payload["F_Autor"] = ""
						payload["PDF"] = "application/octet-stream"
						payload["F_Description"] = ""
						payload["F_Anodedefensadelatesis"] = "-1"
						payload["F_Tutor1"] = ""
						payload["F_Tutor2"] = ""
						payload["F_Tutor3"] = ""
						payload["F_Tutor4"] = ""
						payload["F_Estado"] = "72"
						payload["F_Lugar"] = ""
						payload["F_Departamento"] = ""
						payload["F_ISBN"] = ""
						payload["F_Editorial"] = ""
						payload["F_Tipodefecha"] = "70"
						payload["F_UrlOficial"] = ""
						payload["F_Materia[]"] = ""
						payload["F_Materia[]"] = ""
						payload["F_Listadescriptores[]"] = ""
						payload["F_Listadescriptores[]"] = ""
						payload["F_Numerodelaresolucion"] = ""
						payload["F_Anoresolucion"] = "-1"
						payload["F_InformacionAdicional"] = ""
						payload["F_TextoCompleto"] = "68"
						payload["Submit"] = "Cargar"
						payload["F_Autorescorporativos"] = ""
						payload["F_ComentariosySugerencias"] = ""
						fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))								
						query = {"Textorestringido":fi,**payload}
						async with session.post(host+f_ids,data=query,headers=headers) as resp:
							raw_data = await resp.read()
							text = raw_data.decode('utf-8', errors='replace')
						soup = BeautifulSoup(text,"html.parser")
						urls = soup.find_all("a")
						for u in urls:
							try:
								if "DownloadFile&Id" in u["href"]:
									await bot.send_message(username,host+u["href"])
									links.append(host+u["href"]+">"+url_id)
							except:
								pass
					except:
						pass
				await msg.edit(f"✅ Finalizado ✅ \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
				txtname = file.split('.')[0].replace(' ','_')+'.txt'
				with open(txtname,"w") as t:
					message = ""
					for li in links:
						message+=li+"\n"
					t.write(message)
					t.close()
				await bot.send_document(usid,txtname,thumb="thumb.jpg",caption="👤 Usuario: lazaro03\n🔑 Contraseña: Michel03.")
				os.unlink(txtname)
			else:
				print(111)
				h = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8","Accept-Encoding":"deflate","Accept-Language":"en-US,en;q=0.5","Connection":"keep-alive","User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
				await msg.edit("💠 Subiendo 💠")
				print(host+"index.php?P=EditResource&ID=NEW")
				async with session.get(host+"index.php?P=EditResource&ID=NEW",headers=h) as resp:
					print(resp.status)
					raw_data = await resp.read()
					text = raw_data.decode('utf-8', errors='replace')
					print("ya")
				soup = BeautifulSoup(text,"html.parser")
				f_ids = soup.find("form",attrs={"name":"EditForm"})["action"]
				print(f_ids)
				url_id = f_ids.split("-")[1]
				payload = {}
				payload["F_RecordStatus"] = "3"
				payload["F_Title"] = ""
				payload["F_Autor"] = ""
				payload["PDF"] = "application/octet-stream"
				payload["F_Description"] = ""
				payload["F_Anodedefensadelatesis"] = "-1"
				payload["F_Tutor1"] = ""
				payload["F_Tutor2"] = ""
				payload["F_Tutor3"] = ""
				payload["F_Tutor4"] = ""
				payload["F_Estado"] = "72"
				payload["F_Lugar"] = ""
				payload["F_Departamento"] = ""
				payload["F_ISBN"] = ""
				payload["F_Editorial"] = ""
				payload["F_Tipodefecha"] = "70"
				payload["F_UrlOficial"] = ""
				payload["F_Materia[]"] = ""
				payload["F_Materia[]"] = ""
				payload["F_Listadescriptores[]"] = ""
				payload["F_Listadescriptores[]"] = ""
				payload["F_Numerodelaresolucion"] = ""
				payload["F_Anoresolucion"] = "-1"
				payload["F_InformacionAdicional"] = ""
				payload["F_TextoCompleto"] = "68"
				payload["Submit"] = "Cargar"
				payload["F_Autorescorporativos"] = ""
				payload["F_ComentariosySugerencias"] = ""
				fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))								
				query = {"Textorestringido":fi,**payload}
				async with session.post(host+f_ids,data=query,headers=headers) as resp:
					raw_data = await resp.read()
					text = raw_data.decode('utf-8', errors='replace')
				soup = BeautifulSoup(text,"html.parser")
				urls = soup.find_all("a")
				for u in urls:
					try:
						if "DownloadFile&Id" in u["href"]:
							url = host+u["href"]+">"+url_id
							await bot.send_message(username,url)
							await msg.edit(f"✅ Finalizado ✅ \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
							txtname = file.split('.')[0].replace(' ','_')+'.txt'
							with open(txtname,"w") as t:
								t.write(url)
							t.close()
							await bot.send_document(usid,txtname,thumb="thumb.jpg",caption="👤 Usuario: lazaro03\n🔑 Contraseña: Michel03.")
							os.unlink(txtname)
					except:
						pass
	except Exception as e:
		print(str(e))

async def rudg_api(file,usid,msg,username):
    try:
        usern = "proslayer"
        passw = "Dairon2005"
        zipssize=200*1024*1024
        filename = file.split("/")[-1]
        host = "https://revistas.udg.co.cu/index.php/reudgr/"
        filesize = Path(file).stat().st_size
        print(21)
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"}
        proxy = None #Configs[username]["gp"]
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
        #login
        msg = await msg.edit("🔴 Conectando ... 🔴")
        connector = aiohttp.TCPConnector()
        if proxy:
            connector = aiohttp_socks.ProxyConnector.from_url(proxy)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(host+"login",headers=headers) as resp:
                html = await resp.text()
            soup = BeautifulSoup(html,"html.parser")
            csrfToken = soup.find("input",attrs={"name":"csrfToken"})["value"]
            payload = {
                "csrfToken": csrfToken,
                "source": "",
                "username": usern,
                "password": passw,
                "remember": "1"
            }
            async with session.post(host+"login/signIn", data=payload,headers=headers) as e:
                print(222)
                print(e.url)
            #upload
            if filesize-1048>zipssize:
                parts = round(filesize / zipssize)
                await msg.edit(f"📦 𝑪𝒐𝒎𝒑𝒓𝒊𝒎𝒊𝒆𝒏𝒅𝒐\n\n🏷 Total: {parts} partes\n")
                files = sevenzip(file,volume=zipssize)
                print(24)
                links = []
            else:
                files = [file]
                links = []
            for file in files:
                try:
                    payload = {}
                    payload["name"] = file.split("/")[-1]
                    payload["revisedFileId"] = ""
                    payload["genreId"] = "86"
                    fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))                               
                    query = {"uploadedFile":fi,**payload}
                    async with session.post(host+"$$$call$$$/wizard/file-upload/file-upload-wizard/upload-file?submissionId=4159&stageId=1&fileStage=2&reviewRoundId=&assocType=&assocId=",data=query,headers=headers) as resp:
                        html = await resp.text()
                    data = loads(html)
                    ids = data["uploadedFile"]["fileId"]
                    url = f"{host}$$$call$$$/api/file/file-api/download-file?fileId={ids}&revision=1&submissionId=4159&stageId=1"
                    await bot.send_message(username,url)
                    links.append(url)
                except:
                    pass
            await msg.edit(f"✅ Finalizado ✅ \n\n{filename}\n[ .txt ] ⤵️")
            txtname = file.split('.')[0].replace(' ','_')+'.txt'
            with open(txtname,"w") as t:
                message = ""
                for li in links:
                    message+=li+"\n"
                t.write(message)
                t.close()
            await bot.send_document(usid,txtname,thumb="thumb.jpg",caption=f"👤 Usuario: {usern}\n🔑 Contraseña: {passw}")
            os.unlink(txtname)
    except Exception as e:
        print(str(e))

async def upload_uci(path,usid,msg,username):
    if "id_del" in Configs[username]:pass
    else:
        Configs[username]["id_del"] = [] 
        await send_config()
    msg = await bot.send_message(username, "**Iniciando**")
    namefile = os.path.basename(path)
    id_de_ms[username] = {"msg":msg, "pat":namefile, "proc":"Up"}
    acuser = Configs[username]["user"]
    user = str(Configs[username]["user"])
    passw = str(Configs[username]["pasw"])
    id_up = str(Configs[username]["id"])
    zips = str(Configs[username]["zips"])
    url_login = str(Configs[username]["host"])
    log = "https://ediciones.uo.edu.cu/index.php/e1/login/signIn"
    filesize = Path(path).stat().st_size
    zipssize = 1024*1024*int(zips)
    size = os.path.getsize(path)/(1024 * 1024)
    size = round(size, 2)
    host = str(Configs["up_dspace"]["host"])
    if filesize-1048>zipssize:
        urls = " "
        await msg.edit("**Iniciando Sesión...**")
        async with aiohttp.ClientSession() as session:
            async with session.get(log, ssl=False) as a:
                html = await a.text()
            soup = BeautifulSoup(html, 'html.parser') 
            csrfToken = soup.find("input", attrs={"name": "csrfToken"})["value"]
            data = {
                "X-Csrf-token": csrfToken,
                "source": "",
                "username": "stvz02",
                "password": "stvz02",
                "remember" : "1"
            }
            async with session.post(log, data=data, ssl=False) as a:
                text = await a.text()
                if "El nombre" in text:
                    await msg.delete()
                    await bot.send_message(username, "**Datos Erroneos de Login\nUse el comando /data_rev para añadir sus datos**")
                    id_de_ms[username]["proc"] = ""
                    return
                else:pass
            await msg.edit("**Sesión Iniciada...**")
            upload_url = f"{url_login}/api/v1/submissions/{id_up}/files"
            inic = time()
            id_delg =[]
            parts = round(filesize / zipssize)
            file_name = os.path.basename(path)
            await msg.edit(f"**Comprimiendo 📂 {file_name}**")
            files = sevenzip(path,volume=zipssize)
            for file in files:
                name_parte = os.path.basename(file)
                fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
                upload_data = {}
                upload_data["fileStage"] = "2"
                upload_data["name[es_ES]"] = name_parte
                upload_data["name[en_US]"] = name_parte
             #   upload_data["file"] = fi
                query = {"file":fi,**upload_data}
                headers = {"X-Csrf-token": csrfToken}
                async with session.post(upload_url, data=query, headers=headers, ssl=False) as resp:
                    if resp.status == 500 or resp.status == 400:
                        await msg.delete()
                        await bot.send_message(username, "**Nube Llena. Por Favor elimine los archivos subidos 📂n\nPuede usar el comando /del_files_all para eliminar todo del server**")
                        id_de_ms[username]["proc"] = ""
                        return
                    else:pass
                    text = await resp.text()
                    response_json = await resp.json()
                    id_del = response_json['id']
                    base_id_del = Configs[username]["id_del"]
                    base_id_del.append(id_del)
                    Configs[username]["id_del"] = base_id_del
                    await send_config()
                    urls += response_json["url"]+"\n"
            uptime = get_readable_time(time() - inic)
            with open(namefile+".txt","w") as f:
                f.write(urls)
            await bot.send_document(username, namefile+".txt", thumb="thumb.jpg", caption=f"**Archivo Subido...\nNombre: {namefile}\nTamaño: {size} Mb\n\nSubido Con: @Stvz_Upload_bot en {uptime}**\n\nDatos para descagar:\nDeben longuearse aquí {log} con los siguientes datos:\nUsuario: {user}\nContraseña: {passw}")
            await msg.delete()
            id_de_ms[username]["proc"] = ""
            return   
    else: 
        await msg.edit("**Iniciando Sesión...**")
        async with aiohttp.ClientSession() as session:
            async with session.get("https://ediciones.uo.edu.cu/index.php/e1/login/signIn", ssl=False) as a:
                html = await a.text()
            soup = BeautifulSoup(html, 'html.parser') 
            csrfToken = soup.find("input", attrs={"name": "csrfToken"})["value"]
            data = {
                "X-Csrf-token": csrfToken,
                "source": "",
                "username": "stvz02",
                "password": "stvz02",
                "remember" : "1"
            }
            async with session.post("https://ediciones.uo.edu.cu/index.php/e1/login/signIn", data=data, ssl=False) as a:
                text = await a.text()
                u = str(a.url)
                if u == "https://ediciones.uo.edu.cu/index.php/e1/login/signIn":
                    await msg.delete()
                    await bot.send_message(username, "**Datos Erroneos de Login\nUse el comando /data_rev para añadir sus datos**")
                    id_de_ms[username]["proc"] = ""
                    return
                else:pass
            await msg.edit("**Sesion Iniciada1**✅")
            # Hacer la solicitud anterior
            fi = Progress(path,lambda current,total,timestart,filename: uploadfile_progres(current,total,timestart,filename,msg))
            upload_data = {}
            upload_data["name"] = namefile
            upload_data["genreId"] = "8"
            upload_data["uploadedFile"] = fi
            query = {"uploadedFile":fi,**upload_data}
            upload_url = "https://ediciones.uo.edu.cu/index.php/e1/$$$call$$$/wizard/file-upload/file-upload-wizard/upload-file?submissionId=132&stageId=1&fileStage=18&reviewRoundId=&assocType=520&assocId=159&queryId=159"
            inic = time()
            async with session.post(upload_url, data=query, ssl=False) as resp:
                if resp.status == 500 or resp.status == 400:
                    await msg.delete()
                    await bot.send_message(username, "**Nube Llena. Por Favor elimine los archivos subidos 📂n\nPuede usar el comando /del_files_all para eliminar todo del server**")
                    id_de_ms[username]["proc"] = ""
                    return
                else:pass
                text = await resp.text()
                response_json = await resp.json()  
                file_id = response_json["uploadedFile"]["fileId"]
                id_sub = response_json["uploadedFile"]["id"]
                await bot.send_message(username, f"Archivo Subido\nNombre: {namefile}\nTamaño: {filesize}\n`https://stvz.down/a/{id_sub}/{file_id}/{namefile}`")
                await msg.delete()
                id_de_ms[username]["proc"] = ""
                return
                ##############################################################

async def upload_token(zips,token,url,path,usid,msg,username):
    msg = await bot.send_message(username, "**Verificando Proxy**")
    proxy = Configs["proxy"]
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True), connector=aiohttp_socks.SocksConnector.from_url(proxy)) as session:
        async with session.get("https://www.google.com/", ssl=False) as response:
            if response.status == 200:
                await msg.edit("**Proxy Activo**")
                pass
            else:
                await msg.edit("**Proxy caido Caida**")
                return
        await msg.edit("**Verificando Nube☁️**")
        v = url+"/login/index.php"
        async with session.get(v, ssl=False) as response:
            if response.status == 200:
                await msg.edit("**Nube Activa**")

                pass
            else:
                await msg.edit("**Nube Caida**")
                return
    filesize = Path(path).stat().st_size
    zipssize = 1024*1024*int(zips)
    size = os.path.getsize(path)/(1024 * 1024)
    size = round(size, 2)
    name = os.path.basename(path)

async def uploads_options(filename, filesize, username):
    buttons = [
        [InlineKeyboardButton("☁UO☁","UO")],
        [InlineKeyboardButton("☁BitZero☁","BitZero")],
        [InlineKeyboardButton("♻Privada♻","Privada")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(username,f'Seleccione el Modo de Subida:\n📕Nombre: {filename.split("/")[-1]}\n📦Tamaño: {sizeof_fmt(filesize)}',reply_markup=reply_markup)
#Run...
backup_thread = threading.Thread(target=save_backup)
backup_thread.daemon = True
backup_thread.start()
try:os.unlink("bot.session")
except:pass
try:os.unlink("bot.session-journal")
except:pass
print("started")
bot.start()
bot.loop.run_forever()