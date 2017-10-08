import tensorflow as tf 
import numpy as np
import sys, json

#Load data
with open ("processed_train_data.json") as json_file:
	train_data_dict = json.load(json_file)
train_data = train_data_dict["data"]
with open ("processed_test_data.json") as json_file:
	test_data_dict = json.load(json_file)
test_data = test_data_dict["data"]

#Restore model if required
restore_model = False 
if (len(sys.argv) > 1 and sys.argv[1] == "restore"):
	restore_model = True

#Tensorboard filename
with open ('./model/tensorboard_iteration.txt', 'r') as rf:
	itr = int(rf.read())
with open ('./model/tensorboard_iteration.txt', 'w') as wf:
	wf.write(str(itr + 1))

#Config
learning_rate = 0.01
input_num = 142
hidden_num = 24
output_num = 24
batch_size = 50
lmbda = 0.02

def get_batch(data, batch_size=batch_size):
	examples = np.array([data[i] for i in np.random.choice(len(data), batch_size)])
	instance = np.array([np.array(examp[0]) for examp in examples])
	instance -= np.mean(instance, axis=0) #Zero mean
	std = np.std(instance, axis=0)
	std = np.array([max(i, 1e-8) for i in std])
	instance /= std #Unit variance

	# if np.array_equal(instance, np.zeros(shape=(10,142))):
	# 	print instance
	#tf.nn.l2_normalize(instance, 0)

	labels = np.array([np.array(examp[1]) for examp in examples])

	return instance, labels

def main ():
	#Input/Output
	x = tf.placeholder(tf.float32, shape=[None, input_num], name="x")
	y_ = tf.placeholder(tf.float32, shape=[None, output_num], name="y_")
		#None means the batch can be any size

	#Weights and bias
	W1 = tf.Variable(tf.truncated_normal(shape =[input_num, hidden_num], mean = 0.0, stddev = 0.1), name="W1")
	W2 = tf.Variable(tf.truncated_normal(shape =[hidden_num, output_num], mean = 0.0, stddev = 0.1), name="W2")
	b1 = tf.Variable(tf.truncated_normal(shape =[hidden_num], mean = 0.0, stddev = 0.1), name="b1")
	b2 = tf.Variable(tf.truncated_normal(shape =[output_num], mean = 0.0, stddev = 0.1), name="b2")

	#Feed forward
	h = tf.matmul(x, W1) + b1
	h_prime = tf.nn.relu(h)
	y = tf.add(tf.matmul(h_prime, W2), b2, name="y")

	#Loss (softmax -> cross entropy loss -> average), SGD
	loss = (tf.reduce_mean(
		tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y)) +
			lmbda*tf.nn.l2_loss(W1) +
    		lmbda*tf.nn.l2_loss(b1) +
    		lmbda*tf.nn.l2_loss(W2) +
    		lmbda*tf.nn.l2_loss(b2))

	train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)

	#Accuracy
	correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

	#Tensorboard
	tf.summary.histogram("W1", W1)
	tf.summary.histogram("W2", W2)
	tf.summary.scalar("Loss", loss)
	tf.summary.scalar("Accuracy", accuracy)

	#Saved session
	saver = tf.train.Saver()

	#Start session
	with tf.Session() as sess: 
		#Restore if necessary
		if restore_model:
			saver.restore(sess, "./model/tf_model")
			print "* Model Restored *"

		#Wrtie tensorboard file
		writer = tf.summary.FileWriter("/tmp/vi_asl/{}".format(itr), sess.graph)
		merged = tf.summary.merge_all()

		#Initialize variables
		sess.run(tf.global_variables_initializer())

		#TRAIN
		num_epochs = 10
		epoch_length = 20000
		best_loss = 2

		for i in range(num_epochs):
			print "Epoch {}/{}".format(i + 1, num_epochs)

			for j in range(epoch_length):
				instance, labels = get_batch(train_data)

				#Print at start of epoch
				if j == 0:

					summary, loss_val, acc = sess.run([merged, loss, accuracy], 
						feed_dict={x: instance, y_: labels})
					writer.add_summary(summary, i)

					print "Loss: {}, Acc: {}".format(loss_val, acc)

				train_step.run(feed_dict={x: instance, y_: labels}) #Able to run since session is interactive
				#feed_dict can replace any tensor

			#Save if loss has improved
			if loss_val < best_loss:
				best_loss = loss_val
				saver.save(sess, "./model/tf_model")
				print "* Loss improved - Model Saved *"

		correct, total = 0.0, 0.0
		k = 0
		c, t = [0]*26, [0]*26
		for test_examp in train_data:
			instance, label = np.array([test_examp[0]]), np.array([test_examp[1]])
			out = sess.run([y], feed_dict={x: instance, y_: label})
			
	
			argA, argB = 0, 0
			maxA, maxB = -100000, -100000
	
			for i, val in enumerate(out[0][0]):
				if val > maxA:
					maxA = val
					argA = i
			for j, val in enumerate(label[0]):
				if val > maxB:
					maxB = val
					argB = j

			if argA != argB:
				print "label", label[0], argB
				print "out", out, argA
				c[argB] += 1
				t[argA] += 1
			k += 1

			if argA == argB:
				correct += 1
			total += 1
		print ("Test Accuracy: {} ({}/{})".format((correct / total), correct, total))
		print c
		print t

#tensorboard --logdir /tmp/vi_asl/


if __name__ == "__main__":
	main()
