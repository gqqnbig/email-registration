from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	# return HttpResponse("Hello, world. You're at the polls index.")

	return render(request, 'index.html', {}, content_type='text/html')
