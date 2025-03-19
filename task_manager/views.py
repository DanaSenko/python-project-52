from django.views.generic import TemplateView
from django.http import HttpResponse
import rollbar

def test_rollbar(request):
    try:
        # Генерация тестовой ошибки
        raise ValueError("This is a test error for Rollbar")
    except Exception as e:
        # Отправка ошибки в Rollbar
        rollbar.report_exc_info()
        return HttpResponse("An error occurred, but it's been reported to Rollbar.")

class IndexView(TemplateView):
    template_name = "index.html"
