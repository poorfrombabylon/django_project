from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import register
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Choice, Question, QuestionList, ResultsModel, ResultChoiceModel
from django.db import IntegrityError


def get_current_session_for_ql(uid, qlid):
    return ResultsModel.objects.all().filter(uid=uid, questionlist=qlid,
                                             date_end__isnull=True)


def get_all_finished_sessions():
    return ResultsModel.objects.all().filter(date_end__isnull=False)


def get_finished_session(uid, qlid):
    return ResultsModel.objects.all().filter(uid=uid, questionlist=qlid,
                                             date_end__isnull=False)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return QuestionList.objects.filter(pub_date__lte=timezone.now())

    @register.filter(name='cut')
    def cut(ql_id, user_id):
        session_id = get_current_session_for_ql(user_id, ql_id)
        finished_session_id = get_finished_session(user_id, ql_id)
        if session_id.exists():
            return 1
        elif finished_session_id.first() != None and finished_session_id.first().date_end != None:
            return 3
        else:
            return 2

    # def get_context_data(self, **kwargs):
    #    context = super(IndexView, self).get_context_data(**kwargs)
    #    context['get_current_session_for_ql'] = get_current_session_for_ql()
    #    return context


class DetailView(generic.DetailView):
    model = QuestionList
    template_name = 'polls/detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if get_current_session_for_ql(request.user.id, kwargs['pk']).exists():
            print('works')
        else:
            new_session = ResultsModel(uid=request.user.id,
                                       questionlist=get_object_or_404(QuestionList, pk=kwargs['pk']),
                                       date_start=timezone.now())
            new_session.save()
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    @register.filter(name='kek')
    def kek(result, q_id):
        boom = ResultChoiceModel.objects.all().filter(result=result, question_id=q_id).first()
        if boom != None:
            return boom.choice_id
        else:
            return 0

    @register.filter(name='turbokek')
    def turbokek(ql_id, user_id):
        return get_current_session_for_ql(user_id, ql_id).first().id


class ResultsView(generic.DetailView):
    model = QuestionList
    template_name = 'polls/results.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ResultsView, self).dispatch(request, *args, **kwargs)


@login_required
def vote(request, questionlist_id):
    questionlist = get_object_or_404(QuestionList, pk=questionlist_id)
    for question in questionlist.question_set.all():
        check_choice = request.POST.get('choice[' + str(question.id) + ']')
        if check_choice != None:
            selected_choice = question.choice_set.get(pk=check_choice)
            selected_choice.votes += 1
            selected_choice.save()
            res_qs_obj = ResultChoiceModel.objects.all().filter(question_id=question.id,
                                                                result_id=get_current_session_for_ql(request.user.id,
                                                                                                     questionlist_id).first().id)
            if res_qs_obj.exists():
                res_obj = res_qs_obj.first()
                res_obj.choice_id = check_choice
                res_obj.save()
            else:
                session_id = get_current_session_for_ql(request.user.id, questionlist_id).first()
                new_session_kek = ResultChoiceModel(choice_id=selected_choice.id, question_id=question.id,
                                                    result=get_object_or_404(ResultsModel, pk=session_id.id))
                new_session_kek.save()

    if get_current_session_for_ql(request.user.id, questionlist_id).exists():
        flag = ResultChoiceModel.objects.all().filter(
            result_id=get_current_session_for_ql(request.user.id, questionlist_id).first().id).count()
        quantity = questionlist.question_set.all().count()
        if flag == quantity:
            good = ResultsModel.objects.all().filter(uid=request.user.id, questionlist=questionlist_id,
                                                     date_end__isnull=True).first()
            good.date_end = timezone.now()
            good.save()
    return HttpResponseRedirect(reverse('polls:results', args=(questionlist.id,)))


@login_required()
def ultra(request):
    all_sessions = get_all_finished_sessions()
    results = {}
    counter = 1
    cc = 1
    ch = {}
    for session in all_sessions:
        questions = Question.objects.all().filter(questionlist_id=session.questionlist_id)
        for q in questions:
            answer = ResultChoiceModel.objects.all().filter(result_id=session.id, question_id=q.id)
            results[str(session.uid) + '_' + str(session.questionlist_id) + '_' + str(q.id)] = {
                'counter': counter,
                'q_text': q.question_text,
                'qn_text': QuestionList.objects.all().filter(id=session.questionlist_id).first().question_list_text,
                'mykekochoice': Choice.objects.all().filter(pk=answer.first().choice_id).first().choice_text,
                'realmyname': User.objects.all().filter(pk=session.uid).first().first_name,
            }
            counter += 1
    for list in QuestionList.objects.all():
        for question in list.question_set.all():
            for choice in question.choice_set.all():
                ch[str(list.id) + '_' + str(question.id) + '_' + str(choice.id)] = {
                    'questionlist': list.question_list_text,
                    'question': question.question_text,
                    'choice': choice.choice_text,
                    'votes': choice.votes,
                    'cc': cc
                }
                cc += 1

    return render(request, "polls/ultra.html", {'results': results, 'ch': ch})
