# -*- encoding: utf-8 -*-
import os

import yaml
from django.core.management.base import BaseCommand

from testapp.models import Test, Question, Answer, TestQuestion


def validate_test(test):
    return True


def parse(path):
    abs_path = os.path.abspath(path)

    assert os.path.isfile(abs_path), "Not found file with data"

    with open(abs_path, 'r') as fio:
        data = yaml.load(fio.read())

    assert data, "File is empty"

    for x in data:
        assert validate_test(x), "Not valid test"
        obj_test = Test(**x.get('info', {}))
        obj_test.save()

        for question in x.get('questions', []):
            obj_question = Question(**question.get('question', {}))
            obj_question.save()

            for answer in question.get('answers'):
                obj_answer = Answer(**answer)
                obj_answer.question = obj_question
                obj_answer.save()

            TestQuestion(test=obj_test, question=obj_question).save()


class Command(BaseCommand):
    help = 'Import test from file'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str)

    def handle(self, *args, **options):
        if 'path' in options:
            parse(options['path'])
        else:
            print('Not found path')
