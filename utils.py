
import logging
from config import *

from database.database import db
import aiohttp
from shortzy import Shortzy


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class temp(object):
    SETTINGS = {}
    FILE_ID = {}
    ASSIGNED_CHANNEL = {}
    LOCAL_MSG = {}

async def save_group_settings(group_id, key, value):
    current = await get_settings(group_id)
    current[key] = value
    temp.SETTINGS[group_id] = current
    await db.update_settings(group_id, current)
    

async def get_settings(chat_id):
    settings = temp.SETTINGS.get(chat_id)
    if not settings:
        settings = await db.get_settings(chat_id)
        temp.SETTINGS[chat_id] = settings
    return settings

async def get_shortlink(chat_id, link):
    settings = await get_settings(chat_id) #fetching settings for group
    if 'shortlink' in settings.keys():
        URL = settings['shortlink']
        API = settings['shortlink_api']
    else:
        URL = URL_SHORTENR_WEBSITE
        API = URL_SHORTNER_WEBSITE_API
    if URL.startswith("shorturllink") or URL.startswith("terabox.in") or URL.startswith("urlshorten.in"):
        URL = URL_SHORTENR_WEBSITE
        API = URL_SHORTNER_WEBSITE_API
    if URL == "api.shareus.io":
        url = f'https://{URL}/easy_api'
        params = {
            "key": API,
            "link": link,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    data = await response.text()
                    return data
        except Exception as e:
            logger.error(e)
            return link
    else:
        shortzy = Shortzy(api_key=API, base_site=URL)
        link = await shortzy.convert(link)
        return link
   

