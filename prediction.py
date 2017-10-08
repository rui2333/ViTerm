import tensorflow as tf
import numpy as np
import json, time, os

saver = tf.train.import_meta_graph('./model/{}.meta'.format("tf_model"))
graph = tf.get_default_graph()

sess = tf.Session()
saver.restore(sess, './model/{}'.format("tf_model"))

x = graph.get_tensor_by_name("x:0")
y = graph.get_tensor_by_name("y:0")

alpha = "abcdefghiklmnopqrstuvwxy"

def predict(example):
	instance, label = np.array([example[0]]), np.array([example[1]])

	output = sess.run([y], feed_dict={x: instance})

	output = output[0][0]
	arg = np.argmax(output)
	y_exp = [min(max(0, np.exp(i)), 1000000) for i in output]
	softmax = [float(i) / np.sum(y_exp) for i in y_exp]
	confidence = max(softmax)

	char = alpha[arg]

	return char, confidence

def pre_process (dic):
	fingers, hand = dic['fingers'], dic['hand']

	if fingers == []:
		return None

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

	label = [0] * 24

	return [clean_inst, label]
