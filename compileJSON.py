import json
from os import listdir
from os.path import splitext

def main():
	files = listdir('./out/all_africa')
	jsonfiles = [f for f in files if splitext(f)[1] == '.json' and f != 'full_dataset.json']

	data = []
	for f in jsonfiles:
		print(f)
		for d in open(f'./out/all_africa/{f}'):
			j = json.loads(d)
			data += j

	print(len(data))

	with open('./out/full_dataset.json', 'w') as f:
		json.dump(data, f)

if __name__ == '__main__':
	main()