from .models import Question, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # :returns: the last five questions made without those in the future
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


"""
def index(generic.ListView):
    #this function shows the latest questions made by the users and displays the last 5
    #returns the render view of the index view with the questions from the  db
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)
"""


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        excludes any question that aren't published yet
        :return:
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

"""
def detail(request, question_id):
    #shows the details of
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
"""


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

"""
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
"""


def vote(request, question_id):

    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # showing the question voting form
        return render(request, 'polls/details.html', {'question': question,
                                                      'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # always returning an HttpresponseRedirect after successfully dealing with Post date
        # This prevents data from being posted twice if the user hits the back button

        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

"""
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""
