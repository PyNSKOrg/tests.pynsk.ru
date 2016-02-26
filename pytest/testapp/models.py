from __future__ import division
from django.db import models
from django.db.models import F
from django.utils import timezone
from datetime import timedelta
from sql import create_testapp_resultview
from managers import GameManager, PlayerManager, TestManager, GameQuestionManager, ResultViewManager
from exceptions import TestIsNotAvailable


def gen_letter():
    import string
    alphabet = string.ascii_lowercase
    for char in alphabet:
        yield char


def calculate_result_score(total_questions, right_answers):
    if total_questions == 0:
        return 0
    return round((right_answers / total_questions) * 5, 2)


class Question(models.Model):
    OPEN = 'O'
    CLOSE = 'C'
    QTYPE = (
        (OPEN, "open question"),
        (CLOSE, "close question"),
    )
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
    text = models.CharField("Question text", max_length=2000)
    created_on = models.DateTimeField("When was created", auto_now_add=True)
    changed_on = models.DateTimeField("When was last changed ", auto_now=True)
    published = models.BooleanField("is published", default=True)
    qtype = models.CharField("question type", choices=QTYPE, max_length=10, default=CLOSE)

    def __unicode__(self):
        return u"%s" % (self.text)


class Test(models.Model):
    name = models.CharField("Test name", max_length=200)
    created_on = models.DateTimeField("When was created", auto_now_add=True)
    changed_on = models.DateTimeField("When was last changed ", auto_now=True)
    questions = models.ManyToManyField(Question, through='TestQuestion')
    published = models.BooleanField("is published", default=False)
    author = models.CharField("Author", max_length=200, blank=True)
    description = models.CharField("Description", max_length=2000, blank=True)
    interval = models.PositiveIntegerField("Retake interval in seconds", default=0)
    objects = models.Manager()
    manager = TestManager()

    def get_interval(self):
        tdelta = timedelta(seconds=self.interval)
        result = {"day": tdelta.days}
        result["hour"], rem = divmod(tdelta.seconds, 3600)
        result["minute"], result["second"] = divmod(rem, 60)
        return result
        
    def check_availability(self, player):
        if not self.published:
            raise TestIsNotAvailable()
        last_game = self.games.filter(player=player).order_by("-start_on").first()
        if not last_game:
            return True
        if last_game.state == Game.OPEN:
            raise TestIsNotAvailable()
        interval = timedelta(seconds=self.interval)
        available_time = last_game.stop_on + interval
        if timezone.now() > available_time:
            return True
        else:
            raise TestIsNotAvailable(available_time=available_time)


    def __unicode__(self):
        return u"%s" % (self.name)


class Player(models.Model):
    tgm_user_id = models.CharField("Telegram user id", max_length=2000, unique=True)
    tgm_first_name = models.CharField("Telegram user's first name", max_length=2000, blank=True)
    tgm_last_name = models.CharField("Telegram user's last name", max_length=2000, blank=True)
    tgm_user_name = models.CharField("Telegram username", max_length=2000, blank=True)
    tests = models.ManyToManyField(Test, through='Game')
    objects = models.Manager()
    manager = PlayerManager()

    def stop_game(self):
        games = self.games.filter(state=Game.OPEN)
        for game in games:
            game.stop()

    def current_game(self):
        """
        Return open game. If multiple return last open game.
        Otherwise return None.
        """
        try:
            return self.games.get(state=Game.OPEN)
        except Game.DoesNotExist:
            return None
        except Game.MultipleObjectsReturned:
            return self.games.filter(state=Game.OPEN).order_by('-start_on').first()

    def get_rating(self):
        rating = []
        all_result = ResultView.objects.all()
        player_result_list = [ 
            result for result in all_result if result.player == self 
        ]
        for player_result in player_result_list:
            worse_result = 0
            all_test_result = [ res for res in all_result if res.test == player_result.test ]
            for result in all_test_result:
                if result.score() < player_result.score():
                    worse_result += 1
            rating.append((
                player_result,
                round((worse_result / len(all_test_result)) * 100, 2)))
        return rating


    def __unicode__(self):
        return u"%s, %s, %s, %s" % (self.tgm_user_id, self.tgm_last_name, self.tgm_first_name, self.tgm_user_name)


class TestQuestion(models.Model):
    class Meta:
        unique_together = (("test", "question"),)
    test = models.ForeignKey('Test')
    question = models.ForeignKey('Question')
    def __unicode__(self):
        return u"Test: %s. Question: %s" % (self.test, self.question)


class Answer(models.Model):
    MAX_LENGTH = 200
    question = models.ForeignKey('Question', related_name='answers')
    text = models.CharField("Answer text", max_length=MAX_LENGTH)
    answer_description = models.TextField("Answer description", max_length=20000, blank=True)
    is_true = models.BooleanField("is true", default=False)
    def __unicode__(self):
        return u"%s" % (self.text)


class Game(models.Model):
    OPEN = 'O'
    CLOSE = 'C'
    STATE = (
        (OPEN, 'Open game'),
        (CLOSE, 'Close game'),
    )
    player = models.ForeignKey("Player", related_name='games')
    test = models.ForeignKey('Test', related_name='games')
    start_on = models.DateTimeField("when was started", auto_now_add=True)
    stop_on = models.DateTimeField("when was stoped", null=True, blank=True)
    questions = models.ManyToManyField("Question", through='GameQuestion')
    state = models.CharField("Game state", choices=STATE, max_length=10, default=OPEN)
    objects = models.Manager()
    manager = GameManager()

    def stop(self):
        if self.state == Game.OPEN:
            self.state = Game.CLOSE
            self.stop_on = timezone.now()
            self.save()

    def no_more_questions(self):
        asked_questions = self.questions.all()
        not_asked_questions = self.test.questions.filter(published=True).exclude(id__in=asked_questions)
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
            not_asked_questions = self.test.questions.filter(published=True).exclude(id__in=asked_questions)
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
        return (question, answers, number)

    def current_game_question(self):        
        try:
            game_question = self.game_questions.order_by('-asked_at')[0:1].get()
            return game_question            
        except GameQuestion.DoesNotExist:
            return None

    def result(self):
        result = {
            'state': self.state,
            'total_questions': self.test.questions.filter(published=True).count(),
            'asked_questions': self.game_questions.count(),
            'right_answers': GameQuestion.objects.right_answers(game=self).count(),            
        }
        result['score'] = calculate_result_score(
            result['total_questions'], result['right_answers']
        )
        return result

    def __unicode__(self):
        return u"%s Test: %s. Player: %s" % (self.start_on, self.test, self.player)


class GameQuestion(models.Model):
    class Meta:
        unique_together = (("game", "question"),)
    
    game = models.ForeignKey("Game", related_name="game_questions")
    question = models.ForeignKey("Question")    
    right_answer = models.CharField("Letter of right answer", blank=True, max_length=1)
    player_answer = models.CharField("Player answer", blank=True, max_length=1)
    asked_at = models.DateTimeField("When was asked", auto_now_add=True)
    answered_at = models.DateTimeField("When was answered", null=True, blank=True)
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


class ResultView(models.Model):
    """Model presenting "testapp_result" postgresql view"""
    SQL = create_testapp_resultview    
    class Meta:
        managed = False        
    id = models.PositiveIntegerField(primary_key=True)    
    player = models.ForeignKey(Player)
    test = models.ForeignKey(Test)
    test_name = models.CharField("Test name", max_length=200)
    number_of_questions = models.PositiveIntegerField()
    number_of_right_answers = models.PositiveIntegerField()
    objects = ResultViewManager()

    def score(self):
        return calculate_result_score(
            self.number_of_questions, 
            self.number_of_right_answers
        )

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def save(self, *args, **kwargs):
        raise NotImplementedError



