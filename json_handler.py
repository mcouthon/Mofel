import json
import os
import io


class JSONHandler(object):

	@staticmethod
	def write_json(url, json_dict):
		"""
		Write a json dict to file
		:param json_dict: A parsed json dictionary
		"""
		url = url.replace('http://', '').split('/')
		domain, title = url[0], url[1]
		file_path = 'recipes/%s/' % domain
		file_name = '%s/%s.json' % (file_path, title)

		if not os.path.exists(file_path):
			os.makedirs(file_path)

		with io.open(file_name, 'w', encoding='utf8') as outfile:
			data = json.dumps(json_dict, outfile, sort_keys=True, indent=4, ensure_ascii=False)
			outfile.write(unicode(data))


