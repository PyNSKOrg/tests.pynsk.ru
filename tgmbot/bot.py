# -*- coding: utf-8 -*-
import telebot
from telebot import types

from django.conf import settings
from testapp.models import Test, Player, Game, GameQuestion, Answer, Question, ResultView

from testapp.exceptions import OpenGameAlreadyExists, TestIsNotAvailable
import re
from django.db.models import Count
from django.template.loader import render_to_string

bot = telebot.TeleBot(settings.TGM_BOT_TOKEN)


def get_or_create_player(message):
    user = message.from_user
    try:
        player = Player.manager.get(tgm_user_id=user.id)
    except Player.DoesNotExist:
        player = Player.manager.create_tgm_user(user)
    return player


@bot.message_handler(commands=['start'])
def start(message):
    get_or_create_player(message)
    text = render_to_string('tgmbot/start', {})
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help(message):
    text = render_to_string('tgmbot/help', {})
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['status'])
def status(message):
    player = get_or_create_player(message)
    text = render_to_string('tgmbot/status', {})
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['tests'])
def list_test(message):    
    test_list = Test.objects.filter(published=True).annotate(Count('questions'))
    text = render_to_string('tgmbot/test_list', 
        {'test_list' : test_list}
    )
    msg = bot.send_message(message.chat.id, text, parse_mode='Markdown')
        

@bot.message_handler(regexp=r"^/test_[\d]+$")
def start_test(message):    
    match = re.search(r"test_([\d]+)", message.text)
    if match:
        test_id = match.group(1)
        try:
            test = Test.manager.get(pk=test_id)
        except Test.DoesNotExist:
            bot.send_message(message.chat.id, u"Такой тест не найден")
            return
        player = get_or_create_player(message)
        try:
            game = Game.manager.create_game(player=player, test=test)
        except OpenGameAlreadyExists:
            bot.send_message(message.chat.id,
                render_to_string('tgmbot/openGameAlreadyExists', {})
            )
            return
        except TestIsNotAvailable as e:
            bot.send_message(message.chat.id,
                render_to_string('tgmbot/TestIsNotAvailable',
                {"available_time": e.available_time})
            )
            return
        next_question(message, game=game)


@bot.message_handler(commands=['next'])
def next_question(message, game=None, additional_text=''):
    if not game:
        player = get_or_create_player(message)
        game = player.current_game()
        if game is None:
            markup = types.ReplyKeyboardHide()
            bot.send_message(message.chat.id, 
            u"Вы не начинали тестирование. Отпраьте /tests, чтобы выбрать тест", reply_markup=markup)
            return
    question, option_list, number = game.next_question()
    if question:
        text = render_to_string('tgmbot/question', {
            'question': question,
            'option_list': option_list,
            'number': number,
            'additional_text': additional_text,
        })
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add(*list([letter.upper() for letter, option in option_list]))
        markup.row('/stop Завершить тест', '/next Следущий вопрос')
        bot.send_message(message.chat.id, text, reply_markup=markup)        
    else:
        markup = types.ReplyKeyboardHide()
        result = game.result()
        rating = ResultView.objects.get_rating(player=game.player, test=game.test)[1]
        text = render_to_string('tgmbot/end_test', {
            'additional_text': additional_text,
            'result': result,
            'rating': rating,
        })
        bot.send_message(message.chat.id, text, reply_markup=markup)
            

@bot.message_handler(commands=['stat'])
def stat(message):
    player = get_or_create_player(message)
    rating_list = player.get_rating()
    if rating_list:
        text = render_to_string('tgmbot/statistics', {
                'rating_list': rating_list,
            })
    else:
        text = "Ваши результаты не найдены"
    bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(commands=['stop'])
def stop_test(message):
    player = get_or_create_player(message)
    game = player.current_game()
    if game:
        game.stop()
        result = game.result()
        rating = ResultView.objects.get_rating(player=game.player, test=game.test)[1]
        text = render_to_string('tgmbot/end_test', {
            'result': result,
            'rating': rating,
        })
        markup = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp=r"^/?([a-z]|[A-Z])$")
def player_answer_handler(message):
    match = re.search(r"^/?([a-z]|[A-Z])$", message.text)
    if match:
        answer = match.group(1)
        player = get_or_create_player(message)
        game = player.current_game()
        if not game:
            return
        game_question = game.current_game_question()
        if game_question:
            result = game_question.reply(answer.lower())
            if result:
                next_question(message, game=game, additional_text=u'\U0001f44d Правильно!')
            else:
                next_question(message, game=game, additional_text=u'\U0001f614 Неверно.')
        else:
            return


@bot.message_handler(commands=['info'])
def info(message):
    user = message.from_user
    bot.send_message(message.chat.id, 'user_id: %s, %s, %s, %s, chat_id: %s' % 
        (user.id, user.first_name, user.last_name, 
        user.username, message.chat.id)
    )