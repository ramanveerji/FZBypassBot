from pyrogram.filters import create
from re import search
from requests import get as rget
from urllib.parse import urlparse, parse_qs
from FZBypass import Config

async def auth_topic(_, __, message):
    for chat in Config.AUTH_CHATS:
        if ':' in chat:
            chat_id, topic_id = chat.split(':')
            if (int(chat_id) == message.chat.id 
                and (is_forum := message.reply_to_message)
                and ((is_forum.text is None and int(topic_id) == is_forum.id)
                or (is_forum.text is not None and int(topic_id) == is_forum.reply_to_message_id))):
                return True
        elif int(chat) == message.chat.id:
            return True
    return False

chat_and_topics = create(auth_topic)

def get_gdriveid(link):
    if "folders" in link or "file" in link:
        res = search(r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)", link)
        return res.group(3)
    parsed = urlparse(link)
    return parse_qs(parsed.query)['id'][0]

def get_dl(link):
    try:
        return rget(f"{Config.DIRECT_INDEX}/generate.aspx?id={get_gdriveid(link)}").json()["link"]
    except:
        return f"{Config.DIRECT_INDEX}/direct.aspx?id={get_gdriveid(link)}"

def convert_time(seconds):
    # Convert seconds to milliseconds
    mseconds = seconds * 1000
    
    # Define a list of tuples, each containing a period name (e.g., 'd' for days)
    # and the corresponding number of milliseconds in that period.
    periods = [('d', 86400000), ('h', 3600000), ('m', 60000), ('s', 1000), ('ms', 1)]
    
    # Initialize an empty list to store the result components
    result_components = []
    
    # Iterate through the periods
    for period_name, period_seconds in periods:
        if mseconds >= period_seconds:
            # Divide the remaining milliseconds by the number of milliseconds in the current period
            period_value, mseconds = divmod(mseconds, period_seconds)
            # Append the formatted period value and name to the result components list
            result_components.append(f'{int(period_value)}{period_name}')
    
    # If the result components list is empty, return '0ms'
    if not result_components:
        return '0ms'
    
    # Join the result components with spaces and return the formatted result string
    return ' '.join(result_components)

