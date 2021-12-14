import django.http
import uuid
import subprocess
import json
import random

from . import Questions

from django.shortcuts import render
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings
from django.core import serializers
from django.template import loader
from django import forms

usernameMaxLength = 15


def getKeyLength(publicKey: str):
	parts = publicKey.split(' ')
	if len(parts) >= 2:
		return len(parts[1])
	else:
		raise ValueError('Public key format is incorrect.')


def index(request: django.http.HttpRequest):
	context = {}
	context['usernameMaxLength'] = usernameMaxLength

	if request.method == 'GET':
		return render(request, 'index.html', context)
	else:
		email = request.POST['email']

		errors = []
		if email.endswith('@ipm.edu.mo') == False:
			errors.append(f'Email must end with @ipm.edu.mo, but you have {email}.')

		username = request.POST['username']
		if not 5 <= len(username) <= usernameMaxLength:
			errors.append(f'The length of user name must be from 5 to 15, but you have {username}.')

		try:
			subprocess.check_output(['id', '-u', username])
			errors.append(f'{username} already exists.')
		except subprocess.CalledProcessError:
			pass

		usePublicKey = request.POST['key'] == 'true'

		publicKey = None
		if usePublicKey:
			publicKey = request.POST['publicKey']

			if publicKey.startswith('ssh-rsa ') == False:
				errors.append(f'Public key format is incorrect. It must start with "ssh-rsa ", but you have {publicKey[0:10]}...')
			else:
				try:
					if getKeyLength(publicKey) <= 250:
						errors.append('Public key is not long enough. It must at least have 2048 bits.')
				except Exception as e:
					errors.append(e)

		if len(errors) > 0:
			return django.http.HttpResponse('<p>'.join(errors))

		# if request.POST['major'] == 'cs' and usePublicKey:
		guid = uuid.uuid4().hex
		accountInfo = {
			'email': email,
			'username': username,
			'major': request.POST['major'],
			'useZShell': request.POST['useZShell'] == 'true',
		}
		if publicKey:
			accountInfo['publicKey'] = publicKey

		cache.set('verify-' + guid, accountInfo, 30 * 60)

		message = f'Click <a href="{request.scheme}://{request.META["HTTP_HOST"]}/verify?id={guid}">this link</a> to activate your account. The link is valid for 30 minutes.'
		send_mail('Shine Cluster Account Verification', message, 'aha@ipm.edu.mo', [email], html_message=message)
		print(f'{guid} -> {accountInfo}')
		return django.http.HttpResponse(f'A verification email has been sent to {email}. Click the link in the email to activate your account. ')


def verify(request: django.http.HttpRequest):
	guid = request.GET.get('id', '')
	accountInfo = cache.get('verify-' + guid)
	if accountInfo is None:
		response = django.http.HttpResponse('Link is expired.')
		response.status_code = 404
		return response

	if 'publicKey' not in accountInfo or accountInfo['major'] != 'cs':
		if not settings.ADMIN_EMAILS:
			return django.http.HttpResponse('Cluster administrator emails are not set.', status=500)

		message = json.dumps(accountInfo)
		send_mail('Shine account manual creation required', message, 'aha@ipm.edu.mo', settings.ADMIN_EMAILS)
		return django.http.HttpResponse('Cluster administrators will get back to you as soon as possible.')

	if not settings.CREATE_ACCOUNT:
		return django.http.HttpResponse('Create account program is not set up.', status=500)

	commands = [settings.CREATE_ACCOUNT, '--email', accountInfo['email'], '--public-key', accountInfo['publicKey'], accountInfo['username']]
	if accountInfo['useZShell']:
		commands.insert(-1, '--zsh')

	output = ''
	try:
		output = subprocess.check_output(commands, stderr=subprocess.STDOUT)
	except subprocess.CalledProcessError as e:
		print(f'{commands} returns error.\n{e.output}\n\n{str(e)}')
		return django.http.HttpResponse('Server error', status=500)

	cache.delete('verify-' + guid)
	return django.http.HttpResponse(f'Account {accountInfo["username"]} is created.')


def createQuestionSet():
	questions = random.sample(Questions.getQuestions(), 10)
	questions = set(questions)
	questionGroups = [questions]

	while True:
		newGroup = set()
		for q in questionGroups[0]:
			if q.prerequisites is not None:
				newGroup.update(q.prerequisites)
		if len(newGroup) > 0:
			questionGroups.insert(0, newGroup)
		else:
			break

	# remove duplicate questions
	allQuestions = set(questionGroups[0])
	questionGroups[0] = list(questionGroups[0])
	for i in range(1, len(questionGroups)):
		questionGroups[i] = list(filter(lambda q: q not in allQuestions, questionGroups[i]))
		allQuestions.update(questionGroups[i])

	# shuffle
	for group in questionGroups:
		random.shuffle(group)

		for question in group:
			random.shuffle(question.choices)

	return questionGroups


def take_test(request: django.http.HttpRequest):
	questionGroups = request.session.get('QuestionSet', None)
	if questionGroups is None:
		questionGroups = createQuestionSet()
		request.session['QuestionSet'] = questionGroups
		request.session['Page'] = 0

	currentQuestions = questionGroups[request.session['Page']]
	form = forms.Form()

	for question in currentQuestions:
		choices = [(c.text, c.text) for c in question.choices]
		form.fields[question.text] = forms.ChoiceField(label=question.text, choices=choices, widget=forms.RadioSelect)

	return render(request, 'takeTest.html', {'form': form})
