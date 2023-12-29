from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery , ReplyKeyboardMarkup, ForceReply , InputMediaDocument , MessageEntity
from pyrogram import Client , filters 
from config import API_HASH,API_ID,BOT_TOKEN,ID_DB,ID_ACC,ID_DB_data,ID_DB_user,FILE_DB,MSG_LOG
import os
from os.path import exists
from time import localtime
from json import loads, dumps
from random import randint
import random
from pathlib import Path
import aiohttp
import asyncio
from urllib.parse import unquote_plus
from time import time,sleep
import bs4
import json
import re
import uuid
from io import BufferedReader
import mimetypes
import requests
from tools.funciones import filezip,descomprimir,limite_msg,files_formatter,mediafiredownload, download_progres , downloadmessage_progres , ytdlp_downloader, sevenzip, uploadfile_progres
from clients.token import MoodleClient
import aiohttp_socks
from clients.draft import MoodleClient2
import shutil 
from bs4 import BeautifulSoup
from pyshortext import short, unshort
from DspaceUclv import DspaceClient
from verify_user import VerifyUserData
from datetime import datetime
from xdlink import xdlink
sizes_reads = {}

admins = ["Pro_Slayerr"]
Temp_dates = {}
DB_global = {}
Config_temp = {}

cancel_list = {}
download_list = {}
reg_db = -1001965505199

DB_accs = {'accesos':[]}
seg = 0

COOKIES_DATE = ()

bot = Client("bot",api_id=API_ID,api_hash=API_HASH,bot_token=BOT_TOKEN)

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

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)

async def send_db():
    datos = datetime.now()
    nueva_media = InputMediaDocument("usuarios.db",caption=str(datos))
    await bot.edit_message_media(chat_id=ID_DB,message_id=FILE_DB,media=nueva_media)
    return

async def save_logs(text):
    message = await bot.get_messages(ID_DB,message_ids=int(MSG_LOG))
    texto = message.text+"\n"+str(text)
    await message.edit(texto[-500:])
    return

async def xdlinks(session,urls,channelid=""):
    strurls = ''
    i = 0
    for u in urls:
        strurls += str(u)
        if i < len(urls)-1:
            strurls += '\n'
        i+=1
    api = 'https://xd-core-api.onrender.com/xdlinks/encode'
    jsondata = {'channelid':channelid,'urls':strurls}
    headers = {'Content-Type':'application/json','Accept': '*/*','Origin':'https://xdownloader.surge.sh','Referer':'https://xdownloader.surge.sh/'}
    async with session.post(api,data=json.dumps(jsondata),headers=headers) as resp:
        html = await resp.text()
    jsonresp = json.loads(html)
    if 'data' in jsonresp:
        return jsonresp['data']
    return None

def rar_compress(file_path: Path, split_size, username):
    files = []
    temp_dir = f"downloads/{username}/TEMP/"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    with open(file_path, "rb") as file:
        part_number = 0
        while (data := file.read(split_size)):
            part_filename = f"{file_path.name}"
            part_path = Path(f"{temp_dir}{part_filename}")
            with open(part_path, "wb") as part_file:
                part_file.write(data)
            shutil.make_archive(f"{part_path}-{part_number}", 'zip', temp_dir, part_filename)
            os.unlink(part_path)
            shutil.move(f"{part_path}-{part_number}.zip",f"downloads/{username}/{part_filename}-{part_number}.zip")
            files.append(f"downloads/{username}/{part_filename}-{part_number}.zip")
            part_number += 1
    shutil.rmtree(f"downloads/{username}/TEMP/")
    return files

@bot.on_message(filters.private)
async def start(client: Client, message: Message):
    async def worker(client: Client, message: Message):
        username = message.from_user.username
        user_id = message.from_user.id
        send = message.reply
        out_message = message.text
        fecha_actual = localtime().tm_mday

        #! Crear carpeta download si no existe
        if exists('ɗ᧐ᥕᥒᥣ᧐ᥲɗs/'+str(username)+'/'):pass
        else:os.makedirs('ɗ᧐ᥕᥒᥣ᧐ᥲɗs/'+str(username)+'/')
        try: Temp_dates[username]
        except: Temp_dates[username] = {'ɗ᧐ᥕᥒᥣisᴛ' : [],'file':''}
        try: Config_temp[username]
        except: Config_temp[username] = {'host':'','user':'','passw':'','zips':5,'proxy_pv':'','proxy': True,'repo':5,'token':None}

        #await bot.edit_message_text(ID_DB,message_id=2,text=dumps(xd,indent=4))
        msg = await bot.get_messages(ID_DB,message_ids=ID_DB_data)
        DB_global.update(loads(msg.text))
        msg_conf = await bot.get_messages(ID_ACC,message_ids=ID_DB_user)
        DB_accs.update(loads(msg_conf.text))

        m = await bot.get_messages(ID_DB, message_ids=FILE_DB)
        try:
            os.unlink("usuarios.db")
        except:pass
        try:
            os.unlink("downloads/usuarios.db")
        except:pass
        await m.download(file_name=f"usuarios.db")
        os.rename("downloads/usuarios.db","usuarios.db")

        if not DB_global['Estado_del_bot'] and username not in admins:
            await send('''**🌘ʙᴏᴛ ᴀᴘᴀɢᴀᴅᴏ ᴇs ᴍɪ ʜᴏʀᴀ ⏲️ ᴅᴇ ᴅᴇsᴄᴀɴsᴏ🌒**

**⏳ʜᴏʀᴀʀɪᴏ ᴘɪᴄᴏ**
2:00PM a 10:00PM

**‼️sᴏʟᴏ ᴇsᴘᴇʀᴇ ᴀ ǫᴜᴇ sᴇ ᴇɴᴄɪᴇɴᴅᴀ‼️**''')
            return
        if username not in DB_accs['accesos']:
            await send('**❌ɴᴏ ᴛɪᴇɴᴇ ᴀᴄᴄᴇsᴏ ᴀʟ ʙᴏᴛ❌ ᴘᴏʀ ғᴀᴠᴏʀ ᴄᴏɴᴛᴀᴄᴛᴇ ᴀ ᴍɪ ᴘʀᴏᴘɪᴇᴛᴀʀɪᴀ⚡️ @tufutbolista11❌**')
            return

        if message.audio or message.document or message.animation or message.sticker or message.photo or message.video:
            if not username in download_list:
                download_list[username] = []

            download_list[username].append(message)
            msg = await bot.send_message(username,"♻️ℝ𝕖𝕔𝕠𝕡𝕚𝕝𝕒𝕟𝕕𝕠 𝕀𝕟𝕗𝕠𝕣𝕞𝕒𝕔𝕚ó𝕟♻️")

            for i in download_list[username]:
                filesize = int(str(i).split('"file_size":')[1].split(",")[0])
                try:
                    filename = str(i).split('"file_name": ')[1].split(",")[0].replace('"',"")
                except:
                    filename = str(randint(11111,999999))+".mp4"
                start = time()
                await msg.edit(f"🦾 ℙ𝕣ᥱρᥲ𝕣ᥲᥒɗ᧐ 𑀥ᥱ𝕤ᥴᥲ𝕣𝕘𝕒 🦾\n\n`{filename}`")
                if not os.path.exists(f'ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/{filename}'):
                    try:
                        a = await i.download(file_name=f'ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/{filename}',progress=downloadmessage_progres,progress_args=(filename,start,msg))
                        if Path(f'ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/{filename}').stat().st_size == filesize:
                            await msg.edit("⚡D⃨e⃨s⃨c⃨a⃨r⃨g⃨a⃨ E⃨x⃨i⃨t⃨o⃨s⃨a⃨⚡")
                            download_list[username] = []
                            #Temp_dates[username]['file'] = f'downloads/{username}/{filename}'
                            path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
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
                    path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                    return
        if out_message.startswith('/start'):
            button1 = InlineKeyboardButton("📝 Mi Plan ","plan")
            buttons = [[button1]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await bot.send_photo(username,'start.jpg',reply_markup=reply_markup,caption='''♥️ ᴴᵒᶫᵃ 👋🏻  ᴮᶦᵉᶰᵛᵉᶰᶦᵈᵒ 💢, 
✈️ ᴮᶦᵉᶰᵛᵉᶰᶦᵈᵒ ᵃ ᶜᵘᵇᵃᶠᶫᶦˣᴹᵃˣ 💢 ᴬᶦᵈᵃᶜʰᶦᵁᵖᶫᵒᵃᵈ ♻️, ᵉˢᵗᵒʸ ˢᶦᵉᵐᵖʳᵉ ᵖᵃʳᵃ ᵗᶦ 🫰🏻, ʸᵒ ᵖᵘᵉᵈᵒ ᵃʸᵘᵈᵃʳᵗᵉ ᵃ ᵈᵉˢᶜᵃʳᵍᵃʳ ᶜᵘᵃᶫᶞᵘᶦᵉʳ ᵃʳᶜʰᶦᵛᵒ ᵐᵘᶫᵗᶦᵐᵉᵈᶦᵃ ᶞᵘᵉ ᵈᵉˢᵉᵉˢ 📂 ˢᶦᶰ ᶜᵒᶰˢᵘᵐᵒ ᵈᵉ ᵐᵉᵍᵃˢ 🧬
🚀 ᴾᵃʳᵃ ᶜᵒᵐᵉᶰᶻᵃʳ ✅ ᵉᶰᵛᶦé ᶜᵘᵃᶫᶞᵘᶦᵉʳ 📂 ᵃʳᶜʰᶦᵛᵒ ᵒ 🔗 ᵉᶰᶫᵃᶜᵉˢ ᵖᵃʳᵃ ᵖʳᵒᶜᵉˢᵃʳ 🌐 ˢᵉ ᵖᵘᵉᵈᵉᶰ ᵉᶰᵛᶦᵃʳ ᵃʳᶜʰᶦᵛᵒˢ ᵈᵉˢᵈᵉ ➜ (ᵞᵒᵘᵀᵘᵇᵉ 💻, ᵀʷᶦᶜʰ 📱, ᴹᵉᵈᶦᵃᶠᶦʳᵉ 🖥 ᵉᶰᵗʳᵉ ᵒᵗʳᵒˢ ˢᵒᵖᵒʳᵗᵉˢ ⛓)''')
            return

        if out_message.startswith('/ls'):
            path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
            msg = files_formatter(path,username)
            await limite_msg(msg[0],username,bot)
            return

        if out_message.startswith('/myfiles'):
            msg = await bot.send_message(username,"♠️ Buscando archivos")
            await webmailuclv_api('',user_id,msg,username,myfiles=True,deleteall=False)
            return

        if out_message.startswith('/clear'):
            msg = await bot.send_message(username,"♠️ Borrando Archivos")
            await webmailuclv_api('',user_id,msg,username,myfiles=True,deleteall=True)
            return

        if out_message.startswith("/my"):
            try:
                data = VerifyUserData().data_user(user_id)
                data = json.loads(data[2])
                msg = "📝 Datos:\n\n"
                msg+= f"📌 Plan: {data['plan']}\n"
                msg+= f"📌 Limite: {sizeof_fmt(data['limite'])}\n"
                msg+= f"📌 Subido: {sizeof_fmt(data['total'])}"
                await bot.send_message(username,msg)
            except:
                await bot.send_message(username,"Elige tu Plan 😉\n\n➧ Plan Básico:\n10 GB de transferencia diaria\n💳90 CUP | 📱 110 CUP\n➧ Plan Estándar: \n20 GB de transferencia diaria\n💳150 CUP | 📱 170 CUP\n➧ Plan Avanzado: \n40 GB de transferencia diaria\n💳200 CUP | 📱 250 CUP\n➧ Plan Premium:  \n80 GB de transferencia diaria\n💳250 CUP | 📱 280 CUP\n☺️ Plan NUBE UO: \n30 GB de transferencia diaria\n💳200 CUP | 📱 250 CUP\n\nContacta con: @tufutbolista11")
            return

        if out_message.startswith('/up'):
            path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
            if "_" in out_message:
                list = out_message.split("_")
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
            h = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
            lista = out_message.split(" ",2)
            name1 = int(lista[1])
            name2 = lista[2]
            msgh = files_formatter(h,username)
            actual = h+msgh[1][name1]
            shutil.move(actual,h+name2)
            await bot.send_message(username,f"R⃨e⃨n⃨o⃨m⃨b⃨r⃨a⃨d⃨o⃨ C⃨o⃨r⃨r⃨e⃨c⃨t⃨a⃨m⃨e⃨n⃨t⃨e⃨\n\n `{msgh[1][name1]}` ➥ `{name2}`")
            msg = files_formatter(h,username)
            await limite_msg(msg[0],username,bot)
            return

        if out_message.startswith("/deleteall"):
            path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
            shutil.rmtree("ɗ᧐ᥕᥒᥣ᧐ᥲɗs/"+username+"/")
            os.mkdir(f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/")
            msg = files_formatter(path,username)
            await limite_msg(msg[0],username,bot)
            return

        if out_message.startswith("/mkdir"):
            name = out_message.split(" ")[1]
            if "." in name or "/" in name or "*" in name:
                await bot.send_message(username,"💢ᴇʟ ɴᴏᴍʙʀᴇ ɴᴏ ᴘᴜᴇᴅᴇ ᴄᴏɴᴛᴇɴᴇʀ . , * /")
                return
            rut = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
            os.mkdir(f"{rut}/{name}")
            await bot.send_message(username,f"📁sᴇ ᴄʀᴇᴏ ᴜɴᴀ ᴄᴀʀᴘᴇᴛᴀ📁\n\n /{name}")
            msg = files_formatter(rut,username)
            await limite_msg(msg[0],username,bot)
            return

        if out_message.startswith("/rmdir"):
            path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
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

        if out_message.startswith("/rm"):
            path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
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
            path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
            archivo = out_message.split(" ")[1]
            ruta = path
            msgh = files_formatter(path,username)
            archivor = path+msgh[1][int(archivo)]
            a = await bot.send_message(username,"🎲D⃨e⃨s⃨c⃨o⃨m⃨p⃨r⃨i⃨m⃨i⃨e⃨n⃨d⃨o⃨ A⃨r⃨c⃨h⃨i⃨v⃨o⃨🎲")
            try:
                descomprimir(archivor,ruta)
                await a.edit("📚A⃨r⃨c⃨h⃨i⃨v⃨o⃨ D⃨e⃨s⃨c⃨o⃨m⃨p⃨r⃨i⃨m⃨i⃨d⃨o⃨📚")
                msg = files_formatter(path,username)
                await limite_msg(msg[0],username,bot)
                return
            except Exception as ex:
                await a.edit("Error: ",ex)
                return

        if out_message.startswith("/seven"):
            path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/"
            if "_" in out_message:
                lista = out_message.split("_")
            else:
                lista = out_message.split(" ")
            msgh = files_formatter(path,username)
            if len(lista) == 2:
                i = int(lista[1])
                j = str(msgh[1][i])
                if not "." in j:
                    h = await bot.send_message(username,"🌐C⃨o⃨m⃨p⃨r⃨i⃨m⃨i⃨e⃨n⃨d⃨o⃨🌐")
                    g = path+msgh[1][i]
                    p = shutil.make_archive(j, format = "zip", root_dir=g)
                    await h.delete()
                    shutil.move(p,path)
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                    return
                else:
                    g = path+msgh[1][i]
                    o = await bot.send_message(username,"🌐C⃨o⃨m⃨p⃨r⃨i⃨m⃨i⃨e⃨n⃨d⃨o⃨🌐")
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
                h = await bot.send_message(username,"🌐C⃨o⃨m⃨p⃨r⃨i⃨m⃨i⃨e⃨n⃨d⃨o⃨🌐")
                if not "." in j:
                    p = shutil.make_archive(j, format = "zip", root_dir=g)
                    await h.edit("⚡𝔇𝔦𝔳𝔦𝔡𝔦𝔢𝔫𝔡𝔬 𝔢𝔫 𝔓𝔞𝔯𝔱𝔢𝔰⚡")
                    a = sevenzip(p,password=None,volume = t*1024*1024)
                    os.remove(p)
                    for i in a :
                        shutil.move(i,path)
                    await h.edit("❄️C⃨o⃨m⃨p⃨r⃨e⃨s⃨i⃨ón⃨ R⃨e⃨a⃨l⃨i⃨z⃨a⃨d⃨a⃨❄️")
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                    return
                else:
                    a = sevenzip(g,password=None,volume = t*1024*1024)
                    await h.edit("❄️C⃨o⃨m⃨p⃨r⃨e⃨s⃨i⃨ón⃨ R⃨e⃨a⃨l⃨i⃨z⃨a⃨d⃨a⃨❄️")
                    msg = files_formatter(path,username)
                    await limite_msg(msg[0],username,bot)
                    return

        if out_message.startswith('http'):
            msg = await send('**📌P̰̰r̰̰ḛ̰p̰̰a̰̰r̰̰a̰̰n̰̰d̰̰o̰̰ D̰̰ḛ̰s̰̰c̰̰a̰̰r̰̰g̰̰a̰̰📌**')
            url = out_message
            if "youtu.be/" in out_message or "youtube.com/" in out_message or "twitch.tv/" in out_message:
                Temp_dates[username]['streaming_list'] = url
                await msg.edit(f"`🖥️ E͓̽l͓̽i͓̽j͓̽a͓̽ u͓̽n͓̽a͓̽ d͓̽e͓̽ l͓̽a͓̽s͓̽ c͓̽a͓̽l͓̽i͓̽d͓̽a͓̽d͓̽e͓̽s͓̽ d͓̽i͓̽s͓̽p͓̽o͓̽n͓̽i͓̽b͓̽l͓̽e͓̽s͓̽ 🖥️`",reply_markup=InlineKeyboardMarkup([
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
                file_path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/{file_name}"
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
                Temp_dates[username]['file'] = f'ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/{file_name}'
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
                        file_path = f"ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/{filename}"
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
                    Temp_dates[username]['file'] = f'ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/{filename}'
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
            await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            return

        if out_message.startswith('/c_uclv'):
            lista = out_message.split(' ')
            DB_global["UCLVC"] = {}
            DB_global["UCLVC"]["X"] = False
            DB_global["UCLVC"]["user"] = lista[1]
            DB_global["UCLVC"]["passw"] =  lista[2]
            DB_global["UCLVC"]["time"] = "2020-12-10 16:47:42.695000"
            DB_global["UCLVC"]["XZimbraCsrfToken"] = ""
            DB_global["UCLVC"]["cookies"] = {}
            await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            return

        if out_message.startswith('/private_proxy'):
            proxy = out_message.split(' ')[1]
            Config_temp[username]['proxy'] = proxy
            await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            return

        if out_message.startswith('/zips'):
            zips = out_message.split(' ')[1]
            Config_temp[username]['zips'] = zips
            await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            return

        #Admins 
        if out_message.startswith('/status_bot') and username in admins:  #ok
            DB_global['Estado_del_bot'] = False if DB_global['Estado_del_bot'] else True
            await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            return

        if out_message.startswith('/status_uclv') and username in admins: #ok
            print(DB_global['Estado_de_uclv'])
            DB_global['Estado_de_uclv'] = False if DB_global['Estado_de_uclv'] else True
            await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            return

        if out_message.startswith('/set') and username in admins:
            clouds = ['GTM', 'UCM','UCCFD','VCL','UCLV','LTU','EDUVI','GRM']
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

                await send('⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️')
                await bot.edit_message_text(ID_DB,message_id=ID_DB_data,text=dumps(DB_global,indent=4))
            else: await send('Esta nube no existe');return

        if out_message.startswith('/restart') and username in admins:
            try:
                msg = await bot.send_message(username,"〽️ **Restableciendo ...**")
                alls = VerifyUserData().all_userid()
                t = 0
                await msg.edit(f"〽️ **Restableciendo .{len(alls)}.**")
                for usid in alls:
                    d = VerifyUserData().data_user(int(usid))
                    d = json.loads(d[2])
                    d['total'] = 0
                    VerifyUserData().update_user(int(usid),d)
                    await send_db()
                    button1 = InlineKeyboardButton("📝 Mi Plan ","plan")
                    buttons = [[button1]]
                    reply_markup = InlineKeyboardMarkup(buttons)
                    await bot.send_message(int(usid),"〽️ **Límite diario restablecido**",reply_markup=reply_markup)
                    t+=1
                tl = len(alls)
                await msg.edit(f"〽️ **Límite Restablecido a {t} de {tl} Usuarios**")
                return
            except Exception as ex:
                await bot.send_message(username,str(ex))
                return

        if out_message.startswith('/add') and username in admins:
            d = out_message.split(" ")
            if len(d)==2:
                msg = f"🗣 Elige un plan para `@{d[1]}`\n"
                button1 = InlineKeyboardButton("🌀 Básico",f"add {d[1]} b")
                button2 = InlineKeyboardButton("🌀 Estándar",f"add {d[1]} e")
                button3 = InlineKeyboardButton("🌀 Avanzado",f"add {d[1]} a")
                button4 = InlineKeyboardButton("🌀 Premium",f"add {d[1]} p")
                button5 = InlineKeyboardButton("⚜️ NUBE UO ⚜️",f"add {d[1]} uo")
                buttons = [[button1,button2],[button3,button4],[button5]]
                reply_markup = InlineKeyboardMarkup(buttons)
                await bot.send_message(username,msg,reply_markup=reply_markup)
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
            await send('**⚡️ᴏᴘᴇʀᴀᴄɪóɴ ʀᴇᴀʟɪᴢᴀᴅᴀ⚡️**')
            return

    bot.loop.create_task(worker(client, message))

@bot.on_callback_query()
async def callback_handler(client: Client, callback_query: CallbackQuery):
    username = callback_query.from_user.username
    user_id = callback_query.from_user.id
    input_mensaje: str = str(callback_query.data)

    if "script" in input_mensaje:
        await callback_query.message.delete()
        input_mensaje = unshort(input_mensaje.split(" ")[1])
        umsg = await bot.send_message(username,"Conectando ...")
        msg = await bot.send_message(-1001994829316,input_mensaje)
        while True:
            data = await bot.get_messages(-1001994829316,message_ids=msg.id)
            if msg.text==data.text:
                pass
            if "[FINALIZADO]" in data.text:
                await umsg.edit("✅ **DESCARGA FINALIZADA** ✅\n\n📲 **Guardado en** `./Documents`\n#rayserver #superinline")
                break
            elif "On Progress" in data.text:
                try:
                    await umsg.edit(data.text,reply_markup=data.reply_markup.inline_keyboard)
                except:pass
        return
    elif "add" in input_mensaje:
        message = callback_query.message
        await message.delete()
        planes = {"b":"basico","e":"estandar","a":"avanzado","p":"premium","uo":"uo"}
        d = input_mensaje.split(" ")
        uname = d[1]
        pl = d[2]
        user = await bot.get_chat(uname)
        usid = user.id
        v = VerifyUserData().verify_already_exists(usid)
        if v:
            await bot.send_message(username,f"**No se puede agregar, @{user} ya es vip**")
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

    if input_mensaje=="plan":
        msg = callback_query.message
        await msg.delete()
        try:
            data = VerifyUserData().data_user(user_id)
            data = json.loads(data[2])
            msg = "📝 Datos:\n\n"
            msg+= f"📌 Plan: {data['plan']}\n"
            msg+= f"📌 Limite: {sizeof_fmt(data['limite'])}\n"
            msg+= f"📌 Subido: {sizeof_fmt(data['total'])}"
            await bot.send_message(username,msg)
        except:
            await bot.send_message(username,"Elige tu Plan 😉\n\n➧ Plan Básico:\n12 GB de transferencia diaria\n💳90 CUP | 📱 110 CUP\n➧ Plan Estándar: \n20 GB de transferencia diaria\n💳150 CUP | 📱 170 CUP\n➧ Plan Avanzado: \n40 GB de transferencia diaria\n💳200 CUP | 📱 250 CUP\n➧ Plan Premium:  \n80 GB de transferencia diaria\n💳250 CUP | 📱 280 CUP\n☺️ Plan NUBE UO: \n30 GB de transferencia diaria\n💳200 CUP | 📱 250 CUP\n\nContacta con: @tufutbolista11")

    if "ccancel" in input_mensaje:
        did = input_mensaje.split(" ")[1]
        cancel_list[did] = False
        msg = callback_query.message
        await msg.edit("❌ **D͓̽e͓̽s͓̽c͓̽a͓̽r͓̽g͓̽a͓̽ C͓̽a͓̽n͓̽c͓̽e͓̽l͓̽a͓̽d͓̽a͓̽** ❌")
        cancel_list.pop(did)
        return
    if "viewurls" in input_mensaje:
        dat = input_mensaje.split(" ")[1]
        text = unshort(dat)
        await bot.send_message(username,text)
        return
    if "fcancel" in input_mensaje:
        download_list[username] = []
        await callback_query.message.delete()
        await bot.send_message(username,"❌ **D͓̽e͓̽s͓̽c͓̽a͓̽r͓̽g͓̽a͓̽ C͓̽a͓̽n͓̽c͓̽e͓̽l͓̽a͓̽d͓̽a͓̽** ❌")
        return
    if input_mensaje == "144" or input_mensaje == "240" or input_mensaje == "360"  or input_mensaje == "480"  or input_mensaje == "720" or input_mensaje == "1080":
        msg = callback_query.message
        url = Temp_dates[username]['streaming_list']
        await msg.delete()
        msg = await client.send_message(username,"__🧬D͓̽e͓̽s͓̽c͓̽a͓̽r͓̽g͓̽a͓̽n͓̽d͓̽o͓̽🧬__")
        download = await ytdlp_downloader(url,user_id,msg,username,lambda data: download_progres(data,msg,input_mensaje),input_mensaje,f'ɗ᧐ᥕᥒᥣ᧐ᥲɗs/{username}/')
        size = os.path.getsize(download)
        await msg.delete()
        Temp_dates[username]['streaming_list'] = ''
        Temp_dates[username]['file'] = download
        await uploads_options('Youtube Video',size,username)
        return

    clouds = ['GTM', 'UCM','UCCFD','VCL','UCLV','LTU','EDUVI','Privada','GRM', 'TESISLS', 'EVEAUH', 'AULAENSAP', 'MEDISUR','MINED','DSPACE','UO']
    token_u = ['GTM', 'UCM','UCCFD','VCL','UCLV','LTU','GRM', 'EVEAUH', ]
    login = ['EDUVI','Privada','AULAENSAP']

    if input_mensaje in clouds:
        if input_mensaje == 'UCLV' and not DB_global['Estado_de_uclv']:
            await bot.send_message(username,'''**⛔️Ｍｏｏｄｌｅ Ｕｃｌｖ ａｐａｇａｄａ⛔️**

**ʜᴏʀᴀʀɪᴏ:**
🟢 𝟙𝟚:𝟘𝟘𝔸𝕄
🔴 𝟠:𝟘𝟘𝔸𝕄

**✅ ᴸᵃ ᵁᶜᶫᵛ ˢᵒᶫᵒ ᵗʳᵃᵇᵃʲᵃʳᵃ ⁸ ʰᵒʳᵃˢ**''')
            return

        await callback_query.message.delete()
        msg = await bot.send_message(username,"💥 ℝ𝕖𝕔𝕠𝕡𝕚𝕝𝕒𝕟𝕕𝕠 𝕀𝕟𝕗𝕠𝕣𝕞𝕒𝕔𝕚ó𝕟 💥")
        filename = Path(Temp_dates[username]['file']).name
        filesize = Path(Temp_dates[username]['file']).stat().st_size
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
                if input_mensaje == "MINED":
                    await sysmined_api(Temp_dates[username]['file'],user_id,msg,username)
                    return
                if input_mensaje == "UO":
                    if d["plan"]!="uo":
                        await msg.edit("💢 No puede usar este Servidor 💢\n\n🗣 Disponible con el plan Nube UO")
                        return
                    else:
                        await webdav(Temp_dates[username]['file'],user_id,msg,username)
                        return
                if input_mensaje == "MEDISUR":
                    await medisur_api(Temp_dates[username]['file'],user_id,msg,username)
                    return
                if input_mensaje == "DSPACE":
                    await dspace_api(Temp_dates[username]['file'],user_id,msg,username)
                    return
                if input_mensaje == "AULAENSAP":
                    Config_temp[username]['host'] = "https://aulaensap.sld.cu/"
                    Config_temp[username]['user'] = "cubaflix1"
                    Config_temp[username]['passw'] = "Cubaflix1234*"
                    Config_temp[username]['repo'] = "3"
                    Config_temp[username]["zips"] = 400
                    input_mensaje = 'Privada'
                if input_mensaje == "UCLVV":
                    Config_temp[username]['host'] = "https://moodle.uclv.edu.cu/"
                    Config_temp[username]['user'] = "ccgomez"
                    Config_temp[username]['passw'] = "Hiran@22"
                    Config_temp[username]['repo'] = "4"
                    Config_temp[username]["zips"] = 390
                    Config_temp[username]["token"] = None
                    input_mensaje = 'Privada'
                if input_mensaje == "UCLV":
                    await webmailuclv_api(Temp_dates[username]['file'],user_id,msg,username)
                    return
                if input_mensaje == "MINED":
                    await mined_api(Temp_dates[username]['file'],user_id,msg,username)
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
                    await msg.edit(f"🗂 **ᴄ͟͟ᴏ͟͟ᴍ͟͟ᴘ͟͟ʀ͟͟ɪ͟͟ᴍ͟͟ɪ͟͟ᴇ͟͟ɴ͟͟ᴅ͟͟ᴏ͟͟ ᴇ͟͟ɴ͟͟ ᴢ͟͟ɪ͟͟ᴘ͟͟s͟͟**")
                    files = await bot.loop.run_in_executor(None, sevenzip, Temp_dates[username]['file'], None, zipssize) 
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
                                    print("↪️F͟͟u͟͟n͟͟c͟͟i͟͟ón͟͟ A͟͟c͟͟t͟͟i͟͟v͟͟a͟͟d͟͟a͟͟↩️")
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
                                    print("↘️F͟͟u͟͟n͟͟c͟͟i͟͟ón͟͟ D͟͟e͟͟s͟͟a͟͟c͟͟t͟͟i͟͟v͟͟a͟͟d͟͟a͟͟↙️")
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
                                        await bot.send_message(username,f'[{filenamex}]({upload})')
                                        break
                        except Exception as ex:
                            await msg.edit(ex)
                            return

                if len(files) == len(logslinks):
                    with open(filename+".txt","w") as f:
                        message = ""
                        for li in logslinks:
                            message+=li+"\n"
                        f.write(message)
                    if input_mensaje in login:
                        await bot.send_document(username,filename+".txt",caption=f"👤 {user}\n🔑 {password}\n🔗 {host}\n\n😊 Gracias Por Usar Nuestro Servicio\n#tufutbolista11 #uploadfree #cubaflixmax")
                    else:
                        await bot.send_document(username,filename+".txt",thumb="thumb.png",caption="😊 Gracias Por Usar Nuestro Servicio\n#tufutbolista11 #uploadfree #cubaflixmax")
                    await msg.edit('**⚡️ғɪɴᴀʟɪᴢᴀᴅᴏ ᴄᴏɴ Éxɪᴛᴏ⚡️ᴀǫᴜɪ ᴛɪᴇɴᴇ sᴜ ᴀʀᴄʜɪᴠᴏ ⚡️**')
                    #os.unlink(filename+".txt")
                else:
                    await msg.edit('**❎Ha ocurrido un error❎**')
                return
        else:
            await msg.edit("Elige tu Plan 😉\n\n➧ Plan Básico:\n10 GB de transferencia diaria\n💳90 CUP | 📱 110 CUP\n➧ Plan Estándar: \n20 GB de transferencia diaria\n💳150 CUP | 📱 170 CUP\n➧ Plan Avanzado: \n40 GB de transferencia diaria\n💳200 CUP | 📱 250 CUP\n➧ Plan Premium:  \n80 GB de transferencia diaria\n💳250 CUP | 📱 280 CUP\n\nContacta con: @tufutbolista11")
            return

def uploadfile_progres(chunk,filesize,start,filename,message):
    try:
        now = time()
        diff = now - start
        mbs = chunk / diff
        msg = f"✴💭 ɴᴀᴍᴇ: {filename}\n\n"
        try:
            msg+=update_progress_bar(chunk,filesize)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
        except:pass
        msg+= f"⚡️ ᴜᴘʟᴏᴀᴅɪɴɢ: {sizeof_fmt(chunk)} of {sizeof_fmt(filesize)}\n\n"
        global seg
        if seg != localtime().tm_sec:
            message.edit(msg)
        seg = localtime().tm_sec
    except Exception as e:
        print(str(e))

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

def update_progress_bar(inte,max):
    percentage = inte / max
    percentage *= 100
    percentage = round(percentage)
    hashes = int(percentage / 5)
    spaces = 20 - hashes
    progress_bar = "[ " + "•" * hashes + "•" * spaces + " ]"
    percentage_pos = int(hashes / 1)
    percentage_string = str(percentage) + "%"
    progress_bar = progress_bar[:percentage_pos] + percentage_string + progress_bar[percentage_pos + len(percentage_string):]
    return(progress_bar)

def uploadfile_progres_medisur(chunk,filesize,start,filename,message,ttotal,ttotal_t,tfilename):
    try:
        now = time()
        diff = now - start
        mbs = chunk / diff
        msg = f"💭 ɴᴀᴍᴇ: {tfilename}\n\n"
        chunk = ttotal+chunk
        try:
            msg+=update_progress_bar(chunk,ttotal_t)+ "  " + sizeof_fmt(mbs)+"/s\n\n"
        except:pass
        msg+= f"⚡️ ᴜᴘʟᴏᴀᴅɪɴɢ: {sizeof_fmt(chunk)} of {sizeof_fmt(ttotal_t)}\n\n"
        global seg
        if seg != localtime().tm_sec:
            message.edit(msg)
        seg = localtime().tm_sec
    except Exception as e:
        print("error: ",str(e))

async def webmailuclv_api(file,usid,msg,username,myfiles=False,deleteall=False):
    try:
        print("webmailuclv_api")
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
                                await bot.send_message(username,url)
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


async def mined_api(file,usid,msg,username):
    print("MINED")
    lista = [133,134,135,136,137,138,139,140]
    global COOKIES_DATE
    try:
        msgs = await bot.get_messages(reg_db, message_ids=8)
        d = json.loads(msgs.text)
        try:
            ids = d[username]["id"]
        except:
            await msg.edit("📡 Asignándole un ID de subida ...")
            ids = str(random.choice(lista))
            d[username] = {"id":ids}
            await bot.edit_message_text(reg_db,message_id=8,text=dumps(d,indent=4))
        zipssize=50*1024*1024
        filename = file.split("/")[-1]
        host = "https://tramites.mined.gob.cu/"
        filesize = Path(file).stat().st_size
        print(21)
        file = await file_renamer(file)
        filename = file.split("/")[-1]
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"}
        proxy = None #Configs[username]["gp"]
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
        #login
        msg = await msg.edit("🔴 Conectando ... 🔴")
        connector = aiohttp.TCPConnector()
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(host+"login.php",headers=headers) as resp:
                html = await resp.text()
            soup = BeautifulSoup(html,"html.parser")
            CSRFToken = soup.find("input",attrs={"name":"__CSRFToken__"})["value"]
            payload = {}
            payload["__CSRFToken__"] = CSRFToken
            payload["luser"] = "aidachimilanc@gmail.com"
            payload["lpasswd"] = "Cubaflix1234*"
            async with session.post(host+"login.php",data=payload,headers=headers) as resp:
                if resp.status==200:
                    cookies = session.cookie_jar
                    for co in cookies:
                        COOKIES_DATE = (co.key,co.value)
                    await msg.edit("✅ **CONECTADO** ✅")
                else:
                    await msg.edit("📵 __No se puedo conectar__")
                    return
            #if ids=="":pass
            #upload
            ttotal_t = filesize
            tfilename = filename
            init_time = time()
            links = ""
            links2 = ""
            ttotal = 0
            partes = 0
            if filesize-1048>zipssize:
                await msg.edit(f"📦 **Comprimiendo en zips**")
                files = await bot.loop.run_in_executor(None, sevenzip, file, None, zipssize)
            else:
                files = [file]
            linksz = []
            try:
                async with session.get(host+f"tickets.php?id={ids}",headers=headers) as resp:
                    html = await resp.text()
                CSRF = str(html).split('name="csrf_token" content="')[1].split('"')[0]
                str1 = str(html).split('textarea name="')[1].split('"')[0]
                str2 = str(html).split("maxfilesize: 512")[1].split("[]")[0].split("name: '")[1]+"[]"
                textarea_value = filename+str(randint(10000,999999))
                payload = {}
                payload["__CSRFToken__"] = CSRF
                payload["id"] = str(ids)
                payload["a"] = "reply"
                payload[str1] = f"<p>{textarea_value}</p>"
                payload[str2] = []
                payload["draft_id"] =  ""
                for file in files:
                    fi = Progress(file,lambda current,total,timestart,filename: uploadfile_progres_medisur(current,total,timestart,filename,msg,ttotal,ttotal_t,tfilename))
                    query = {"upload[]":fi}
                    current = Path(file).stat().st_size
                    async with session.post(host+"ajax.php/form/upload/ticket/attach",data=query,headers=headers) as resp:
                        html = await resp.text()
                    data = loads(html)
                    i = data["id"]
                    payload[str2].append(f"{i},{file}")
                    ttotal+=current
                    partes+=1
                async with session.post(host+f"tickets.php?id={ids}",data=payload,headers=headers) as resp:
                    print(resp.status)
                    html = await resp.text()
                await msg.edit("⚒ Contruyendo enlaces </>")
                sleep(5)
                resp = requests.get(host+f"tickets.php?id={ids}",cookies={COOKIES_DATE[0]:COOKIES_DATE[1]},headers=headers)
                soup = BeautifulSoup(resp.text,"html.parser")
                v1 = soup.find_all("div")
                for v in v1:
                    try:
                        tx = v.find('div', attrs={'class': 'thread-body'}).find('p').text
                        if tx==textarea_value:
                            script_tag = v.find('script')
                            script_content = script_tag.string
                            start_index = script_content.find('{')
                            end_index = script_content.rfind('}') + 1
                            json_content = script_content[start_index:end_index]
                            json_data = json.loads(json_content)
                            for key in json_data:
                                url = "https://tramites.mined.gob.cu"+json_data[key]["download_url"]
                                dat = {"name":file.split('/')[-1],"url":url}
                                if not dat in linksz:
                                    linksz.append(dat)
                    except:pass
            except Exception as ex:
                if "index" in str(ex):
                    COOKIES_DATE = ()
                    await msg.edit("❗️ Espera unos segundos y mande a subir el archivo nuevamente")
                    return
                await bot.send_message("tufutbolista11","Up "+str(ex))
                pass
                #os.unlink(file)
            if len(linksz)==0:
                await msg.edit("😔 No se subió ningún archivo")
                return
            end_time = time()
            tiempo_transcurrido = end_time - init_time
            minutos_transcurridos = str(tiempo_transcurrido / 60)
            total_time = minutos_transcurridos[:4]
            if "0." in total_time:
                total_time = total_time + " segundos"
            else:
                total_time = total_time + " minutos"
            await msg.delete()
            #await bot.send_sticker(username,"speed.tgs")
            encript = ""
            n = 0
            for a in linksz:
                encript+=f"➣ {n} [{a['name']}]({a['url']}))\n"
                n+=1
            encripted = short(encript)
            button1 = InlineKeyboardButton("👀 Ver Enlaces ",f"viewurls {encripted}")
            buttons = [[button1]]
            reply_markup = InlineKeyboardMarkup(buttons)
            m = f"🎖 **FINALIZADO** 🎖 \n\n 🎬 `{filename}`\n📦 **Tamaño:** {sizeof_fmt(ttotal_t)}\n⏰ **Subido en {total_time}**\n🗂 **Partes: {partes} de 50 mb**\n🌐 **Host**: {host}login.php\n👤 **User:** `aidachimilanc@gmail.com`\n🔑 **Passw:** Cubaflix1234**\n\n😊 **Gracias Por Usar Nuestro Servicio**\n#tufutbolista11 #uploadfree #cubaflixmax"
            await bot.send_message(username,m,reply_markup=reply_markup)
            message = ""
            for link in linksz:
                message+=f"{link['url']}\n"
            with open(filename+".txt","w") as txt:
                txt.write(message)
            await bot.send_document(usid,filename+".txt",thumb="thumb.png",caption="😊 **Gracias Por Usar Nuestro Servicio**\n#tufutbolista11 #uploadfree #cubaflixmax\n")
    except Exception as e:
        await bot.send_message("tufutbolista11","Mined: "+str(e))

async def dspace_api(file,usid,msg,username):
    try:
        us = "ccgomez"
        p = "Hiran@22"
        ids = "19146"
        zipssize=99*1024*1024
        filename = file.split("/")[-1]
        host = "https://dspace.uclv.edu.cu/"
        filesize = Path(file).stat().st_size
        print(21)
        file = await file_renamer(file)
        filename = file.split("/")[-1]
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"}
        proxy = None #Configs[username]["gp"]
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
        #login
        await msg.edit("⚡️ ᴄᴏɴᴇᴄᴛᴀɴᴅᴏ .... ⚡️")
        connector = aiohttp.TCPConnector()
        async with aiohttp.ClientSession(connector=connector) as session:
            cli = DspaceClient(us,p,ids)
            login = cli.login()
            try:
                if login:
                    await msg.edit("✅ **ᴄᴏɴᴇᴄᴛᴀᴅᴏ** ✅")
                else:
                    await msg.edit("📵 __ɴᴏ sᴇ ᴘᴜᴇᴅᴏ ᴄᴏɴᴇᴄᴛᴀʀ__")
                    return
            except:pass
            if filesize-1048>zipssize:
                await msg.edit(f"📦 **Comprimiendo en zips**")
                files = await bot.loop.run_in_executor(None, sevenzip, file, None, zipssize)
            else:
                files = [file]
            linksz = []
            #await msg.delete()
            for file in files:
                try:
                    filen = file.split('/')[-1]
                    await msg.edit(f"**🔱 ʟᴀ ɴᴜʙᴇ ɴᴏ ᴍᴜᴇsᴛʀᴀ ᴘʀᴏɢʀᴇsᴏ 🔱 ᴘᴇʀᴏ sᴜ ᴀʀᴄʜɪᴠᴏs sᴇ ᴇsᴛᴀ sᴜʙɪᴇɴᴅᴏ ᴀ ʟᴀ ɴᴜʙᴇ ⚡️ {filen}**")
                    upload = await bot.loop.run_in_executor(None, cli.upload, file)
                    await bot.send_message(username,f"**[{filen}]({upload['url']})**")
                    linksz.append(upload['url'])
                    #os.unlink(file)
                except Exception as ex:
                    await bot.send_message(username,"Up "+str(ex))
                    pass
            if len(linksz)==0:
                await msg.edit("😔 No se subió ningún archivo")
                return
            #sawait msg.edit(f"✅ 𝑭𝒊𝒏𝒂𝒍𝒊𝒛𝒂𝒅𝒐 𝒆𝒙𝒊𝒕𝒐𝒔𝒂𝒎𝒆𝒏𝒕𝒆")
            await msg.delete()
            message = ""
            for link in linksz:
                message+=f"{link}\n"
            with open(filename+".txt","w") as txt:
                txt.write(message)
            await bot.send_document(usid,filename+".txt",caption=f"👤 {us}\n🔑 {p}🔗 {host}\n\n😊 **Gracias Por Usar Nuestro Servicio**\n#tufutbolista11 #uploadfree #cubaflixmax\n")
    except Exception as e:
        await bot.send_message(username,"DSPACE- "+str(e))
    return

async def medisur_api(file,usid,msg,username):
	try:
		zipssize=15*1024*1024
		filename = file.split("/")[-1]
		host = "https://medisur.sld.cu/index.php/medisur/"
		filesize = Path(file).stat().st_size
		print(21)
		proxy = None #Configs[username]["gp"]
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}
		#login
		msg = await msg.edit("💠 𝕮͟͟𝖔͟͟𝖓͟͟𝖊͟͟𝖈͟͟𝖙͟͟𝖆͟͟𝖓͟͟𝖉͟͟𝖔͟͟ 𝖆͟͟𝖑͟͟ 𝖘͟͟𝖊͟͟𝖗͟͟𝖛͟͟𝖎͟͟𝖉͟͟𝖔͟͟𝖗͟͟ ... 💠")
		connector = aiohttp.TCPConnector()
		async with aiohttp.ClientSession(connector=connector) as session:
			payload = payload = {}
			payload["source"] = "/index.php/medisur/user/profile"
			payload["username"] = "cubaflix"
			payload["password"] = "Cubaflix1234*"
			async with session.post(host+"login/signIn", data=payload) as e:
				print(222)
			#upload
			if filesize-1048>zipssize:
				parts = round(filesize / zipssize)
				await msg.edit(f"🔰 𝕮𝖔𝖒𝖕𝖗𝖎𝖒𝖎𝖊𝖓𝖉𝖔\n\n🏷 Total: {parts} partes\n")
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
				await msg.edit(f"🔱 𝕱𝖎𝖓𝖆𝖑𝖎𝖟𝖆𝖉𝖔 𝕰𝖝𝖎𝖙𝖔𝖘𝖆𝖒𝖊𝖓𝖙𝖊✨𝕴𝖔𝖒𝖊 𝖘𝖚 𝕬𝖗𝖈𝖍𝖎𝖛𝖔 🔱 \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
				txtname = file.split('.')[0].replace(' ','_')+'.txt'
				with open(txtname,"w") as t:
					message = ""
					for li in links:
						message+=li+"\n"
					t.write(message)
					t.close()
				await bot.send_document(usid,txtname)
			else:
				await msg.edit("♻️ S͛uͧвⷡⷡiͥeͤndͩoͦ eͤl Aͣrͬcͨhͪiͥvͮoͦ Aͣl S͛eͤrͬvͮiͥdͩoͦrͬ ♻️")
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
					await msg.edit(f"💠 𝕱𝖎𝖓𝖆𝖑𝖎𝖟𝖆𝖉𝖔 𝕰𝖝𝖎𝖙𝖔𝖘𝖆𝖒𝖊𝖓𝖙𝖊✨𝕴𝖔𝖒𝖊 𝖘𝖚 𝕬𝖗𝖈𝖍𝖎𝖛𝖔 💠 \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
					txtname = file.split('.')[0].replace(' ','_')+'.txt'
					with open(txtname,"w") as t:
						t.write(url)
						t.close()
					await bot.send_document(usid,txtname)
	except Exception as e:
		print(str(e))

def generate():
    prefix = "web-file-upload-"
    random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))
    unique_id = str(uuid.uuid4().time_low)

    random_name = f"{prefix}{random_string}-{unique_id}"
    return random_name

async def webdav(file,usid,msg,username):
    try:
        await save_logs("webdav")
        proxy = DB_global['Proxy_Global']
        user = "denia.rivero"
        password = "ContraseñaUpload1234*"
        host = "https://nube.uo.edu.cu/"
        if proxy:
            proxy = aiohttp_socks.ProxyConnector.from_url(f"{proxy}",ssl=False)
        else:
            proxy = aiohttp.TCPConnector(ssl=False)
        file = await file_renamer(file)
        filename = file.split("/")[-1]
        filesize = Path(file).stat().st_size
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
        async with aiohttp.ClientSession(connector=proxy) as session:
            await save_logs(1)
            ids = "E88DF8CD-154A-4B85-A255-B162C8632F3A"
            await msg.edit(f"Conectando 🔴")
            #login
            async with session.get(host+"index.php/login",headers=headers) as resp:
                html = await resp.text()
            soup = BeautifulSoup(html,'html.parser')
            requesttoken = soup.find('head')['data-requesttoken']
            await save_logs(requesttoken)
            timezone = 'America/Mexico_City'
            timezone_offset = '-5'
            payload = {'user':user,'password':password,'timezone':timezone,'timezone_offset':timezone_offset,'requesttoken':requesttoken}
            async with session.post(host+"index.php/login",data=payload,headers=headers) as resp:
                await save_logs(f"login {resp.status}")
            #cookies = await bot.get_messages(-1001994829316,message_ids=2)
            #cookies = json.loads(cookies.text)
            #session.cookie_jar.update_cookies(cookies["uo"])
            async with session.get(host+"index.php/apps/files/") as resp:
                html = await resp.text()
                await save_logs(f"get_files {resp.status}")
            soup = BeautifulSoup(html,'html.parser')
            requesttoken = soup.find('head')['data-requesttoken']
            async with session.put(host+"apps/user_status/heartbeat",data={"status": "away"},headers={"requesttoken":requesttoken}) as resp:
                await save_logs(f"heartbeat {resp.status}")
            await msg.edit(f"Conectado 🟢")

            #data = await bot.get_messages(-1001994829316,message_ids=2)
            #data = json.loads(data.text)
            #cookies = session.cookie_jar
            #c = ["oc_sessionPassphrase","oc6bl3nmmgyx"]
            #if not "uo" in data:
            #    data["uo"] = {}
            #for cookie in cookies:
            #    if cookie.key in c:
            #        data["uo"].update({cookie.key:cookie.value})
            #await bot.edit_message_text(-1001994829316,message_id=2,text=dumps(data,indent=4))
            #login
            try:
                webdav_url = host+"remote.php/dav/uploads/"+ids+"/"+ generate()
                await save_logs(webdav_url)
                try:
                    async with session.request("MKCOL", webdav_url,headers={"requesttoken":requesttoken,**headers}) as resp:
                        await save_logs("MKCOL "+str(resp.status))
                except:
                    await msg.edit("Este servidor está temporalmente fuera de servicio [await_please]")
                    return
                await save_logs("up_webdav")
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
                    await save_logs("Finalizado")
                    await msg.edit("✅ **Finalizado** ✅")
                    u = webdav_url+"/.file"
                    u = f"{usid}\nuo\n{filename}\n{filesize}\n{u}"
                    u = short(u)
                    u = f"script {u}"
                    button1 = InlineKeyboardButton("📲 Descargar Archivo",u)
                    buttons = [[button1]]
                    reply_markup = InlineKeyboardMarkup(buttons)
                    await msg.edit(f"✅ **Finalizado** ✅\n📂  [{filename}]({u})\n❄️ **Tamaño:** {sizeof_fmt(filesize)}",reply_markup=reply_markup)
                    complete = False
            except Exception as ex:
                await save_logs(ex)
    except Exception as ex:
        await save_logs(str(ex))

seg_chunk = 0
def uploadfile_progres_chunk(chunk,filesize,start,filename,size_zip,message,username):
    if chunk == size_zip and sizes_reads[username]['size'] == 0:
        sizes_reads[username]['size'] = chunk
    elif chunk == size_zip and sizes_reads[username]['size'] != 0:
        sizes_reads[username]['size'] += chunk
    current_size = sizes_reads[username]['size'] + chunk
    now = time()
    diff = now - start
    mbs = chunk / diff
    barra = update_progress_bar(current_size,filesize)
    msg = f"🔼 𝚄𝚙𝚕𝚘𝚊𝚍𝚒𝚗𝚐 \n\n𝐍𝐚𝐦𝐞: `{filename}`\n\n{barra} **{sizeof_fmt(mbs)}/s** \n\n▶️ **{sizeof_fmt(current_size)}** of **{sizeof_fmt(filesize)}** "
    global seg_chunk
    if seg_chunk != localtime().tm_sec:
        message.edit(msg,reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancel","cancel")]]))
    seg_chunk = localtime().tm_sec

async def sysmined_api(file,usid,msg,username):
    try:
        await save_logs("sysmined")
        proxy = DB_global['Proxy_Global']
        host = "https://bienestar-apmined.xutil.net/"
        proxy = aiohttp_socks.ProxyConnector.from_url(f"{proxy}")
        file = await file_renamer(file)
        filename = file.split("/")[-1]
        filename_chunk = filename
        filesize = Path(file).stat().st_size
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
        async with aiohttp.ClientSession(connector=proxy) as session:
            await save_logs(1)
            await msg.edit("🔰 𝙲𝚘𝚖𝚙𝚛𝚒𝚖𝚒𝚎𝚗𝚍𝚘")
            files = await bot.loop.run_in_executor(None, rar_compress , Path(file), 19*1024*1024, username)
            if len(files)==0:
                await msg.edit("**No Hay Archivos a Subir**")
                return
            await msg.edit("**CONECTANDO ...**")
            sizes_reads[username] = {"size":0}
            async with session.get(host+"sysapmined/esES/neoclassic/6902013625da0ea90dfda60075811440/3894003075da0ea916ee314054459690.php",headers={"Upgrade-Insecure-Requests":"1",**headers}) as resp:
                await save_logs(resp.status)
            async with session.get(host+"sysapmined/esES/neoclassic/services/webentry/anonymousLogin?we_uid=5819359306473f170cb9eb1049011769",headers={"Upgrade-Insecure-Requests":"1",**headers}) as resp:
                await save_logs(resp.status)
            async with session.get(host+"sysapmined/esES/neoclassic/cases/cases_Open?APP_UID=81475984365760ce3e22133018715878&DEL_INDEX=1&action=draft",headers={"Upgrade-Insecure-Requests":"1",**headers}) as resp:
                html = await resp.text()
            accessToken = str(html).split('{"accessToken":"')[1].split('"')[0]
            links = []
            for file in files:
                try:
                    fi = Progress(file,lambda chunk,total,start,filename: uploadfile_progres_chunk(chunk,filesize,start,filename_chunk,total,msg,username))
                    query = {"form[]":fi}
                    async with session.post(host+"api/1.0/apmined/case/7521856476567e9be279022093933770/upload/file_archivos_asunto",data=query,headers={"Authorization":f"Bearer {accessToken}","X-Requested-With":"XMLHttpRequest",**headers}) as resp:
                        html = await resp.text()
                    data = json.loads(html)
                    u = f"{host}sysapmined/en/%7Bskin%7D/cases/cases_ShowDocument?a={data[0]['appDocUid']}&v=1"
                    os.unlink(file)
                    button1 = InlineKeyboardButton("⬇️ Descargar Enlace ⬇️",url=u)
                    buttons = [[button1]]
                    reply_markup = InlineKeyboardMarkup(buttons)
                    await bot.send_message(username,f"📂  [{file.split('/')[-1]}]({u})",reply_markup=reply_markup)
                    links.append(u)
                except Exception as e:
                    await save_logs(str(e))
                    pass
            await msg.delete()
            await bot.send_message(username,f"💠 𝕱𝖎𝖓𝖆𝖑𝖎𝖟𝖆𝖉𝖔 𝕰𝖝𝖎𝖙𝖔𝖘𝖆𝖒𝖊𝖓𝖙𝖊✨𝕴𝖔𝖒𝖊 𝖘𝖚 𝕬𝖗𝖈𝖍𝖎𝖛𝖔 💠")
            txtname = file.split('.')[0].replace(' ','_')+'.txt'
            with open(txtname,"w") as t:
                message = ""
                for li in links:
                    message+=li+"\n"
                t.write(message)
                t.close()
            await bot.send_document(usid,txtname,thumb="thumb.png")
            os.unlink(txtname)
    except Exception as ex:
        await save_logs(str(ex))

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
		msg = await msg.edit("💠 𝕮͟͟𝖔͟͟𝖓͟͟𝖊͟͟𝖈͟͟𝖙͟͟𝖆͟͟𝖓͟͟𝖉͟͟𝖔͟͟ 𝖆͟͟𝖑͟͟ 𝖘͟͟𝖊͟͟𝖗͟͟𝖛͟͟𝖎͟͟𝖉͟͟𝖔͟͟𝖗͟͟ ... 💠")
		connector = aiohttp.TCPConnector()
		if proxy:
			connector = aiohttp_socks.ProxyConnector.from_url(proxy)
		async with aiohttp.ClientSession(connector=connector) as session:
			payload = payload = {}
			payload["F_UserName"] = "Cubaflix3"
			payload["F_Password"] = "Upload1234*"
			async with session.post(host+"index.php?P=UserLogin", data=payload,headers=headers) as e:
				print(222)
				print(e.url)
			#upload
			if filesize-1048>zipssize:
				parts = round(filesize / zipssize)
				await msg.edit(f"🔰 𝙲𝚘𝚖𝚙𝚛𝚒𝚖𝚒𝚎𝚗𝚍𝚘\n\n🏷 Total: {parts} partes\n")
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
				await msg.edit(f"💠 𝕱𝖎𝖓𝖆𝖑𝖎𝖟𝖆𝖉𝖔 𝕰𝖝𝖎𝖙𝖔𝖘𝖆𝖒𝖊𝖓𝖙𝖊✨𝕴𝖔𝖒𝖊 𝖘𝖚 𝕬𝖗𝖈𝖍𝖎𝖛𝖔 💠 \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
				txtname = file.split('.')[0].replace(' ','_')+'.txt'
				with open(txtname,"w") as t:
					message = ""
					for li in links:
						message+=li+"\n"
					t.write(message)
					t.close()
				await bot.send_document(usid,txtname,caption="➪ U͓̽s͓̽u͓̽a͓̽r͓̽i͓̽o͓̽: `Cubaflix3`\n➪ C͓̽o͓̽n͓̽t͓̽r͓̽a͓̽s͓̽e͓̽ña͓̽: `Upload1234*`")
				os.unlink(txtname)
			else:
				print(111)
				h = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8","Accept-Encoding":"deflate","Accept-Language":"en-US,en;q=0.5","Connection":"keep-alive","User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
				await msg.edit("🔱 S͛uͧвⷡⷡiͥeͤndͩoͦ eͤl Aͣrͬcͨhͪiͥvͮoͦ Aͣl S͛eͤrͬvͮiͥdͩoͦrͬ 🔱")
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
							await msg.edit(f"💠 𝕱𝖎𝖓𝖆𝖑𝖎𝖟𝖆𝖉𝖔 𝕰𝖝𝖎𝖙𝖔𝖘𝖆𝖒𝖊𝖓𝖙𝖊✨𝕴𝖔𝖒𝖊 𝖘𝖚 𝕬𝖗𝖈𝖍𝖎𝖛𝖔 💠 \n\n{file.split('/')[-1]}\n[ .txt ] ⤵️")
							txtname = file.split('.')[0].replace(' ','_')+'.txt'
							with open(txtname,"w") as t:
								t.write(url)
							t.close()
							await bot.send_document(usid,txtname,caption="➪ U͓̽s͓̽u͓̽a͓̽r͓̽i͓̽o͓̽: `Cubaflix3`\n➪ C͓̽o͓̽n͓̽t͓̽r͓̽a͓̽s͓̽e͓̽ña͓̽: `Upload1234*`")
							os.unlink(txtname)
					except:
						pass
	except Exception as e:
		print(str(e))

async def uploads_options(filename, filesize, username):
    buttons = [
        [InlineKeyboardButton("🤩☁️UO☁️🤩","UO")],
        [InlineKeyboardButton("🤩☁️MINED☁️🤩","MINED")],
        [InlineKeyboardButton("⚡️☁GTM☁⚡️","GTM")],
        [InlineKeyboardButton("⚡️☁UCM☁⚡️","UCM")],
        [InlineKeyboardButton("⚡️☁UCLV☁⚡️","UCLV")],
        [InlineKeyboardButton("⚡️☁LTU☁⚡️","LTU")],
        [InlineKeyboardButton("⚡️☁️ DSPACE ☁️⚡️","DSPACE")],
        [InlineKeyboardButton("⚡️☁️ AULAENSAP ☁️⚡️","AULAENSAP")],
        [InlineKeyboardButton("⚡️♻PRIVADA♻⚡️","PRIVADA")]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await bot.send_message(username,f'Seleccione el Modo de Subida:\n📕Nombre: {filename.split("/")[-1]}\n📦Tamaño: {sizeof_fmt(filesize)}',reply_markup=reply_markup)
#Run...
try:
    os.unlink("bot.session")
except:pass
try:
    os.unlink("bot.session-journal")
except:pass
print("started")
bot.start()
bot.loop.run_forever()