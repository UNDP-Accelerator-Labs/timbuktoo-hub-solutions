from sys import argv, path as syspath
from os.path import join, dirname
import json, re

import pandas as pd
from ollama import chat

## CUSTOM MODULES
syspath.append(join(dirname(__file__), './'))
from prompts import RATING_INNOVATIONS_IN_AFRICA

# JOSHCI'S PROMPTS
# https://github.com/UNDP-Accelerator-Labs/nlpapi/blob/main/nlpapi/default_prompts.py

# doc = """Field Digital Skills: Micro-courses via WhatsApp for farmers
# This platfrom is developed by the CGIAR Digital Innovation Initiative, offers micro - courses to farmers via WhatsApp. It capitalizes on the growing smartphone penetration, especially in regions like sub - Saharan Africa. Unlike conventional e - learning platforms, it addresses the challenges of self - regulated learning for farmers. Through a meticulous process involving learner profiling, goal setting, and iterative design, it crafts bite - sized micro - courses. These are bundled into learning routes; currently, "Field Digital Skills, Level 1" is available, comprising four courses on smartphone learning essentials.
# Farmers can enroll by registering their mobile numbers on the CO - LAB Learning Network. All instructional videos are conveniently hosted on a YouTube playlist, ensuring easy access for learners seeking to enhance their digital skills and improve farming practices through this innovative, mobile - first learning solution.
# training and learning
# private sector
# short term (up to 1 year)
# long term (5 and above)"""

def summarize (article):
	stream: ChatResponse = chat(
		model='llama3.2:3b-instruct-q4_1', 
		options= {
			'seed': 42,
			'temperature': 0.2,
			'num_predict': 500,
		},
		messages = [
			{
				'role': 'system',
				'content': RATING_INNOVATIONS_IN_AFRICA,
			},
			{
				'role': 'user',
				'content': f"Please rate the following article: {article}"
			},
		],
		stream=True,
	)

	full_response = ''

	for chunk in stream:
		# print(chunk['message'])
		print(chunk['message']['content'], end='', flush=True)
		full_response += chunk['message']['content']
	print('\n')
	return full_response.replace('```', '')

def main ():
	if len(argv) < 2:
		print ('missing data file location')
	else:
		output = []
		data = pd.read_excel(argv[1])
		page = int(argv[2])
		limit = int(argv[3])
		# docs = data[~pd.isna(data['content'])]['content'].to_list()
		for i,r in data[page*limit:(page+1)*limit].iterrows():
			try:
				doc = re.sub(r'\s+', ' ', r['content'])
				categorized = summarize(doc)
				categorized = json.loads(categorized)
				categorized['pad_id'] = r['pad_id']
				output.append(categorized)
			except:
				print(f'rejected {r['pad_id']}')
		
		with open(f'out/categorized-{page+1}.json', 'w') as f:
			json.dump(output, f)

if __name__ == '__main__':
	main()