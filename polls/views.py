from django.http import HttpResponse, HttpResponseRedirect
# from django.http import Http404
# from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
#from django.template import loader
from .models import Choice, Question
from django.utils import timezone
# Create your views here.
# class IndexView(generic.ListView):

# 	template_name = 'polls/index.html'
# 	context_object_name = 'latest_question_list'
# 	def get_queryset(self):
# 	"""
# 	Return the last five published questions (not including those set to be published in the future).
# 	"""
# 		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')[:5]
class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'
	def get_queryset(self):
		"""
		Excludes any questions that arent published yet.
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question+list'
	def get_queryset(self):
		"""
		Return the last five published questions (not including those set to be published in the future)
		"""
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
# def results(request, question_id):
	# question = get_object_or_404(Question, pk=question_id)
	# return render(request, 'polls/results.html', {'question':question})


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST
['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html',{'question': question,
		'error_message': "You didnt slect a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()	
		return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))	
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
		# output = ', '.join([q.question_text for q in latest_question_list])
	# return HttpResponse(template.render(context, request))
def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	# try:
	# 	question = Question.objects.get(pk=question_id)
	# except Question.DoesNotExist:
	# 	raise Http404("Question does not exist")
	return render(request, 'polls/detail.html',{'question': question })
	# return HttpResponse("You're looking at question %s." % question_id)
def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)
def vote (request, question_id):
	return HttpResponse("You're voting on question %s." %question_id)
	