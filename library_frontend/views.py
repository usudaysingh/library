import os
import requests
import time
import zipfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse, QueryDict
# from django.shortcuts import RequestContext, render_to_response
from django.shortcuts import render
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
# from wkhtmltopdf.views import PDFTemplateResponse

class HomeView(View):
	template = 'home.html'

	def get(self, request, *args, **kwargs):
		return render(request, self.template)