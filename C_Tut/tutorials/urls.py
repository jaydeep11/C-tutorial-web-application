from django.urls import path
from . import views

app_name='tutorials'
urlpatterns=[
    #tutorials/stu_home/
    path('stu_home',views.stu_home,name="stu_home"),
    #tutorials/3/
    path('<int:tutorial_id>/',views.show_tutorial,name="show_tutorial"),
    #tutorials/arithmetic_example
    path('arithmetic_example',views.arithmetic_example,name="arithmetic_example"),
    #tutorials/arithmetic_example
    path('relational_example',views.relational_example,name="relational_example"),
    #tutorials/logical_example
    path('logical_example',views.logical_example,name="logical_example"),
    #tutorials/bitwise_example
    path('bitwise_example',views.bitwise_example,name="bitwise_example"),
    #tutorials/assignment_example
    path('assignment_example',views.assignment_example,name="assignment_example"),
    #tutorials/misc_example
    path('misc_example',views.misc_example,name="misc_example"),
    #tutorials/precedence_example
    path('precedence_example',views.precedence_example,name="precedence_example"),
    #tutorials/if_statement
    path('if_statement',views.if_statement,name="if_statement"),
     #tutorials/ifelse_statement
    path('ifelse_statement',views.ifelse_statement,name="ifelse_statement"),
    #tutorials/nestedif_statement
    path('nestedif_statement',views.nestedif_statement,name="nestedif_statement"),
    #tutorials/switch_statement
    path('switch_statement',views.switch_statement,name="switch_statement"),
    #tutorials/nestedswitch_statement
    path('nestedswitch_statement',views.nestedswitch_statement,name="nestedswitch_statement"),
]