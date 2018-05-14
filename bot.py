# -*- coding: utf-8 -*-
import os
import telebot
import time
import chlenomerconfig
import telebot
import random
from telebot import types
from pymongo import MongoClient
import threading


client1=os.environ['database']
client=MongoClient(client1)
db=client.chlenomer
idgroup=db.ids
iduser=db.ids_people

ban=[]

wait=[]
ch=[]
members=[]
play=[]

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
writed=[
]
massive=['Хер','хер','Член','член','Хуй','хуй']
elita=[441399484, 55888804, 314238081]

@bot.message_handler(commands=['sendm'])
def sendmes(message):
    if message.from_user.id==441399484:
        x=idgroup.find({})
        y=iduser.find({})
        tex=message.text.split('/sendm')
        for one in x:
            try:
              bot.send_message(one['id'], tex[1])
            except:
                pass
        for one in y:
            try:
              bot.send_message(one['id'], tex[1])
            except:
                pass


    
            
            
@bot.message_handler(commands=['stats'])
def stats(m):
    x=iduser.find_one({'id':m.from_user.id})
    if x!=None:
        try:
            percent=round((x['pet']['wons']/(x['pet']['lose']+x['pet']['wons']))*100,0)
        except:
            try:
                if x['pet']['wons']!=0:
                    percent=100
                else:
                    percent=0
            except:
                pass
        try:
            bot.send_message(m.chat.id, 'Победы: '+str(x['pet']['wons'])+'\nПоражения: '+str(x['pet']['lose'])+'\nВинрейт: '+str(percent)+'%')
        except:
            pass
            
            
            
@bot.message_handler(commands=['elita']) 
def elit(m):
    if m.from_user.id in elita:
        Kb = types.ReplyKeyboardMarkup()
        Kb.add(types.KeyboardButton("Член"))
        Kb.add(types.KeyboardButton("Хер"))
        bot.send_message(m.from_user.id, 'Вы элита!', reply_markup=Kb)
    
    
#@bot.message_handler(commands=['update'])
#def upd(m):
#  if m.from_user.id==441399484:
#         try:
#            iduser.update_many({'pet':{'$ne':None}}, {'$set':{'pet.lose':0}})
#
#         except:
#            pass
            
            
@bot.message_handler(commands=['mysize'])
def size(m):
    x=iduser.find_one({'id':m.from_user.id})
    try:
        sredn=x['summ']/x['kolvo']
        sredn=round(sredn, 1)
    except:
        sredn=0
    try:
        bot.send_message(m.chat.id, m.from_user.first_name+', средний размер вашего члена: '+str(sredn)+' см.\nВы измеряли член '+str(x['kolvo'])+' раз(а)!') 
        bot.send_message(441399484, m.from_user.first_name+', средний размер вашего члена: '+str(sredn)+' см.\nВы измеряли член '+str(x['kolvo'])+' раз(а)!')
    except:
        bot.send_message(m.chat.id, 'Измерьте член хотя бы 1 раз!')
                        
    
    
@bot.message_handler(commands=['me'])
def mme(m):
    x=iduser.find_one({'id': m.from_user.id})
    try:
     bot.send_message(m.chat.id, m.from_user.first_name+', Ваши членокоины: '+str(x['chlenocoins'])+'. Сейчас они не нужны, но следите за обновлениями - в будущем они понадобятся!')
     bot.send_message(441399484, m.from_user.first_name+', Ваши членокоины: '+str(x['chlenocoins'])+'. Сейчас они не нужны, но следите за обновлениями - в будущем они понадобятся!')                                                                                                                                     
    except:
      try:
        bot.send_message(m.chat.id, 'Упс! Какая-то ошибка! Наверное, вы ни разу не измеряли член! (напишите боту "член")')
        bot.send_message(441399484, 'Упс! Какая-то ошибка! Наверное, вы ни рару не измеряли член!')  
      except:
        pass
                                                                 
        
          
                
@bot.message_handler(commands=['channel'])
def channel(message):
  try:
    bot.send_message(message.chat.id, 'Канал обновлений: @chlenomer')
  except:
    pass
                     

@bot.message_handler(commands=['start'])
def startms(message):
    try:
        bot.send_message(message.from_user.id, 'Это бот для сражений питомцев Членомера! Подробнее - /pethelp')
    except:
        pass


@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.id==441399484:
        group=0
        people=0
        x=idgroup.find({})
        for element in x:
            group+=1
        y=iduser.find({})
        for element in y:
            people+=1
        try:
            bot.send_message(message.from_user.id, 'Группы: '+str(group)+'\n'+'Люди: '+str(people))
        except:
            pass
        
                     
        
@bot.message_handler(commands=['name'])
def name(m):
    player=iduser.find_one({'id':m.from_user.id})
    if player!=None:
        x=m.text.split('/name ')
        if len(x)==2:
            if len(x[1])<=40:
                try:
                    iduser.update_one({'id':m.from_user.id}, {'$set':{'pet.name':x[1]}})
                    bot.send_message(m.from_user.id, 'Вы успешно переименовали питомца!')
                except:
                    bot.send_message(m.from_user.id, 'У вас нет питомца!')          
            else:
                bot.send_message(m.from_user.id, 'Длина имени не должна превышать 40 символов!')
        else:
            bot.send_message(m.from_user.id, 'Неверный формат! Пишите в таком формате:\n'+'/name *имя*, где *имя* - имя вашего питомца.', parse_mode='markdown')
    else:
        bot.send_message(m.from_user.id, 'Сначала напишите боту "член" хотя бы один раз!')
            
        
        
        

@bot.message_handler(commands=['fight'])
def fight(m):
    user=m.from_user.id
    if m.chat.id>0:
      z=iduser.find_one({'id':m.from_user.id})
      if z!=None:
        if z['pet']!=None:
          if z['pet']['name']!=None:
           x=0
           for ids in play:
             if ids['id1']['id']==user:
                x=1
                y=ids['id1']
             if ids['id2']['id']==user:
                x=1
                y=ids['id2']
           if x==0:
            t=threading.Timer(300, noplayers, args=[m.from_user.id])
            t.start()
            try:
                bot.send_message(m.chat.id, 'Вы встали в очередь на поединок питомцев! Ожидайте игроков...')
            except:
                pass
            wait.append(m.from_user.id)
            player=iduser.find_one({'id':m.from_user.id})
            for id in wait:
                if id!=m.from_user.id:
                    x=iduser.find_one({'id':id})
                    if x['pet']['level']==player['pet']['level']: 
                        name1=player['pet']['name']
                        name2=x['pet']['name']
                        try:
                            wait.remove(player['id'])
                        except:
                            pass
                        try:
                            wait.remove(x['id'])
                        except:
                            pass
                        gofight(player['id'], x['id'], name1, name2)                
          else:
            try:
                bot.send_message(m.from_user.id, 'Сначала дайте питомцу имя! (команда /name)') 
            except:
                pass
        else:
            try:
                bot.send_message(m.from_user.id, 'У вас нет питомца!')
            except:
                pass
      else:
        try:
            bot.send_message(m.from_user.id, 'Сначала напишите боту "член"!')
        except:
            pass
    else:
      try:
       bot.send_message(m.from_user.id, 'Эту команду можно использовать только в личных сообщениях бота!') 
      except:
            pass

@bot.message_handler(commands=['cancel'])
def cancel(m):
    try:
        wait.remove(m.from_user.id)
        bot.send_message(m.from_user.id, 'Вы  были успешно удалены из очереди.') 
    except:
        pass
    
    
@bot.callback_query_handler(func=lambda call:True)
def inline(call):
    ataka=0
    user=call.from_user.id
    if call.data=='atk+1':
        ataka=1
    elif call.data=='atk+2':
        ataka=2
    elif call.data=='atk+5':
        ataka=5
    elif call.data=='atk+10':
        ataka=10
    if ataka>0:
        x=0
        for ids in play:
            if ids['id1']['id']==user:
                x=1
                y=ids['id1']
            if ids['id2']['id']==user:
                x=1
                y=ids['id2']
        if x==1:
            if y['attackselect']==1:
                if y['attack']>=ataka:
                    y['attackround']+=ataka
                    y['attack']-=ataka
                    Keyboard=types.InlineKeyboardMarkup()
                    Keyboard.add(types.InlineKeyboardButton(text='+1', callback_data='atk+1'))
                    Keyboard.add(types.InlineKeyboardButton(text='+2', callback_data='atk+2'))
                    Keyboard.add(types.InlineKeyboardButton(text='+5', callback_data='atk+5'))
                    Keyboard.add(types.InlineKeyboardButton(text='+10', callback_data='atk+10'))
                    Keyboard.add(types.InlineKeyboardButton(text='Окончить выбор', callback_data='endattack'))
                    medit('Теперь выставьте количество атаки, которое хотите поставить в этом ходу. Текущая атака: '+str(y['attackround']),
                    call.from_user.id,
                    call.message.message_id, reply_markup=Keyboard)
                else:
                    bot.answer_callback_query(call.id, 'У вас недостаточно атаки!')
            else:
                bot.send_message(user, 'Нет!')
                
                
    defence=0
    user=call.from_user.id
    if call.data=='def+1':
        defence=1
    elif call.data=='def+2':
        defence=2
    elif call.data=='def+5':
        defence=5
    elif call.data=='def+10':
        defence=10
    if defence>0:
        x=0
        for ids in play:
            if ids['id1']['id']==user:
                x=1
                y=ids['id1']
            if ids['id2']['id']==user:
                x=1
                y=ids['id2']
        if x==1:
            if y['defenceselect']==1:
                if y['defence']>=defence:
                    y['defenceround']+=defence
                    y['defence']-=defence
                    Keyboard=types.InlineKeyboardMarkup()
                    Keyboard.add(types.InlineKeyboardButton(text='+1', callback_data='def+1'))
                    Keyboard.add(types.InlineKeyboardButton(text='+2', callback_data='def+2'))
                    Keyboard.add(types.InlineKeyboardButton(text='+5', callback_data='def+5'))
                    Keyboard.add(types.InlineKeyboardButton(text='+10', callback_data='def+10'))
                    Keyboard.add(types.InlineKeyboardButton(text='Окончить выбор', callback_data='enddef'))
                    medit('Теперь выставьте количество защиты, которое хотите поставить в этом ходу. Текущая защита: '+str(y['defenceround']),
                    call.from_user.id,
                    call.message.message_id, reply_markup=Keyboard)
                else:
                    bot.answer_callback_query(call.id, 'У вас недостаточно защиты!')
            else:
                bot.send_message(user, 'Нет!')
                    
    if call.data=='endattack':
          x=0
          for ids in play:
            if ids['id1']['id']==user:
                x=1
                y=ids['id1']
            if ids['id2']['id']==user:
                x=1
                y=ids['id2']
          if x==1:
            if y['attackselect']==1:
                y['attackselect']=0
                y['defenceselect']=1
                Keyboard=types.InlineKeyboardMarkup()
                Keyboard.add(types.InlineKeyboardButton(text='+1', callback_data='def+1'))
                Keyboard.add(types.InlineKeyboardButton(text='+2', callback_data='def+2'))
                Keyboard.add(types.InlineKeyboardButton(text='+5', callback_data='def+5'))
                Keyboard.add(types.InlineKeyboardButton(text='+10', callback_data='def+10'))
                Keyboard.add(types.InlineKeyboardButton(text='Окончить выбор', callback_data='enddef'))
                medit('Теперь выставьте количество защиты, которое хотите поставить в этом ходу. Текущая защита: 0', call.from_user.id, call.message.message_id, reply_markup=Keyboard)
                        
    if call.data=='enddef':
          x=0
          for ids in play:
            if ids['id1']['id']==user:
                x=1
                y=ids['id1']
                z=ids['id2']
            if ids['id2']['id']==user:
                x=1
                y=ids['id2']
                z=ids['id1']
          if x==1:
            y['defenceselect']=0
            medit('Ожидайте других игроков...', call.from_user.id, call.message.message_id)
            y['timer'].cancel()
            y['ready']=1
            ready(y, z, ids)


            

            
            
            
def medit(message_text,chat_id, message_id,reply_markup=None,parse_mode='Markdown'):
    return bot.edit_message_text(chat_id=chat_id,message_id=message_id,text=message_text,reply_markup=reply_markup,
                                 parse_mode=parse_mode)


def gofight(id1, id2, name1, name2):
    player1=iduser.find_one({'id':id1})
    player2=iduser.find_one({'id':id2})
    player1['pet']['attack']=player1['pet']['maxattack']
    player1['pet']['defence']=player1['pet']['maxdefence']
    player2['pet']['attack']=player2['pet']['maxattack']
    player2['pet']['defence']=player2['pet']['maxdefence']
    play.append(creategame(id1, id2, player1, player2))
    bot.send_message(id1, 'Битва начинается! Ваш питомец дерётся с питомцем, которого зовут '+'*"'+name2+'"'+'*! Его уровень: '+str(player2['pet']['level']), parse_mode='markdown')
    bot.send_message(id2, 'Битва начинается! Ваш питомец дерётся с питомцем, которого зовут '+'*"'+name1+'"'+'*! Его уровень: '+str(player1['pet']['level']), parse_mode='markdown')
    bot.send_message(441399484, 'Битва начинается! Ваш питомец дерётся с питомцем, которого зовут '+'*"'+name2+'"'+'*! Его уровень: '+str(player2['pet']['level']), parse_mode='markdown')
    bot.send_message(441399484, 'Битва начинается! Ваш питомец дерётся с питомцем, которого зовут '+'*"'+name1+'"'+'*! Его уровень: '+str(player1['pet']['level']), parse_mode='markdown')
    xod(id1, id2, name1, name2, player1, player2)
    
    
    
def xod(id1, id2, name1, name2, player1, player2):
  try:
    if player1['pet']['skill']==None:
        skill1='Отсутствует'
    else:
        skill1=player1['pet']['skill']
        
    if player2['pet']['skill']==None:
        skill2='Отсутствует'
    else:
        skill2=player2['pet']['skill']
    bot.send_message(id1, 'Информация о вашем питомце:\n'+'❤️ХП: '+str(player1['pet']['hp'])+
                     '\n⚔️Атака: '+str(player1['pet']['attack'])+'/'+str(player1['pet']['maxattack'])+'\n'+
                     '⚡️Реген атаки: '+str(player1['pet']['regenattack'])+'\n'+
                    '🛡Защита: '+str(player1['pet']['defence'])+'/'+str(player1['pet']['maxdefence'])+'\n'+
                     '🔵Реген защиты: '+str(player1['pet']['regendefence'])+'\n'+
                     '🔺Скилл: '+skill1       
                    )
    
    bot.send_message(id2, 'Информация о вашем питомце:\n'+'❤️ХП: '+str(player2['pet']['hp'])+
                     '\n⚔️Атака: '+str(player2['pet']['attack'])+'/'+str(player2['pet']['maxattack'])+'\n'+
                     '⚡️Реген атаки: '+str(player2['pet']['regenattack'])+'\n'+
                    '🛡Защита: '+str(player2['pet']['defence'])+'/'+str(player2['pet']['maxdefence'])+'\n'+
                     '🔵Реген защиты: '+str(player2['pet']['regendefence'])+'\n'+
                     '🔺Скилл: '+skill2       
                    )
  except:
    if player1['skill']==None:
        skill1='Отсутствует'
    else:
        skill1=player1['skill']
        
    if player2['skill']==None:
        skill2='Отсутствует'
    else:
        skill2=player2['skill']
    bot.send_message(id1, 'Информация о вашем питомце:\n'+'❤️ХП: '+str(player1['hp'])+
                     '\n⚔️Атака: '+str(player1['attack'])+'/'+str(player1['maxattack'])+'\n'+
                     '⚡️Реген атаки: '+str(player1['attackregen'])+'\n'+
                    '🛡Защита: '+str(player1['defence'])+'/'+str(player1['maxdefence'])+'\n'+
                     '🔵Реген защиты: '+str(player1['defenceregen'])+'\n'+
                     '🔺Скилл: '+skill1       
                    )
    
    bot.send_message(id2, 'Информация о вашем питомце:\n'+'❤️ХП: '+str(player2['hp'])+
                     '\n⚔️Атака: '+str(player2['attack'])+'/'+str(player2['maxattack'])+'\n'+
                     '⚡️Реген атаки: '+str(player2['attackregen'])+'\n'+
                    '🛡Защита: '+str(player2['defence'])+'/'+str(player2['maxdefence'])+'\n'+
                     '🔵Реген защиты: '+str(player2['defenceregen'])+'\n'+
                     '🔺Скилл: '+skill2       
                    )
   
    
  for ids in play:
            if ids['id1']['id']==id1:
                ids['id1']['attackselect']=1
            if ids['id2']['id']==id1:
                ids['id2']['attackselect']=1
            if ids['id1']['id']==id2:
                ids['id1']['attackselect']=1
            if ids['id2']['id']==id2:
                ids['id2']['attackselect']=1
  t=threading.Timer(60, noready, args=[ids['id1'], ids['id2'], ids])
  t.start()
  zz=threading.Timer(60, noready, args=[ids['id2'],ids['id1'], ids])
  zz.start()
  ids['id1']['timer']=t
  ids['id2']['timer']=zz
  Keyboard=types.InlineKeyboardMarkup()
  Keyboard.add(types.InlineKeyboardButton(text='+1', callback_data='atk+1'))
  Keyboard.add(types.InlineKeyboardButton(text='+2', callback_data='atk+2'))
  Keyboard.add(types.InlineKeyboardButton(text='+5', callback_data='atk+5'))
  Keyboard.add(types.InlineKeyboardButton(text='+10', callback_data='atk+10'))
  Keyboard.add(types.InlineKeyboardButton(text='Окончить выбор', callback_data='endattack'))
  msg1=bot.send_message(id1, 'Теперь выставьте количество атаки, которое хотите поставить в этом ходу. Текущая атака: 0', reply_markup=Keyboard)  
  msg2=bot.send_message(id2, 'Теперь выставьте количество атаки, которое хотите поставить в этом ходу. Текущая атака: 0', reply_markup=Keyboard)
  ids['id1']['message']=msg1.message_id
  ids['id2']['message']=msg2.message_id
    

def ready(ids, id2, game): 
    ids['ready']=1
    if ids['ready']==1 and id2['ready']==1:
        endturn(game)


def noready(ids, id2, game):
    ids['ready']=1
    medit('Время вышло!', ids['id'], ids['message'])
    if ids['ready']==1 and id2['ready']==1:
        endturn(game)
                

def endturn(game):#############################################################  ENDTURN
    text1=''
    text2=''
    player1=game['id1']
    player2=game['id2']
    damage1=player1['attackround']
    damage2=player2['attackround']
    defence1=player1['defenceround']
    defence2=player2['defenceround']
    losehp1=damage2-defence1
    if losehp1<0:
        losehp1=0
    player1['hp']-=losehp1
    text1+='*'+player1['name']+'*:\n'+'Выставленная атака: '+str(player1['attackround'])+'\nВыставленная защита: '+str(player1['defenceround'])+'\nПолученный урон: '+str(losehp1)
    
        
    losehp2=damage1-defence2
    if losehp2<0:
        losehp2=0
    player2['hp']-=losehp2
    text2+='*'+player2['name']+'*:\n'+'Выставленная атака: '+str(player2['attackround'])+'\nВыставленная защита: '+str(player2['defenceround'])+'\nПолученный урон: '+str(losehp2)
        
    try:    
        bot.send_message(player1['id'], 'Результаты хода:\n\n'+text1+'\n'+'\n'+text2, parse_mode='markdown')
    except:
        pass
    try:
        bot.send_message(player2['id'], 'Результаты хода:\n\n'+text1+'\n'+'\n'+text2, parse_mode='markdown')
    except:
        pass
    player1['attackround']=0
    player1['defenceround']=0
    player1['ready']=0
    if player1['attack']<player1['maxattack']:
        player1['attack']+=player1['attackregen']
    if player1['defence']<player1['maxdefence']:
        player1['defence']+=player1['defenceregen']
    player2['attackround']=0
    player2['defenceround']=0
    player2['ready']=0
    if player2['attack']<player2['maxattack']:
        player2['attack']+=player2['attackregen']
    if player2['defence']<player2['maxdefence']:
        player2['defence']+=player2['defenceregen']
    if player1['hp']<=0 and player2['hp']>0:
        try:
            bot.send_message(player1['id'], 'Победа питомца с именем '+player2['name']+'!')
        except:
            pass
        try:
            bot.send_message(player2['id'], 'Победа питомца с именем '+player2['name']+'!')
        except:
            pass
        bot.send_message(441399484, 'Победа питомца с именем '+player2['name']+'!')
        iduser.update_one({'id':player2['id']}, {'$inc':{'pet.wons':1}})
        iduser.update_one({'id':player1['id']}, {'$inc':{'pet.lose':1}})
        play.remove(game)
    elif player2['hp']<=0 and player1['hp']>0: 
        try:
            bot.send_message(player1['id'], 'Победа питомца с именем '+player1['name']+'!')
        except:
            pass
        try:
            bot.send_message(player2['id'], 'Победа питомца с именем '+player1['name']+'!')
        except:
            pass
        bot.send_message(441399484, 'Победа питомца с именем '+player1['name']+'!')
        iduser.update_one({'id':player1['id']}, {'$inc':{'pet.wons':1}})
        iduser.update_one({'id':player2['id']}, {'$inc':{'pet.lose':1}})
        play.remove(game)
    elif player1['hp']<=0 and player2['hp']<=0:
        try:
            bot.send_message(player1['id'], 'Ничья! Оба питомца проиграли!')
        except:
            pass
        try:
            bot.send_message(player2['id'], 'Ничья! Оба питомца проиграли!')
        except:
                pass
        iduser.update_one({'id':player2['id']}, {'$inc':{'pet.lose':1}})
        iduser.update_one({'id':player1['id']}, {'$inc':{'pet.lose':1}})
        bot.send_message(441399484, 'Ничья! Оба питомца проиграли!')
        play.remove(game)
    else:
        xod(player1['id'], player2['id'], player1['name'], player2['name'], game['id1'], game['id2'])
        
        
def noplayers(id):
    try:
        wait.remove(id)
        bot.send_message(id, 'Вы ожидали оппонента 5 минут и были удалены из очереди! Попробуйте позже, когда будут ещё бойцы.')
    except:
        pass
        
@bot.message_handler(commands=['buypet'])
def buypet(m):
    x=iduser.find_one({'id':m.from_user.id})
    if x!=None:
      if x['pet']==None:
        if x['chlenocoins']>=5:
            iduser.update_one({'id':m.from_user.id}, {'$set':{'pet':petcreate()}})
            iduser.update_one({'id':m.from_user.id}, {'$inc':{'chlenocoins':-5}})
            bot.send_message(m.chat.id, 'Поздравляю, вы купили питомца! Подробнее об этом в /pethelp.')
        else:
            bot.send_message(m.chat.id, 'Не хватает членокоинов! (нужно 5)')
      else:
        bot.send_message(m.chat.id, 'У вас уже есть питомец!')
    else:
        bot.send_message(m.chat.id, 'Сначала напишите боту "член" хотя бы раз!')
        

        
        
@bot.message_handler(commands=['pethelp'])
def pethelp(m):
    bot.send_message(m.chat.id, 'Питомец вам нужен для участия в боях. Чтобы поучаствовать, нужно написать боту в личные сообщения команду /fight.\n'+
                     'У питомца есть ХП, Атака, Защита, Регенерация атаки, Регенерация защиты. '+
                     'Каждый ход вы выбираете, сколько атаки и сколько защиты поставить на раунд... И ваш питомец сражается своим членом! Каждая поставленная единица защиты заблокирует единицу атаки соперника.\n'+
                     'Таким образом, если вы ставите 2 атаки и 3 брони, а ваш соперник - 3 атаки и 1 броню, то вы получите 0 урона, а он получит 1 урон.\n'+
                     'Прокачка питомца сейчас недоступна, но в будущем появится!'
                    )
                             
                             
                             
                             
@bot.message_handler(commands=['feedback'])
def feedback(message):
    if message.from_user.username!=None:
      bot.send_message(314238081, message.text+"\n"+'@'+message.from_user.username)
      bot.send_message(message.chat.id, 'Сообщение отправлено!')

            
def petcreate():
    return{
        'name':None,
        'level':1,
        'maxattack':4,
        'maxdefence':4,
        'attack':0,
        'defence':0,
        'hp':10,
        'regenattack':1,
        'regendefence':1,
        'skill':None,
        'exp':0,
        'wons':0,
        'lose':0
    }
    
    

def creategame(id1, id2, player1, player2):
             return{
                'id1':{'id':id1,
                       'timer':None,
                       'attackselect':0,
                       'defenceselect':0,
                       'maxattack':player1['pet']['maxattack'],
                       'maxdefence':player1['pet']['maxdefence'],
                       'attack':player1['pet']['maxattack'],
                       'defence':player1['pet']['maxdefence'],
                       'attackround':0,
                       'defenceround':0,
                       'ready':0,
                       'name':player1['pet']['name'],
                       'hp':player1['pet']['hp'],
                       'attackregen':player1['pet']['regenattack'],
                       'defenceregen':player1['pet']['regendefence'],
                       'skill':player1['pet']['skill'],
                       'message':None
                      },
                'id2':{
                    'timer':None,
                    'id':id2,
                    'attackselect':0,
                    'defenceselect':0,
                    'maxattack':player2['pet']['maxattack'],
                    'maxdefence':player2['pet']['maxdefence'],
                    'attack':player2['pet']['maxattack'],
                    'defence':player2['pet']['maxdefence'],
                    'attackround':0,
                    'defenceround':0,
                    'ready':0,
                    'name':player2['pet']['name'],
                    'hp':player2['pet']['hp'],
                    'attackregen':player2['pet']['regenattack'],
                    'defenceregen':player2['pet']['regendefence'],
                    'skill':player2['pet']['skill'],
                    'message':None
                     }
            }


    
    

        
                         



while True:
    from requests.exceptions import ReadTimeout
    from requests.exceptions import ConnectionError
    try:
        bot.polling()
    except(ReadTimeout, ConnectionError):
        pass

