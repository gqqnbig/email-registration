import requests


def test_html5Conformance(websiteUrl):
	response = requests.get(websiteUrl)
	assert len(response.text) > 0

	validationResult = requests.post('https://validator.w3.org/nu/?out=json', headers={'Content-type': 'text/html; charset=utf-8'}, data=response.text.encode('utf-8'))

	json = validationResult.json()
	messages = json['messages']
	errors = [m for m in messages if m['type'] == 'error']

	# OK to have 'Attribute “v-xxx” not allowed on element
	errors = [m for m in errors if 'Attribute “v-' not in m['message']]
	# OK to use v-bind shorthand
	errors = [m for m in errors if 'Attribute “:' not in m['message']]

	assert len(errors) == 0


if __name__ == '__main__':
	test_html5Conformance('http://127.0.0.1:8000/')
