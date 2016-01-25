# -*- encoding: utf-8 -*-
from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

from testapp.managers import GameManager, \
    GameQuestionManager, PlayerManager, TestManager


def gen_letter():
    import string
    alphabet = string.ascii_lowercase
    for char in alphabet:
        yield char


class Question(models.Model):
    OPEN = 'O'
    CLOSE = 'C'
    QTYPE = ((OPEN, _('open question')), (CLOSE, _('close question')),)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = 'Questions'

    text = models.CharField(_('Question text'), max_length=2000)
    created_on = models.DateTimeField(_('When was created'), auto_now_add=True)
    changed_on = models.DateTimeField(_('When was last changed'), auto_now=True)
    published = models.BooleanField(_('is published'), default=True)
    qtype = models.CharField(_('question type'),
                             choices=QTYPE,
                             max_length=10,
                             default=CLOSE)

    def __str__(self):
        return u"%s" % self.text

    def __unicode__(self):
        return u"%s" % self.text


class Test(models.Model):
    name = models.CharField(_('Test name'), max_length=200)
    created_on = models.DateTimeField(_('When was created'), auto_now_add=True)
    changed_on = models.DateTimeField(_('When was last changed'), auto_now=True)
    questions = models.ManyToManyField(Question, through='TestQuestion')
    published = models.BooleanField(_('is published'), default=False)
    author = models.CharField(_('Author'), max_length=200, blank=True)
    description = models.CharField(_('Description'), max_length=2000, blank=True)
    objects = models.Manager()
    manager = TestManager()

    def __unicode__(self):
        return u"%s" % self.name


class Player(models.Model):
    tgm_user_id = models.CharField(_('Telegram user id'),
                                   max_length=2000,
                                   unique=True)
    tgm_first_name = models.CharField(_("Telegram user's first name"),
                                      max_length=2000,
                                      blank=True)
    tgm_last_name = models.CharField(_("Telegram user's last name"),
                                     max_length=2000,
                                     blank=True)
    tgm_user_name = models.CharField(_('Telegram username'),
                                     max_length=2000,
                                     blank=True)
    tests = models.ManyToManyField(Test, through='Game')
    objects = models.Manager()
    manager = PlayerManager()

    def stop_game(self):
        games = self.games.filter(state=Game.OPEN)
        for game in games:
            game.stop()

    def current_game(self):
        """Return open game.

        If multiple return last open game. Otherwise return None.

        """
        try:
            return self.games.get(state=Game.OPEN)
        except Game.DoesNotExist:
            return None
        except MultipleObjectsReturned:
            return self.games.filter(
                    state=Game.OPEN).order_by('-start_on').first()

    def __unicode__(self):
        return u"%s" % self.tgm_user_id

    def __str__(self):
        return u"%s" % self.tgm_user_id


class TestQuestion(models.Model):
    class Meta:
        unique_together = (('test', 'question'),)

    test = models.ForeignKey('Test')
    question = models.ForeignKey('Question')

    def __unicode__(self):
        return u"Test: %s. Question: %s" % (self.test, self.question)

    def __str__(self):
        return u"Test: %s. Question: %s" % (self.test, self.question)


class Answer(models.Model):
    MAX_LENGTH = 200
    question = models.ForeignKey(_('Question'), related_name='answers')
    text = models.CharField(_('Answer text'), max_length=MAX_LENGTH)
    answer_description = models.TextField(_('Answer description'),
                                          max_length=20000,
                                          blank=True)
    is_true = models.BooleanField(_('is true'), default=False)

    def __str__(self):
        return u"%s" % self.text

    def __unicode__(self):
        return u"%s" % self.text


class Game(models.Model):
    OPEN = 'O'
    CLOSE = 'C'
    STATE = ((OPEN, _('Open game')), (CLOSE, _('Close game')),)
    player = models.ForeignKey('Player', related_name='games')
    test = models.ForeignKey('Test')
    start_on = models.DateTimeField(_('when was started'), auto_now_add=True)
    stop_on = models.DateTimeField(_('when was stoped'), null=True, blank=True)
    questions = models.ManyToManyField(_('Question'), through='GameQuestion')
    state = models.CharField(_('Game state'),
                             choices=STATE,
                             max_length=10,
                             default=OPEN)
    objects = models.Manager()
    manager = GameManager()

    def stop(self):
        if self.state == Game.OPEN:
            self.state = Game.CLOSE
            self.stop_on = timezone.now()
            self.save()

    def no_more_questions(self):
        asked_questions = self.questions.all()
        not_asked_questions = self.test.questions.filter(
                published=True).exclude(id__in=asked_questions)
        if not_asked_questions:
            return False
        else:
            return True

    def next_question(self):
        question = None
        answers = []
        number = None
        if self.state == Game.OPEN:
            asked_questions = self.questions.all()
            not_asked_questions = self.test.questions.filter(
                    published=True).exclude(id__in=asked_questions)
            question = not_asked_questions.order_by('?').first()
            if question:
                number = len(asked_questions) + 1
                game_question = GameQuestion(game=self, question=question)
                answer_list = question.answers.order_by('?').all()
                gen = gen_letter()
                for answer in answer_list:
                    letter = next(gen)
                    answers.append((letter, answer))
                    if answer.is_true:
                        game_question.right_answer = letter
                game_question.save()
            else:
                self.stop()
        return question, answers, number

    def current_game_question(self):
        try:
            game_question = self.game_questions.order_by('-asked_at')[0:1].get(
            )
            return game_question
        except GameQuestion.DoesNotExist:
            return None

    def result(self):
        result = {
            'state': self.state,
            'total_questions':
                self.test.questions.filter(published=True).count(),
            'asked_questions': self.game_questions.count(),
            'right_answers':
                GameQuestion.objects.right_answers(game=self).count(),
        }
        return result

    def __unicode__(self):
        return u"%s Test: %s. Player: %s" % (self.start_on, self.test,
                                             self.player)

    def __str__(self):
        return u"%s Test: %s. Player: %s" % (self.start_on, self.test,
                                             self.player)


class GameQuestion(models.Model):
    class Meta:
        unique_together = (('game', 'question'),)

    game = models.ForeignKey('Game', related_name='game_questions')
    question = models.ForeignKey('Question')
    right_answer = models.CharField(_('Letter of right answer'),
                                    blank=True,
                                    max_length=1)
    player_answer = models.CharField(_('Player answer'), blank=True, max_length=1)
    asked_at = models.DateTimeField(_('When was asked'), auto_now_add=True)
    answered_at = models.DateTimeField(_('When was answered'),
                                       null=True,
                                       blank=True)
    objects = GameQuestionManager()

    def reply(self, answer):
        answer = answer.lower()
        game = self.game
        if game.state == Game.OPEN:
            self.answered_at = timezone.now()
            self.player_answer = answer
            self.save()
            if self.right_answer == answer:
                return True
            else:
                return False

    def is_right(self):
        if self.player_answer:
            if self.player_answer == self.right_answer:
                return True
        return False

    def __unicode__(self):
        return u"%s, %s" % (self.game, self.question)

    def __str__(self):
        return u"%s, %s" % (self.game, self.question)
