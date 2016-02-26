from django.test import TestCase
from .models import Test, Player, Game
from .exceptions import TestIsNotAvailable

class TestTestCase(TestCase):
    def setUp(self):
        test = Test.objects.create(
            name="Test1",
            published=True
        )
        player = Player.objects.create(tgm_user_id=1)

    def test_method_check_availability_if_not_published(self):
        """Test is not available, if it is not published"""   
        test = Test.objects.get(name="Test1")
        test.published = False
        test.save()
        player = Player.objects.get(tgm_user_id=1)
        with self.assertRaises(TestIsNotAvailable):
            test.check_availability(player=player)

    def test_method_check_availability_time_interval(self):
        """Test is not available, if test interval time doesn't expire"""
        test = Test.objects.get(name="Test1")
        test.interval = 60*60*24*30
        test.save()
        player = Player.objects.get(tgm_user_id=1)
        game = Game.manager.create_game(player=player, test=test)
        game.stop()
        with self.assertRaises(TestIsNotAvailable):
            test.check_availability(player=player)        

    def test_method_check_availability_there_are_not_game(self):
        """Test is not available, if there is an open game"""
        test = Test.objects.get(name="Test1")
        player = Player.objects.get(tgm_user_id=1)
        game = Game.manager.create_game(player=player, test=test)
        with self.assertRaises(TestIsNotAvailable):
            test.check_availability(player=player)


class TestResultCase(TestCase):
    def setUp(self):
        pass
    def test_calculate_score(self):
        """if zero number of questions in test, score is zero"""
        pass


class TestResultViewCase(TestCase):
    def setUp(self):
        pass
    def test_score_method(self):
        """if zero number of questions in test, score is zero"""
        pass    
    def test_if_unpublished_test(self):
        """"""
        pass