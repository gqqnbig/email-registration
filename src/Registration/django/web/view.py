import django.http
import uuid
import subprocess

from django.shortcuts import render
from django.core.mail import send_mail
from django.core.cache import cache
from django.conf import settings

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

		usePublicKey = request.POST['key'] == 'true'
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

		if request.POST['major'] == 'cs' and usePublicKey:
			guid = uuid.uuid4().hex
			accountInfo = {
				'email': email,
				'username': username,
				'publicKey': publicKey,
			}
			cache.set('verify-' + guid, accountInfo, 30 * 60)

			message = f'Click <a href="http://aha.ipm.edu.mo/verify?id={guid}">this link</a> to activate your account. The link is valid for 30 minutes.'
			# send_mail('Shine account verification', message, 'aha@ipm.edu.mo', [email], html_message=message)
			print(f'{guid} -> {accountInfo}')
			return django.http.HttpResponse(f'A verification email has been sent to {email}. Click the link in the email to activate your account.')


def verify(request: django.http.HttpRequest):
	guid = request.GET.get('id', '')
	accountInfo = cache.get('verify-' + guid)
	if accountInfo is None:
		response = django.http.HttpResponse('Incorrect parameters')
		response.status_code = 404
		return response
	else:
		cache.delete('verify-' + guid)

		subprocess.check_output([settings.CREATE_ACCOUNT, accountInfo['username'], accountInfo['email'], accountInfo['publicKey']])
		return django.http.HttpResponse(f'Account {accountInfo["username"]} is created on aha.ipm.edu.mo.')

