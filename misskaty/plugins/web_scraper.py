"""
 * @author        yasir <yasiramunandar@gmail.com>
 * @date          2022-12-01 09:12:27
 * @lastModified  2023-01-11 12:23:31
 * @projectName   MissKatyPyro
 * Copyright @YasirPedia All rights reserved
"""
import re
import logging
from bs4 import BeautifulSoup
from pykeyboard import InlineKeyboard, InlineButton
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from misskaty.helper.http import http
from misskaty import app
from misskaty.vars import COMMAND_HANDLER
from misskaty.core.message_utils import *

__MODULE__ = "WebScraper"
__HELP__ = """
/melongmovie - Scrape website data from MelongMovie Web. If without query will give latest movie list.
/lk21 [query <optional>] - Scrape website data from LayarKaca21. If without query will give latest movie list.
/pahe [query <optional>] - Scrape website data from Pahe.li. If without query will give latest post list.
/terbit21 [query <optional>] - Scrape website data from Terbit21. If without query will give latest movie list.
/savefilm21 [query <optional>] - Scrape website data from Savefilm21. If without query will give latest movie list.
/movieku [query <optional>] - Scrape website data from Movieku.cc
/nodrakor [query] - Scrape website data from nodrakor.icu
/zonafilm [query] - Scrape website data from zonafilm.icu
/gomov [query <optional>] - Scrape website data from GoMov. If without query will give latest movie list.
"""

headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}

LOGGER = logging.getLogger(__name__)
SCRAP_DICT = {} # Dict for Pahe, Terbit21, LK21

def split_arr(arr, size: 5):
     arrs = []
     while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
     arrs.append(arr)
     return arrs

# Terbit21 GetData
async def getDataTerbit21(msg, kueri, CurrentPage):
    if not SCRAP_DICT.get(msg.id):
        if not kueri:
            terbitjson = (await http.get('https://yasirapi.eu.org/terbit21')).json()
        else:
            terbitjson = (await http.get(f'https://yasirapi.eu.org/terbit21?q={kueri}')).json()
        if not terbitjson.get("result"):
            return await msg.edit("Sorry, could not find any results!")
        SCRAP_DICT[msg.id] = [split_arr(terbitjson["result"], 6), kueri]
    try:
        index = int(CurrentPage - 1)
        PageLen = len(SCRAP_DICT[msg.id][0])
        
        if kueri:
            TerbitRes = f"<b>#Terbit21 Results For:</b> <code>{kueri}</code>\n\n"
        else:
            TerbitRes = "<b>#Terbit21 Latest:</b>\n🌀 Use /terbit21 [title] to start search with title.\n\n"
        for c, i in enumerate(SCRAP_DICT[msg.id][0][index], start=1):
            TerbitRes += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Category:</b> <code>{i['kategori']}</code>\n"
            TerbitRes += "\n" if re.search(r"Complete|Ongoing", i["kategori"]) else f"💠 <b><a href='{i['dl']}'>Download</a></b>\n\n"
        IGNORE_CHAR = "[]"
        TerbitRes = ''.join(i for i in TerbitRes if not i in IGNORE_CHAR)
        return TerbitRes, PageLen
    except (IndexError, KeyError):
        await msg.edit("Sorry, could not find any results!")

# LK21 GetData
async def getDatalk21(msg, kueri, CurrentPage):
    if not SCRAP_DICT.get(msg.id):
        if not kueri:
            lk21json = (await http.get('https://yasirapi.eu.org/lk21')).json()
        else:
            lk21json = (await http.get(f'https://yasirapi.eu.org/lk21?q={kueri}')).json()
        if not lk21json.get("result"):
            return await msg.edit("Sorry could not find any matching results!")
        SCRAP_DICT[msg.id] = [split_arr(lk21json["result"], 6), kueri]
    try:
        index = int(CurrentPage - 1)
        PageLen = len(SCRAP_DICT[msg.id][0])
        
        if kueri:
            lkResult = f"<b>#Layarkaca21 Results For:</b> <code>{kueri}</code>\n\n"
        else:
            lkResult = "<b>#Layarkaca21 Latest:</b>\n🌀 Use /lk21 [title] to start search with title.\n\n"
        for c, i in enumerate(SCRAP_DICT[msg.id][0][index], start=1):
            lkResult += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Category:</b> <code>{i['kategori']}</code>\n"
            lkResult += "\n" if re.search(r"Complete|Ongoing", i["kategori"]) else f"💠 <b><a href='{i['dl']}'>Download</a></b>\n\n"
        IGNORE_CHAR = "[]"
        lkResult = ''.join(i for i in lkResult if not i in IGNORE_CHAR)
        return lkResult, PageLen
    except (IndexError, KeyError):
        await msg.edit("Sorry could not find any matching results!")

# Pahe GetData
async def getDataPahe(msg, kueri, CurrentPage):
    if not SCRAP_DICT.get(msg.id):
        pahejson = (await http.get(f'https://yasirapi.eu.org/pahe?q={kueri}')).json()
        if not pahejson.get("result"):
            return await msg.edit("Sorry could not find any matching results!", quote=True)
        SCRAP_DICT[msg.id] = [split_arr(pahejson["result"], 6), kueri]
    try:
        index = int(CurrentPage - 1)
        PageLen = len(SCRAP_DICT[msg.id][0])
        
        paheResult = f"<b>#Pahe Results For:</b> <code>{kueri}</code>\n\n" if kueri else f"<b>#Pahe Latest:</b>\n🌀 Use /pahe [title] to start search with title.\n\n"
        for c, i in enumerate(SCRAP_DICT[msg.id][0][index], start=1):
            paheResult += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n\n"
        IGNORE_CHAR = "[]"
        paheResult = ''.join(i for i in paheResult if not i in IGNORE_CHAR)
        return paheResult, PageLen
    except (IndexError, KeyError):
        await msg.edit("Sorry could not find any matching results!")

# MelongMovie GetData
async def getDataMelong(msg, kueri, CurrentPage):
    if not SCRAP_DICT.get(msg.id):
        data = await http.get(f'http://167.99.31.48/?s={kueri}', headers=headers)
        bs4 = BeautifulSoup(data.text, "lxml")
        melongdata = []
        for res in bs4.select(".box"):
            dd = res.select("a")
            url = dd[0]["href"]
            title = dd[0]["title"]
            try:
                quality = dd[0].find(class_="quality").text
            except:
                quality = "N/A"
            melongdata.append({"judul": title, "link": url, "quality": quality})
        if not melongdata:
            return await msg.reply("Sorry could not find any results!", quote=True)
        SCRAP_DICT[msg.id] = [split_arr(melongdata, 6), kueri]
    try:
        index = int(CurrentPage - 1)
        PageLen = len(SCRAP_DICT[msg.id][0])
        
        melongResult = f"<b>#MelongMovie Latest:</b>\n🌀 Use /{msg.command[0]} [title] to start search with title.\n\n"
        for c, i in enumerate(SCRAP_DICT[msg.id][0][index], start=1):
            melongResult += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Quality:</b> {i['quality']}\n<b>Extract:</b> <code>/{msg.command[0]}_scrap {i['link']}</code>\n\n"
        IGNORE_CHAR = "[]"
        melongResult = ''.join(i for i in melongResult if not i in IGNORE_CHAR)
        return melongResult, PageLen
    except (IndexError, KeyError):
        await msg.edit("Sorry could not find any matching results!")

# Zonafilm GetData
async def getDataZonafilm(msg, kueri, CurrentPage):
    if not SCRAP_DICT.get(msg.id):
        zonafilm = await http.get(f'https://zonafilm.icu/?s={kueri}', headers=headers)
        text = BeautifulSoup(zonafilm.text, "lxml")
        entry = text.find_all(class_="entry-header")
        if "Nothing Found" in entry[0].text:
            if not kueri:
                return await msg.edit("404 Not FOUND!")
            else:
                return await msg.edit(f"404 Not FOUND For: {kueri}")
        data = []
        for i in entry:
            genre = i.find(class_="gmr-movie-on").text
            genre = f"{genre}" if genre != "" else "N/A"
            judul = i.find(class_="entry-title").find("a").text
            link = i.find(class_="entry-title").find("a").get("href")
            data.append({"judul": judul, "link": link, "genre": genre})
        SCRAP_DICT[msg.id] = [split_arr(data, 6), kueri]
    try:
        index = int(CurrentPage - 1)
        PageLen = len(SCRAP_DICT[msg.id][0])
        
        ZonafilmResult = f"<b>#Zonafilm Results For:</b> <code>{kueri}</code>\n\n" if kueri else f"<b>#Zonafilm Latest:</b>\n🌀 Use /zonafilm [title] to start search with title.\n\n"
        for c, i in enumerate(SCRAP_DICT[msg.id][0][index], start=1):
            ZonafilmResult += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Genre:</b> <code>{i['genre']}</code>\n"
            ZonafilmResult += f"<b>Extract:</b> <code>/zonafilm_scrap {i['link']}</code>\n\n" if "/tv/" not in i["link"] else "\n"
        IGNORE_CHAR = "[]"
        ZonafilmResult = ''.join(i for i in ZonafilmResult if not i in IGNORE_CHAR)
        return ZonafilmResult, PageLen
    except (IndexError, KeyError):
        await msg.edit("Sorry could not find any matching results!")

# GoMov GetData
async def getDataGomov(msg, kueri, CurrentPage):
    if not SCRAP_DICT.get(msg.id):
        gomovv = await http.get(f'https://185.173.38.216/?s=', headers=headers)
        text = BeautifulSoup(gomovv.text, "lxml")
        entry = text.find_all(class_="entry-header")
        if "Nothing Found" in entry[0].text:
            if not kueri:
                return await msg.edit("404 Not FOUND!")
            else:
                return await msg.edit(f"404 Not FOUND For: {kueri}")
        data = []
        for i in entry:
            genre = i.find(class_="gmr-movie-on").text
            genre = f"{genre}" if genre != "" else "N/A"
            judul = i.find(class_="entry-title").find("a").text
            link = i.find(class_="entry-title").find("a").get("href")
            data.append({"judul": judul, "link": link, "genre": genre})
        SCRAP_DICT[msg.id] = [split_arr(data, 6), kueri]
    try:
        index = int(CurrentPage - 1)
        PageLen = len(SCRAP_DICT[msg.id][0])
        
        gomovResult = f"<b>#Gomov Results For:</b> <code>{kueri}</code>\n\n" if kueri else f"<b>#Gomov Latest:</b>\n🌀 Use /gomov [title] to start search with title.\n\n"
        for c, i in enumerate(SCRAP_DICT[msg.id][0][index], start=1):
            gomovResult += f"<b>{c}. <a href='{i['link']}'>{i['judul']}</a></b>\n<b>Genre:</b> <code>{i['genre']}</code>\n"
            gomovResult += "\n" if re.search(r"Series", i["genre"]) else f"<b>Extract:</b> <code>/gomov_scrap {i['link']}</code>\n\n"
        IGNORE_CHAR = "[]"
        gomovResult = ''.join(i for i in gomovResult if not i in IGNORE_CHAR)
        return gomovResult, PageLen
    except (IndexError, KeyError):
        await msg.edit("Sorry could not find any matching results!")

# Terbit21 CMD
@app.on_message(filters.command(['terbit21'], COMMAND_HANDLER))
async def terbit21_s(client, message):
    kueri = ' '.join(message.command[1:])
    if not kueri:
        kueri = None
    pesan = await message.reply("Getting data from Terbit21..")
    CurrentPage = 1
    terbitres, PageLen = await getDataTerbit21(pesan, kueri, CurrentPage)
    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_terbit21#{number}' + f'#{pesan.id}#{message.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{message.from_user.id}")
    )
    await editPesan(pesan, terbitres, reply_markup=keyboard)

# LK21 CMD
@app.on_message(filters.command(['lk21'], COMMAND_HANDLER))
async def lk21_s(client, message):
    chat_id = message.chat.id 
    kueri = ' '.join(message.command[1:])
    if not kueri:
        kueri = None
    pesan = await message.reply("Getting data from LK21..")
    CurrentPage = 1
    lkres, PageLen = await getDatalk21(pesan, kueri, CurrentPage)
    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_lk21#{number}' + f'#{pesan.id}#{message.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{message.from_user.id}")
    )
    await editPesan(pesan, lkres, reply_markup=keyboard)

# Pahe CMD
@app.on_message(filters.command(['pahe'], COMMAND_HANDLER))
async def pahe_s(client, message):
    chat_id = message.chat.id 
    kueri = ' '.join(message.command[1:])
    if not kueri:
        kueri = ""
    pesan = await message.reply("Getting data from Pahe Web..")
    CurrentPage = 1
    paheres, PageLen = await getDataPahe(pesan, kueri, CurrentPage)
    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_pahe#{number}' + f'#{pesan.id}#{message.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{message.from_user.id}")
    )
    await editPesan(pesan, paheres, reply_markup=keyboard)

# Gomov CMD
@app.on_message(filters.command(['gomov'], COMMAND_HANDLER))
async def gomov_s(client, message):
    kueri = ' '.join(message.command[1:])
    if not kueri:
        kueri = ""
    pesan = await message.reply("Getting data from Gomov Web..")
    CurrentPage = 1
    gomovres, PageLen = await getDataGomov(pesan, kueri, CurrentPage)
    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_gomov#{number}' + f'#{pesan.id}#{message.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{message.from_user.id}")
    )
    await editPesan(pesan, gomovres, reply_markup=keyboard)

# Zonafilm CMD
@app.on_message(filters.command(['zonafilm'], COMMAND_HANDLER))
async def zonafilm_s(client, message):
    kueri = ' '.join(message.command[1:])
    if not kueri:
        kueri = ""
    pesan = await message.reply("Getting data from Zonafilm Web..")
    CurrentPage = 1
    zonafilmres, PageLen = await getDataZonafilm(pesan, kueri, CurrentPage)
    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_zonafilm#{number}' + f'#{pesan.id}#{message.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{message.from_user.id}")
    )
    await editPesan(pesan, zonafilmres, reply_markup=keyboard)

# MelongMovie CMD
@app.on_message(filters.command(['melongmovie'], COMMAND_HANDLER))
async def melong_s(client, message):
    kueri = ' '.join(message.command[1:])
    if not kueri:
        kueri = ""
    pesan = await message.reply("Getting data from Melongmovie..")
    CurrentPage = 1
    melongres, PageLen = await getDataMelong(pesan, kueri, CurrentPage)
    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_melong#{number}' + f'#{pesan.id}#{message.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{message.from_user.id}")
    )
    await editPesan(pesan, melongres, reply_markup=keyboard)

# Terbit21 Page Callback
@app.on_callback_query(filters.create(lambda _, __, query: 'page_terbit21#' in query.data))
async def terbit21page_callback(client, callback_query):
    if callback_query.from_user.id != int(callback_query.data.split('#')[3]):
        return await callback_query.answer("Not yours..", True)
    message_id = int(callback_query.data.split('#')[2])
    CurrentPage = int(callback_query.data.split('#')[1])
    try:
        kueri = SCRAP_DICT[message_id][1]
    except KeyError:
        return await callback_query.answer("Invalid callback data, please send CMD again..")

    try:
        terbitres, PageLen = await getDataTerbit21(callback_query.message, kueri, CurrentPage)
    except TypeError:
        return

    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_terbit21#{number}' + f'#{message_id}#{callback_query.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{callback_query.from_user.id}")
    )
    await editPesan(callback_query.message, terbitres, reply_markup=keyboard)

@app.on_callback_query(filters.create(lambda _, __, query: 'page_melong#' in query.data))
async def melongpage_callback(client, callback_query):
    if callback_query.from_user.id != int(callback_query.data.split('#')[3]):
        return await callback_query.answer("Not yours..", True)
    message_id = int(callback_query.data.split('#')[2])
    CurrentPage = int(callback_query.data.split('#')[1])
    try:
        kueri = SCRAP_DICT[message_id][1]
    except KeyError:
        return await callback_query.answer("Invalid callback data, please send CMD again..")

    try:
        terbitres, PageLen = await getDataMelong(callback_query.message, kueri, CurrentPage)
    except TypeError:
        return

    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_melong#{number}' + f'#{message_id}#{callback_query.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{callback_query.from_user.id}")
    )
    await editPesan(callback_query.message, terbitres, reply_markup=keyboard)

# Lk21 Page Callback
@app.on_callback_query(filters.create(lambda _, __, query: 'page_lk21#' in query.data))
async def lk21page_callback(client, callback_query):
    if callback_query.from_user.id != int(callback_query.data.split('#')[3]):
        return await callback_query.answer("Not yours..", True)
    message_id = int(callback_query.data.split('#')[2])
    CurrentPage = int(callback_query.data.split('#')[1])
    try:
        kueri = SCRAP_DICT[message_id][1]
    except KeyError:
        return await callback_query.answer("Invalid callback data, please send CMD again..")

    try:
        lkres, PageLen = await getDatalk21(callback_query.message, kueri, CurrentPage)
    except TypeError:
        return

    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_lk21#{number}' + f'#{message_id}#{callback_query.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{callback_query.from_user.id}")
    )
    await editPesan(callback_query.message, lkres, reply_markup=keyboard)

# Pahe Page Callback
@app.on_callback_query(filters.create(lambda _, __, query: 'page_pahe#' in query.data))
async def pahepage_callback(client, callback_query):
    if callback_query.from_user.id != int(callback_query.data.split('#')[3]):
        return await callback_query.answer("Not yours..", True)
    message_id = int(callback_query.data.split('#')[2])
    CurrentPage = int(callback_query.data.split('#')[1])
    try:
        kueri = SCRAP_DICT[message_id][1]
    except KeyError:
        return await callback_query.answer("Invalid callback data, please send CMD again..")

    try:
        lkres, PageLen = await getDataPahe(callback_query.message, kueri, CurrentPage)
    except TypeError:
        return

    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_pahe#{number}' + f'#{message_id}#{callback_query.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{callback_query.from_user.id}")
    )
    await editPesan(callback_query.message, lkres, reply_markup=keyboard)

# Gomov Page Callback
@app.on_callback_query(filters.create(lambda _, __, query: 'page_gomov#' in query.data))
async def gomovpage_callback(client, callback_query):
    if callback_query.from_user.id != int(callback_query.data.split('#')[3]):
        return await callback_query.answer("Not yours..", True)
    message_id = int(callback_query.data.split('#')[2])
    CurrentPage = int(callback_query.data.split('#')[1])
    try:
        kueri = SCRAP_DICT[message_id][1]
    except KeyError:
        return await callback_query.answer("Invalid callback data, please send CMD again..")

    try:
        gomovres, PageLen = await getDataGomov(callback_query.message, kueri, CurrentPage)
    except TypeError:
        return

    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_gomov#{number}' + f'#{message_id}#{callback_query.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{callback_query.from_user.id}")
    )
    await editPesan(callback_query.message, gomovres, reply_markup=keyboard)

@app.on_callback_query(filters.create(lambda _, __, query: 'page_zonafilm#' in query.data))
async def zonafilmpage_callback(client, callback_query):
    if callback_query.from_user.id != int(callback_query.data.split('#')[3]):
        return await callback_query.answer("Not yours..", True)
    message_id = int(callback_query.data.split('#')[2])
    CurrentPage = int(callback_query.data.split('#')[1])
    try:
        kueri = SCRAP_DICT[message_id][1]
    except KeyError:
        return await callback_query.answer("Invalid callback data, please send CMD again..")

    try:
        zonafilmres, PageLen = await getDataZonafilm(callback_query.message, kueri, CurrentPage)
    except TypeError:
        return

    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, 'page_gomov#{number}' + f'#{message_id}#{callback_query.from_user.id}')
    keyboard.row(
        InlineButton("❌ Close", f"close#{callback_query.from_user.id}")
    )
    await editPesan(callback_query.message, zonafilmres, reply_markup=keyboard)

### Scrape DDL Link From Web ###

# Savefilm21 DDL
@app.on_message(filters.command(["savefilm21_scrap"], COMMAND_HANDLER))
async def savefilm21_scrap(_, message):
    try:
        link = message.text.split(" ", maxsplit=1)[1]
        html = await http.get(link, headers=headers)
        soup = BeautifulSoup(html.text, "lxml")
        res = soup.find_all(class_="button button-shadow")
        res = "".join(f"{i.text}\n{i['href']}\n\n" for i in res)
        await message.reply(
            f"<b>Hasil Scrap dari {link}</b>:\n\n{res}",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❌ Close",
                            callback_data=f"close#{message.from_user.id}",
                        )
                    ]
                ]
            ),
        )
    except IndexError:
        return await message.reply(f"Gunakan command /{message.command[0]} <b>[link]</b> untuk scrap link download")
    except Exception as e:
        await message.reply(f"ERROR: {str(e)}")

# Scrape DDL Link Nodrakor
@app.on_message(filters.command(["nodrakor_scrap"], COMMAND_HANDLER))
async def nodrakor_scrap(_, message):
    try:
        link = message.text.split(" ", maxsplit=1)[1]
        html = await http.get(link, headers=headers)
        soup = BeautifulSoup(html.text, "lxml")
        hasil = soup.find_all(class_="gmr-download-wrap clearfix")[0]
        await message.reply(f"<b>Hasil Scrap dari {link}</b>:\n{hasil}")
    except IndexError:
        return await message.reply(f"Gunakan command /{message.command[0]} <b>[link]</b> untuk scrap link download")
    except Exception as e:
        await message.reply(f"ERROR: {str(e)}")


# Scrape Link Download Movieku.CC
@app.on_message(filters.command(["movieku_scrap"], COMMAND_HANDLER))
async def muviku_scrap(_, message):
    try:
        link = message.text.split(" ", maxsplit=1)[1]
        html = await http.get(link, headers=headers)
        soup = BeautifulSoup(html.text, "lxml")
        res = soup.find_all(class_="smokeurl")
        data = []
        for i in res:
            for b in range(len(i.find_all("a"))):
                link = i.find_all("a")[b]["href"]
                kualitas = i.find_all("a")[b].text
                # print(f"{kualitas}\n{link
                data.append({"link": link, "kualitas": kualitas})
        if not data:
            return await message.reply("Oops, data film tidak ditemukan.")
        res = "".join(f"<b>Host: {i['kualitas']}</b>\n{i['link']}\n\n" for i in data)
        await message.reply(res)
    except IndexError:
        return await message.reply(f"Gunakan command /{message.command[0]} <b>[link]</b> untuk scrap link download")
    except Exception as e:
        await message.reply(f"ERROR: {str(e)}")

# Scrape DDL Link Melongmovie
@app.on_message(filters.command(["melongmovie_scrap"], COMMAND_HANDLER))
async def melong_scrap(_, message):
    try:
        link = message.text.split(" ", maxsplit=1)[1]
        headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}

        html = await http.get(link, headers=headers)
        soup = BeautifulSoup(html.text, "lxml")
        for ep in soup.findAll(text=re.compile(r"(?i)episode\s+\d+|LINK DOWNLOAD")):
            hardsub = ep.findPrevious("div")
            softsub = ep.findNext("div")
            rep = f"{hardsub}\n{softsub}"
            await message.reply(rep)
    except IndexError:
        await message.reply(f"Gunakan command /{message.command[0]} <b>[link]</b> untuk scrap link download")

# Scrape DDL Link Gomov & Zonafilm
@app.on_message(filters.command(["gomov_scrap", "zonafilm_scrap"], COMMAND_HANDLER))
async def gomov_zonafilm_dl(_, message):
    try:
        link = message.text.split(" ", maxsplit=1)[1]
        headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}

        html = await http.get(link, headers=headers)
        soup = BeautifulSoup(html.text, "lxml")
        entry = soup.find(class_="gmr-download-wrap clearfix")
        hasil = soup.find(class_="title-download").text
        for i in entry.find(class_="list-inline gmr-download-list clearfix"):
            title = i.find("a").text
            link = i.find("a")["href"]
            hasil += f"\n{title}\n{link}\n"
        await message.reply(
            hasil,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❌ Close",
                            callback_data=f"close#{message.from_user.id}",
                        )
                    ]
                ]
            ),
        )
    except IndexError:
        await message.reply(f"Gunakan command /{message.command[0]} <b>[link]</b> untuk scrap link download")
    except Exception as err:
        await message.reply(f"ERROR: {err}")