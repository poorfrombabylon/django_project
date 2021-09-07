from urllib.parse import urlencode, unquote
from django.contrib import admin
from django.utils.html import format_html

from .models import Question, Choice, QuestionList
from django.urls import reverse


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionInLine(admin.TabularInline):
    model = Question
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']
    fieldsets = [
        (None, {'fields': ['question_text', 'questionlist']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'questionlist', 'was_published_recently')
    list_filter = ['pub_date']

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionAdmin, self).get_form(request, obj=obj, **kwargs)
        ql1 = request.GET.get('ql1')
        if ql1 != None:
            questionlist = QuestionList.objects.get(id=ql1)
            form.base_fields['questionlist'].initial = questionlist
        # if request.user.is_superuser:
        #    pass
        # else:
        #    shops = Shop.objects.filter(user_id=user.id)
        #    form.base_fields['refShop'].initial = shops[0]

        return form

    def get_preserved_filters(self, request):
        form = super(QuestionAdmin, self).get_preserved_filters(request)
        ql1 = request.GET.get('questionlist__id')
        pretail = ""
        if len(form) > 0:
            pretail += form + "&"
        if ql1 != None:
            pretail += urlencode({'ql1': ql1})
        return pretail


class QuestionListAdmin(admin.ModelAdmin):
    list_display = ('view_questions_link',)

    def view_questions_link(self, obj):
        url = (
                reverse("admin:polls_question_changelist")
                + "?"
                + urlencode({"questionlist__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{}</a>', url, obj.question_list_text)


admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionList, QuestionListAdmin)
