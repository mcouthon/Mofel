import requests
from parsers import ParserFactory
from json_handler import JSONHandler

readability_token = 'c302342e901b8a2658cf4f5b52e27dd66313e32a'
url = 'http://minimalistbaker.com/cheesy-jalapeno-corn-dip/'

if __name__ == '__main__':
	if False:
		html_text = requests.get(url).text

	if True:
		with open('tmp/cheesy-jalapeno-corn-dip.html', 'r') as json_file:
			html_text = json_file.read().decode('utf8')

	parser_factory = ParserFactory()
	parser = parser_factory.get_parser('minimalistbaker.com')
	JSONHandler.write_json(url, parser.parse_html(html_text))
