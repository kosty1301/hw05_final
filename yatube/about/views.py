from django.views.generic.base import TemplateView
from django.conf import settings as conf_settings

TITLE_DICT = conf_settings.TITLE_DICT


class AboutAuthor(TemplateView):
    template_name = 'about/author.html'

    def get_context_data(self, **kwargs):
        title = TITLE_DICT.get('AboutAuthor')
        context = super().get_context_data(**kwargs)
        context['title'] = title

        return context


class TechAuthor(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        title = TITLE_DICT.get('TechAuthor')
        context = super().get_context_data(**kwargs)
        context['title'] = title

        return context
