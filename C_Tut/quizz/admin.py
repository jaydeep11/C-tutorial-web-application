from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _

from .models import Quiz,Progresss,Question,MCQuestion,TF_Question,Answer
from tutorials.models import Tutorial
# Register your models here.
class AnswerInline(admin.TabularInline):
    model = Answer


class QuizAdminForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz


class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm

    list_display = ('title', 'tutorial', )
    list_filter = ('tutorial',)
    search_fields = ('description', 'tutorial', )

class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'tutorial', )
    list_filter = ('tutorial',)
    fields = ('content', 'tutorial',
              'figure','code', 'quiz', 'explanation', 'answer_order')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

    inlines = [AnswerInline]


class ProgresssAdmin(admin.ModelAdmin):
    """
    to do:
            create a user section
    """
    search_fields = ('student', 'score', )


class TFQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', )
    fields = ('content', 'tutorial',
              'figure', 'quiz', 'explanation', 'correct',)

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

admin.site.register(Quiz, QuizAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Progresss, ProgresssAdmin)
admin.site.register(TF_Question, TFQuestionAdmin)