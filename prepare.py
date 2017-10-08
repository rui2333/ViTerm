import os, json, sys

folder = "trainings/"
output_name = "processed_trained_data.json"
if (len(sys.argv) > 1 and sys.argv[1] == "test"):
	folder = "tests/"
	output_name = "processed_test_data.json"


alph = "abcdefghijklmnopqrstuvwxyz"

all_examples = []

for example in os.listdir(folder):
	example_name = example
	letter = example_name[:1]


	with open (folder + example_name) as json_file:
		og_inst = json.load(json_file)

	fingers, hand = og_inst['fingers'], og_inst['hand']

	clean_inst = []

	palm_position = hand['palm_position']

	for i in range(5):
		for finger in fingers:
			if (finger['type'] == i):
				bones = finger['bone']
				for bone in bones:
					clean_inst += [bone['length']]
					clean_inst += [i * 100 for i in bone['direction']]
					clean_inst += [center - palm for center, palm in zip(bone['center'], palm_position)]

	clean_inst += [wrist - palm for wrist, palm in zip(hand['wrist_position'], palm_position)]
	clean_inst += hand['palm_position']

	clean_inst = clean_inst[4:]

	label = [0] * 26
	label[alph.find(letter)] = 1

	examp = [clean_inst, label]

	all_examples.append(examp)


with open(output_name, 'w') as write_file:
	write_file.write(json.dumps({"data": all_examples}, indent=4))
