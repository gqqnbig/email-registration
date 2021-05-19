from django.shortcuts import render
import django.http

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

		usePublicKey = request.POST['key'] == 'yes'
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
			return django.http.HttpResponse('A verification email has been sent to . Click the link in the email to activate your account.')
