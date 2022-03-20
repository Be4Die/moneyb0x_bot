import texts
import data
import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.TOKEN)



@bot.message_handler(commands=['addIncome'])
def addMoney(message):
    success = True
    try:
        arg = str(message.text.split(maxsplit=1)[1]).split(' ')
        arg = int(arg[0])
        lastvalue = data.GetUserData(message.chat.id)
        if lastvalue == False:
            lastvalue = 0
        else: lastvalue= int(lastvalue.income)
        data.SetUserIncome(message.chat.id,lastvalue+arg)
        bot.send_message(message.chat.id,texts.successaddmoneyMsg.format(arg))
    except: 
        success = False

    if success == False:
        bot.send_message(message.chat.id,texts.undefindText)

    return success

@bot.message_handler(commands=['addConsumption'])
def addConsumption(message):
    success = True
    try:
        arg = str(message.text.split(maxsplit=1)[1]).split(' ')
        arg = int(arg[0])
        lastvalue = data.GetUserData(message.chat.id)
        if lastvalue == False:
            lastvalue = 0
        else: lastvalue= int(lastvalue.consumption)
        data.SetUserConsumption(message.chat.id,lastvalue+arg)
        bot.send_message(message.chat.id,texts.successputawaymoneyMsg.format(arg))
    except: 
        success = False

    if success == False:
        bot.send_message(message.chat.id,texts.undefindText)

    return success

@bot.message_handler(commands=['addMonthIncome'])
def addMonthMoney(message):
    success = True
    try:
        arg = str(message.text.split(maxsplit=1)[1]).split(' ')
        arg = int(arg[0])
        data.SetUserMonthIncome(message.chat.id,arg)
        bot.send_message(message.chat.id,texts.successaddmonthmoneyMsg.format(arg))
    except: 
        success = False

    if success == False:
        bot.send_message(message.chat.id,texts.undefindText)

    return success

@bot.message_handler(commands=['addMonthConsumption'])
def addMonthConsumption(message):
    success = True
    try:
        arg = str(message.text.split(maxsplit=1)[1]).split(' ')
        arg = int(arg[0])
        data.SetUserMonthConsumption(message.chat.id,arg)
        bot.send_message(message.chat.id,texts.successputawaymonthmoneyMsg.format(arg))
    except: 
        success = False

    if success == False:
        bot.send_message(message.chat.id,texts.undefindText)

    return success

@bot.message_handler(commands=['setTarget'])
def setTarget(message):
    success = True
    try:
        arg = str(message.text.split(maxsplit=1)[1]).split(' ')
        arg = int(arg[0])
        data.SetUserTarget(message.chat.id, arg)
        bot.send_message(message.chat.id, texts.successsetTarget.format(arg))
    except: 
        success = False

    if success == False:
        bot.send_message(message.chat.id,texts.undefindText)

def default_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    item1 = types.KeyboardButton(texts.moneyboxBtn)
    item2 = types.KeyboardButton(texts.errorBtn)
    item3 = types.KeyboardButton(texts.authorBtn)


    markup.add(item1, item2,item3)
    return markup

def moneybox_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    item1 = types.KeyboardButton(texts.commandsBtn)
    item2 = types.KeyboardButton(texts.getdeltaBtn)
    item3 = types.KeyboardButton(texts.gettargettimeBtn)
    item4 = types.KeyboardButton(texts.getmonthdeltaBtn)
    item5 = types.KeyboardButton(texts.deletedataBtn)
    item6 = types.KeyboardButton(texts.backBtn)


    markup.add(item1, item2, item3, item4,item5,item6)
    return markup

@bot.message_handler(commands=['go', 'start'])
def start(message):

    bot.send_message(message.chat.id,texts.helloMsg.format(
        message.from_user.first_name, 
        bot.get_me().first_name)
        ,reply_markup = default_menu())

@bot.message_handler(content_types=['text'])
def markup_handler(message):
    if message.chat.type == 'private':
        match message.text:
            case texts.authorBtn: bot.send_message(message.chat.id, texts.authorMsg)
            case texts.moneyboxBtn: bot.send_message(message.chat.id, texts.moneyboxMsg, reply_markup=moneybox_menu())
            case texts.backBtn: bot.send_message(message.chat.id,texts.backBtn, reply_markup=default_menu())
            case texts.commandsBtn: bot.send_message(message.chat.id,texts.commandsMsg)
            case texts.getdeltaBtn:
                userinfo = data.GetUserData(message.chat.id)
                if userinfo == False or (int(userinfo.income) == 0 and int(userinfo.consumption)): 
                    bot.send_message(message.chat.id,texts.undefindMoney)
                else:
                    budget =  int(userinfo.income) - int(userinfo.consumption)
                    if budget >0: bot.send_message(message.chat.id, texts.deltamoneyPosMsg.format(budget))
                    if budget <0: bot.send_message(message.chat.id, texts.deltamoneyNegMsg.format(budget))
            case texts.getmonthdeltaBtn:
                userinfo = data.GetUserData(message.chat.id)
                if userinfo == False or (int(userinfo.monthincome) == 0 and int(userinfo.monthconsumption)): 
                    bot.send_message(message.chat.id,texts.undefindmonthMoney)
                else:
                    budget =  int(userinfo.monthincome) - int(userinfo.monthconsumption)
                    if budget >0: bot.send_message(message.chat.id, texts.deltamonthmoneyPosMsg.format(budget))
                    if budget <0: bot.send_message(message.chat.id, texts.deltamonthmoneyNegMsg.format(budget))
            case texts.gettargettimeBtn:
                userinfo = data.GetUserData(message.chat.id)
                print("1")
                if userinfo == False or (int(userinfo.monthincome) == 0 and int(userinfo.monthconsumption)): 
                    bot.send_message(message.chat.id,texts.undefindmonthMoney)
                else:
                    budget =  int(userinfo.monthincome) - int(userinfo.monthconsumption)
                    print(budget)
                    if int(userinfo.target) == 0: bot.send_message(message.chat.id,texts.undefindTarget)
                    elif budget > 0: 
                        time = str((int(userinfo.target)//budget)+1)
                        if int(time[-1]) == 1: text = time + ' месяц'
                        if int(time[-1]) > 1 and int(time[-1]) < 5: text = time + ' месяцa'
                        if int(time[-1]) >= 5 or int(time[-1]) == 0: text = time + ' месяцев'

                        bot.send_message(message.chat.id,texts.gettargettimeMsg.format(userinfo.target, text))
                    elif budget <=0: bot.send_message(message.chat.id,texts.errbudgetMsg)

            case texts.errorBtn: bot.send_message(message.chat.id, texts.finderrorMsg)

            case texts.deletedataBtn:
                try: 
                    data.ClearUserData(message.chat.id)
                    bot.send_message(message.chat.id,texts.successdeleteuserdataMsg)
                except:
                    bot.send_message(message.chat.id,texts.errdeleteuserdataMsg)

            case _: bot.send_message(message.chat.id,texts.undefindText)


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except ConnectionError as e:
        print(texts.connectionError.format(e))
    except Exception as r:
        print(texts.undefindError.format(r))