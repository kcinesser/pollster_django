from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Question, Choice

# Create your views here.

# Get questions and show them
def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  context = {'latest_question_list': latest_question_list}

  return render(request, 'polls/index.html', context)

# Show specific question details
def detail(request, question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Poll not found!")

  return render(request, 'polls/details.html', { 'question': question })

# Show question results
def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)

  return render(request, 'polls/results.html', { 'question': question })

# Submit a vote to a poll
def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try: 
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', { 'question': question, 'error_message': "You didn't seclect a choice.",})
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))