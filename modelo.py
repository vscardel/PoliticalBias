import tensorflow as tf
import numpy as np

tam_vetor_treino = 63850
num_iteracoes_treino = 10000
batch_size = 32
lr = 0.001
valor_alfa = 0.4

treino = np.load('base_processada/base_treino.npy')
labels = np.load('base_processada/base_labels_treino.npy')
validacao = np.load('base_processada/base_validacao.npy')
labels_validacao = np.load('base_processada/base_labels_validacao.npy')
teste = np.load('base_processada/base_teste.npy')

graph = tf.Graph()
with graph.as_default():
	vetores_treino = tf.compat.v1.placeholder(tf.float32, shape = (None,tam_vetor_treino))
	labels_treino = tf.compat.v1.placeholder(tf.int64, shape=(None,))
	learning_rate = tf.compat.v1.placeholder(tf.float32)
	training = tf.compat.v1.placeholder(tf.bool)
	alfa = tf.compat.v1.placeholder(tf.float32)

	vetores_treino_flatten = tf.reshape(vetores_treino,[-1,vetores_treino.shape[1]])

	#encoder
	e1 = tf.compat.v1.layers.dense(vetores_treino_flatten, 1024, activation=tf.nn.relu, name='e1')
	e2 = tf.compat.v1.layers.dense(e1, 512, activation=tf.nn.relu, name='e2')
	e3 = tf.compat.v1.layers.dense(e2, 256, activation=tf.nn.relu, name='e3')
	e4 = tf.compat.v1.layers.dense(e3, 128, activation=tf.nn.relu, name='e4')

	#classifier
	# c1 = tf.compat.v1.layers.dense(e4, 1024, activation=tf.nn.relu, name='c1')
	c1 = tf.compat.v1.layers.dense(vetores_treino_flatten, 1024, activation=tf.nn.relu, name='c1')
	c1 = tf.compat.v1.layers.dropout(c1,0.5, training = training)
	c2 = tf.compat.v1.layers.dense(c1, 64, activation=tf.nn.relu, name='c2')
	c2 = tf.compat.v1.layers.dropout(c2,0.2, training = training)
	
	output_classifier = tf.compat.v1.layers.dense(c2, 2, name='output_classifier')

	#decoder
	d1 = tf.compat.v1.layers.dense(e4,256, activation=tf.nn.relu, name='d1')
	d2 = tf.compat.v1.layers.dense(d1,512, activation=tf.nn.relu, name='d2')
	d3 = tf.compat.v1.layers.dense(d2,1024, activation=tf.nn.relu, name='d3')
	d4 = tf.compat.v1.layers.dense(d3,tam_vetor_treino, activation=tf.nn.relu, name='d4')

	#loss = tf.compat.v1.nn.sparse_softmax_cross_entropy_with_logits(labels=labels_treino, logits=output_classifier)
	loss_classifier = tf.compat.v1.nn.sparse_softmax_cross_entropy_with_logits(labels=labels_treino, logits=output_classifier)
	loss_encoder_decoder = (d4 - vetores_treino_flatten) ** 2
	loss = (1-alfa)*tf.reduce_sum(loss_classifier) + alfa*tf.reduce_sum(loss_encoder_decoder)

	train_op = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

	correct = tf.reduce_sum(tf.cast(tf.equal(tf.argmax(output_classifier, axis=1), labels_treino), dtype=tf.float32))

	saver = tf.compat.v1.train.Saver()

	print(correct)

def accuracy(session, Xi, yi):
	batch_size = 32
	cont = 0
	for i in range(0, len(Xi), batch_size):
		X_batch = Xi[i:i+batch_size]
		y_batch = yi[i:i+batch_size]
		ret = session.run([correct], feed_dict = {vetores_treino : X_batch, labels_treino : y_batch, training : False})
		cont += ret[0]
	return 100.0*cont/len(Xi)


maior_acc = 0.0

with tf.compat.v1.Session(graph = graph) as session:

	session.run(tf.compat.v1.global_variables_initializer())

	for i in range(num_iteracoes_treino):

		indexes = np.random.permutation(len(treino))[:batch_size]
		batch_reportagem = np.take(treino, indexes, axis=0)
		labels_batch = np.take(labels, indexes, axis=0)

		ret = session.run([train_op], feed_dict = {vetores_treino : batch_reportagem, 
												   labels_treino : labels_batch, 
												   learning_rate : lr,
												   alfa: valor_alfa,
												   training: True})

		acc_atual = accuracy(session, validacao, labels_validacao)

		if i % 10 == 9:

			if acc_atual > maior_acc:
				print('salvando modelo com maior acuracia ate o momento')
				print()
				saver.save(session, 'modelo/my-model')
				maior_acc = acc_atual

			print("Iteration #%d" % (i))
			print("TRAIN: ACC=%.5f" % (accuracy(session, treino, labels)))
			print("VAL: ACC=%.5f\n" % (acc_atual))