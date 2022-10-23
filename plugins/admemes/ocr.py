

from telegram import ChatAction,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler,PicklePersistence
from plugins.helper_functions.cust_p_filters import f_onw_fliter
import logging
import os
from functools import wraps
import requests

API_KEY = os.environ.get("API_KEY","") 

def  send_typing_action(func):
    """Sends typing action while processing func command."""
    
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@run_async
@send_typing_action
@Client.on_message(
    filters.command("ocr") &
    f_onw_fliter
)
async def ocr(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙰 𝙿𝙷𝙾𝚃𝙾.")
        return
def convert_image(update,context):
    file_id = update.message.photo[-1].file_id
    newFile=context.bot.get_file(file_id)
    file= newFile.file_path
    context.user_data['filepath']=file
    keyboard =  [[InlineKeyboardButton("Arabic", callback_data='ara'),
                  InlineKeyboardButton("Bulgarian", callback_data='bul'),
                  InlineKeyboardButton("Chinese", callback_data='chs')
                 ],
                 [
                  InlineKeyboardButton("Croatian", callback_data='hrv'),
                  InlineKeyboardButton("Danish", callback_data='dan')
                  InlineKeyboardButton("Dutch", callback_data='dut')
                 ],
                 [
                 InlineKeyboardButton("English", callback_data='eng'),
                 InlineKeyboardButton("Finnish", callback_data='fin'),
                 InlineKeyboardButton("French", callback_data='fre')
                 ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select the Language Here 👇",
                              
@run_async
def button(update,context):
    filepath=context.user_data['filepath']
    query = update.callback_query                          
    query.answer()
    query.edit_message_text("Extracting Text....")
    data=requests.get(f"https://api.ocr.space/parse/imageurl?apikey={API_KEY}&url={filepath}&language={query.data}&detectOrientation=True&filetype=JPG&OCREngine=1&isTable=True&scale=True")
    data=data.json()
    if data['IsErroredOnProcessing']==False:
        message=data['ParsedResults'][0]['ParsedText']
        query.edit_message_text(f"{message}") 
    else:
        query.edit_message_text(text="⚠️ Something went wrong")
                              
persistence=PicklePersistence('userdata')
def main():   
    token=TOKEN 
    updater = Updater(token,use_context=True,persistence=persistence)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(MessageHandler(Filters.photo, convert_image))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling(clean=True)
    updater.idle()
        
                              
if __name__=="__main__":
        main()
    

                              

    

       
    
    

   
