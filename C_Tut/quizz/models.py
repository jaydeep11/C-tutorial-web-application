from __future__ import unicode_literals
import re
import json

from django.db import models
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import (
    MaxValueValidator, validate_comma_separated_integer_list,
)
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings

from model_utils.managers import InheritanceManager

from home.models import student
from tutorials.models import Tutorial

class Quiz(models.Model):
    tutorial=models.OneToOneField(Tutorial,default="",on_delete=models.CASCADE,null=True)
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=60, blank=False)

    description = models.TextField(
        verbose_name=_("Description"),
        blank=True, help_text=_("a description of the quiz"))
    
    random_order = models.BooleanField(
        blank=False, default=False,
        verbose_name=_("Random Order"),
        help_text=_("Display the questions in "
                    "a random order or as they "
                    "are set?"))

    max_questions = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("Max Questions"),
        help_text=_("Number of questions to be answered on each attempt."))

    answers_at_end = models.BooleanField(
        blank=False, default=False,
        help_text=_("Correct answer is NOT shown after question."
                    " Answers displayed at the end."),
        verbose_name=_("Answers at end"))

    pass_mark = models.SmallIntegerField(
        blank=True, default=0,
        verbose_name=_("Pass Mark"),
        help_text=_("Percentage required to pass exam."),
        validators=[MaxValueValidator(100)])

    success_text = models.TextField(
        blank=True, help_text=_("Displayed if user passes."),
        verbose_name=_("Success Text"))

    fail_text = models.TextField(
        verbose_name=_("Fail Text"),
        blank=True, help_text=_("Displayed if user fails."))
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.pass_mark > 100:
            raise ValidationError('%s is above 100' % self.pass_mark)

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)
    
    class Meta:
        verbose_name = _("Quizz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all().select_subclasses()
    
    @property
    def get_max_score(self):
        return self.get_questions().count()

class ProgresssManager(models.Manager):

    def new_progresss(self, student):
        new_progress = self.create(student=student,
                                   score="")
        new_progress.save()
        return new_progress
        
class Progresss(models.Model):
    student=models.OneToOneField(student,default="",on_delete=models.CASCADE,null=True)
    
    score = models.CharField(max_length=1024,
                             verbose_name=_("Score"),
                             validators=[validate_comma_separated_integer_list])

    objects = ProgresssManager()

    class Meta:
        verbose_name = _("User Progress")
        verbose_name_plural = _("User progress records")
        
    @property
    def list_all_tut_scores(self):
        """
        Returns a dict in which the key is the category name and the item is
        a list of three integers.
        The first is the number of questions correct,
        the second is the possible best score,
        the third is the percentage correct.
        The dict will have one key for every category that you have defined
        """
        score_before = self.score
        output = {}

        for tut in Tutorial.objects.all():
            to_find = re.escape(tut.name) + r",(\d+),(\d+),"
            #  group 1 is score, group 2 is highest possible

            match = re.search(to_find, self.score, re.IGNORECASE)

            if match:
                score = int(match.group(1))
                possible = int(match.group(2))

                try:
                    percent = int(round((float(score) / float(possible))
                                        * 100))
                except:
                    percent = 0

                output[tut.name] = [score, possible, percent]

            else:  # if category has not been added yet, add it.
                self.score += tut.name + ",0,0,"
                output[tut.name] = [0, 0]

        if len(self.score) > len(score_before):
            # If a new category has been added, save changes.
            self.save()

        return output

    def update_score(self, question, score_to_add=0, possible_to_add=0):
        """
        Pass in question object, amount to increase score
        and max possible.
        Does not return anything.
        """
        tutorial_test = Tutorial.objects.filter(name=question.tutorial).exists()

        if any([item is False for item in [tutorial_test,
                                           score_to_add,
                                           possible_to_add,
                                           isinstance(score_to_add, int),
                                           isinstance(possible_to_add, int)]]):
            return _("error"), _("tutorial does not exist or invalid score")

        to_find = re.escape(str(question.tutorial)) + r",(?P<score>\d+),(?P<possible>\d+),"

        match = re.search(to_find, self.score, re.IGNORECASE)

        if match:
            updated_score = int(match.group('score')) + abs(score_to_add)
            updated_possible = int(match.group('possible')) + abs(possible_to_add)

            new_score = ",".join(
                [
                    str(question.tutorial),
                    str(updated_score),
                    str(updated_possible), ""
                ])

            # swap old score for the new one
            self.score = self.score.replace(match.group(), new_score)
            self.save()

        else:
            #  if not present but existing, add with the points passed in
            self.score += ",".join(
                [
                    str(question.tutorial),
                    str(score_to_add),
                    str(possible_to_add),
                    ""
                ])
            self.save()
            

class Question(models.Model):
    """
    Base class for all question types.
    Shared properties placed here.
    """

    quiz = models.ManyToManyField(Quiz,
                                  verbose_name=_("Quiz"),
                                  blank=True)

    tutorial = models.ForeignKey(Tutorial,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE)

    figure = models.ImageField(upload_to='uploads/%Y/%m/%d',
                               blank=True,
                               null=True,
                               verbose_name=_("Figure"))

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the question text that "
                                           "you want displayed"),
                               verbose_name=_('Question'))

    code = models.TextField(max_length=2000,
                                   blank=True,
                                   help_text=_("code to be solved by user."),
                                   verbose_name=_('Code'))

    explanation = models.TextField(max_length=2000,
                                   blank=True,
                                   help_text=_("Explanation to be shown "
                                               "after the question has "
                                               "been answered."),
                                   verbose_name=_('Explanation'))

    objects = InheritanceManager()

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['tutorial']

    def __str__(self):
        return self.content
    
class TF_Question(Question):
    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Tick this if the question "
                                              "is true. Leave it blank for"
                                              " false."),
                                  verbose_name=_("Correct"))

    def check_if_correct(self, guess):
        if guess == "True":
            guess_bool = True
        elif guess == "False":
            guess_bool = False
        else:
            return False

        if guess_bool == self.correct:
            return True
        else:
            return False

    def get_answers(self):
        return [{'correct': self.check_if_correct("True"),
                 'content': 'True'},
                {'correct': self.check_if_correct("False"),
                 'content': 'False'}]

    def get_answers_list(self):
        return [(True, True), (False, False)]

    def answer_choice_to_string(self, guess):
        return str(guess)

    class Meta:
        verbose_name = _("True/False Question")
        verbose_name_plural = _("True/False Questions")
        ordering = ['tutorial']
        
ANSWER_ORDER_OPTIONS = (
    ('content', _('Content')),
    ('random', _('Random')),
    ('none', _('None'))
)


class MCQuestion(Question):

    answer_order = models.CharField(
        max_length=30, null=True, blank=True,
        choices=ANSWER_ORDER_OPTIONS,
        help_text=_("The order in which multichoice "
                    "answer options are displayed "
                    "to the user"),
        verbose_name=_("Answer Order"))

    def check_if_correct(self, guess):
        answer = Answer.objects.get(id=guess)

        if answer.correct is True:
            return True
        else:
            return False

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by('content')
        if self.answer_order == 'random':
            return queryset.order_by('?')
        if self.answer_order == 'none':
            return queryset.order_by()
        return queryset

    def get_answers(self):
        return self.order_answers(Answer.objects.filter(question=self))

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in
                self.order_answers(Answer.objects.filter(question=self))]

    def answer_choice_to_string(self, guess):
        return Answer.objects.get(id=guess).content

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")


@python_2_unicode_compatible
class Answer(models.Model):
    question = models.ForeignKey(MCQuestion, verbose_name=_("Question"), on_delete=models.CASCADE)

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Content"))

    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Is this a correct answer?"),
                                  verbose_name=_("Correct"))

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
    
class SittingManager(models.Manager):

    def new_sitting(self, student, quiz):
        if quiz.random_order is True:
            question_set = quiz.question_set.all().select_subclasses().order_by('?')
        else:
            question_set = quiz.question_set.all().select_subclasses()

        question_set = [item.id for item in question_set]

        if len(question_set) == 0:
            raise ImproperlyConfigured('Question set of the quiz is empty. '
                                       'Please configure questions properly')

        if quiz.max_questions and quiz.max_questions < len(question_set):
            question_set = question_set[:quiz.max_questions]

        questions = ",".join(map(str, question_set)) + ","

        new_sitting = self.create(student=student,
                                  quiz=quiz,
                                  question_order=questions,
                                  question_list=questions,
                                  incorrect_questions="",
                                  current_score=0,
                                  complete=False,
                                  user_answers='{}')
        return new_sitting
    
    def user_sitting(self, student, quiz):
        try:
            sitting = self.get(student=student, quiz=quiz, complete=False)
        except Sitting.DoesNotExist:
            sitting = self.new_sitting(student, quiz)
        except Sitting.MultipleObjectsReturned:
            sitting = self.filter(student=student, quiz=quiz, complete=False)[0]
        return sitting

class Sitting(models.Model):
    student = models.ForeignKey(student, on_delete=models.CASCADE)

    quiz = models.ForeignKey(Quiz, verbose_name=_("Quiz"), on_delete=models.CASCADE)

    question_order = models.CharField(
        max_length=1024,
        verbose_name=_("Question Order"),
        validators=[validate_comma_separated_integer_list])

    question_list = models.CharField(
        max_length=1024,
        verbose_name=_("Question List"),
        validators=[validate_comma_separated_integer_list])

    incorrect_questions = models.CharField(
        max_length=1024,
        blank=True,
        verbose_name=_("Incorrect questions"),
        validators=[validate_comma_separated_integer_list])

    current_score = models.IntegerField(verbose_name=_("Current Score"))

    complete = models.BooleanField(default=False, blank=False,
                                   verbose_name=_("Complete"))

    user_answers = models.TextField(blank=True, default='{}',
                                    verbose_name=_("User Answers"))

    start = models.DateTimeField(auto_now_add=True,
                                 verbose_name=_("Start"))

    end = models.DateTimeField(null=True, blank=True, verbose_name=_("End"))

    objects = SittingManager()

    class Meta:
        permissions = (("view_sittings", _("Can see completed exams.")),)
        
    def get_first_question(self):
        """
        Returns the next question.
        If no question is found, returns False
        Does NOT remove the question from the front of the list.
        """
        if not self.question_list:
            return False

        first, _ = self.question_list.split(',', 1)
        question_id = int(first)
        return Question.objects.get_subclass(id=question_id)

    def remove_first_question(self):
        if not self.question_list:
            return

        _, others = self.question_list.split(',', 1)
        self.question_list = others
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    @property
    def get_current_score(self):
        return self.current_score

    def _question_ids(self):
        return [int(n) for n in self.question_order.split(',') if n]

    @property
    def get_percent_correct(self):
        dividend = float(self.current_score)
        divisor = len(self._question_ids())
        if divisor < 1:
            return 0            # prevent divide by zero error

        if dividend > divisor:
            return 100

        correct = int(round((dividend / divisor) * 100))

        if correct >= 1:
            return correct
        else:
            return 0

    def mark_quiz_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def add_incorrect_question(self, question):
        """
        Adds uid of incorrect question to the list.
        The question object must be passed in.
        """
        if len(self.incorrect_questions) > 0:
            self.incorrect_questions += ','
        self.incorrect_questions += str(question.id) + ","
        if self.complete:
            self.add_to_score(-1)
        self.save()

    @property
    def get_incorrect_questions(self):
        """
        Returns a list of non empty integers, representing the pk of
        questions
        """
        return [int(q) for q in self.incorrect_questions.split(',') if q]

    def remove_incorrect_question(self, question):
        current = self.get_incorrect_questions
        current.remove(question.id)
        self.incorrect_questions = ','.join(map(str, current))
        self.add_to_score(1)
        self.save()

    @property
    def check_if_passed(self):
        return self.get_percent_correct >= self.quiz.pass_mark

    @property
    def result_message(self):
        if self.check_if_passed:
            return self.quiz.success_text
        else:
            return self.quiz.fail_text

    def add_user_answer(self, question, guess):
        current = json.loads(self.user_answers)
        current[question.id] = guess
        self.user_answers = json.dumps(current)
        self.save()

    def get_questions(self, with_answers=False):
        question_ids = self._question_ids()
        questions = sorted(
            self.quiz.question_set.filter(id__in=question_ids)
                                  .select_subclasses(),
            key=lambda q: question_ids.index(q.id))

        if with_answers:
            user_answers = json.loads(self.user_answers)
            for question in questions:
                question.user_answer = user_answers[str(question.id)]

        return questions

    @property
    def questions_with_user_answers(self):
        return {
            q: q.user_answer for q in self.get_questions(with_answers=True)
        }

    @property
    def get_max_score(self):
        return len(self._question_ids())

    def progress(self):
        """
        Returns the number of questions answered so far and the total number of
        questions.
        """
        answered = len(json.loads(self.user_answers))
        total = self.get_max_score
        return answered, total
