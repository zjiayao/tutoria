from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from account.models import (User, Tutor)

class IndexView(generic.TemplateView):
    template_name = 'result.html'
    # context_object_name = 'index_context'

class ResultView(generic.TemplateView):
     # tutor_list = Tutor.objects()
     template_name = 'result.html'
     context_object_name = 'results'