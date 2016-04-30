from bs4 import BeautifulSoup


class ParserFactory(object):
	def __init__(self):
		self._domain_to_parser = {'minimalistbaker.com': MinimalistBakerParser()}

	def get_parser(self, domain):
		return self._domain_to_parser.get(domain, None)


class Parser(object):
	def __init__(self):
		self._bs = None

	def parse_html(self, readability_json):
		pass


class MinimalistBakerParser(Parser):
	def __init__(self):
		super(MinimalistBakerParser, self).__init__()

	def parse_html(self, html_text):
		self._bs = BeautifulSoup(html_text, 'html.parser')
		parsed_dict = dict()

		# This is where the actual recipe is contained
		data = self._bs.find('div', {'class': 'easyrecipe'})
		parsed_dict['Name'] = data.find('div', {'class': 'ERSName'}).text
		times = data.find('div', {'class': 'ERSTimes'})
		parsed_dict['Prep Time'] = times.find('time', {'itemprop': 'prepTime'}).text
		parsed_dict['Total Time'] = times.find('time', {'itemprop': 'totalTime'}).text
		parsed_dict['Summary'] = data.find('div', {'class': 'ERSSummary'}).text

		ingredients = data.find('div', {'class': 'ERSIngredients'})
		parsed_dict['Ingredients'] = self._parse_ingredients(ingredients)

		instructions = data.find('div', {'class': 'ERSInstructions'})
		parsed_dict['Instructions'] = [item.text for item in instructions.find_all('li', {'class': 'instruction'})]

		notes = data.find('div', {'class': 'ERSNotes'})
		parsed_dict['Notes'] = [item.text for item in notes.find_all('br')]

		nutrition = data.find('div', {'class': 'ERSNutrionDetails'})
		l = nutrition.find_all(text=True)
		parsed_dict['Nutritional Details'] = {l[i].strip(): l[i+1] for i in xrange(0, len(l) - 1, 2)}

		return parsed_dict

	@staticmethod
	def _parse_ingredients(ingredients_tag):
		"""
		Parse the ingredients tag
		:param ingredients_tag:
		:return: A dictionary with all the ingredients, grouped in sets for each section
		"""
		ingredients_dict = dict()
		while True:
			div_tag = ingredients_tag.find_next('div')
			if 'ERSSectionHead' in div_tag['class']:
				cur_set = ingredients_dict.setdefault(div_tag.text, list())

				ingredients = div_tag.find_next('ul')
				for ingredient in ingredients.find_all('li', {'class': 'ingredient'}):
					cur_set.append(ingredient.text)
			elif 'ERSClear' in div_tag['class']:
				break

			ingredients_tag = div_tag

		return ingredients_dict
