import random

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView, FormView

from .forms import QuestionForm
from .models import Quiz, Progresss, Sitting, Question
from tutorials.models import Tutorial
from home.models import student,CPerson

class QuizTake(FormView):
    form_class = QuestionForm
    template_name = 'quizz/question.html'
    result_template_name = 'quizz/result.html'
    single_complete_template_name = 'single_complete.html'

    def dispatch(self, request, *args, **kwargs):
        self.tutorial = get_object_or_404(Tutorial, id=self.kwargs['tutorial_id'])
        self.quiz=self.tutorial.quiz

        try:
            self.logged_in_user = self.request.user.is_authenticated()
        except TypeError:
            self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            cperson=CPerson.objects.get(user=request.user)
            Student=student.objects.get(cperson=cperson)
            self.sitting = Sitting.objects.user_sitting(Student ,self.quiz)

        if self.sitting is False:
            return render(request, self.single_complete_template_name)

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        if self.logged_in_user:
            self.question = self.sitting.get_first_question()
            self.progress = self.sitting.progress()
            
        form_class = self.form_class

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.sitting.get_first_question() is False:
                return self.final_result_user()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['tut_list']=Tutorial.objects.all()
        context['question'] = self.question
        context['quiz'] = self.quiz
        cperson=CPerson.objects.get(user=self.request.user)
        Student=student.objects.get(cperson=cperson)
        context['stu_progress']=Student.progress
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        cperson=CPerson.objects.get(user=self.request.user)
        Student=student.objects.get(cperson=cperson)
        progresss, c = Progresss.objects.get_or_create(student=Student)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progresss.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progresss.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                               .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        cperson=CPerson.objects.get(user=self.request.user)
        Student=student.objects.get(cperson=cperson)
        if self.sitting.check_if_passed and Student.progress==self.get_tut_rank():
            Student.progress=Student.progress+1
            Student.save()
        tut_list=Tutorial.objects.all()
        results = {
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
            'tut_list':tut_list,
            'stu_progress':Student.progress,
        }
        
        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] = self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] = self.sitting.get_incorrect_questions

        return render(self.request, self.result_template_name, results)
    
    def get_tut_rank(self):
        c=1
        rank=0
        while c<=self.tutorial.id:
            curr_tut=Tutorial.objects.filter(pk=c).first()
            if curr_tut:
                rank=rank+1
            c=c+1
        return rank