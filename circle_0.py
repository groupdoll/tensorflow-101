import numpy as np
import tensorflow as tf

import data

train_points, train_labels, test_points, test_labels = data.gen_circle_train_test_data(noise=0.)
# data.plot(train_points, train_labels)
# data.plot(test_points, test_labels)
train_labels = train_labels.reshape([-1, 1])
test_labels = test_labels.reshape([-1, 1])


def extract_feature(points):
    x0 = points[:, 0]
    x0x0 = x0 * x0
    x1 = points[:, 1]
    x1x1 = x1 * x1
    features = np.stack((x0x0, x1x1), axis=1)
    return features


train_features = extract_feature(train_points)
test_features = extract_feature(test_points)

X = tf.placeholder(tf.float32, [None, 2])
Y_label = tf.placeholder(tf.float32, [None, 1])

W = tf.Variable(tf.zeros([2, 1]))
B = tf.Variable(tf.zeros([1]))

Y_predict = tf.tanh(X @ W + B)
# Y_predict = tf.tanh(tf.add(tf.matmul(X, W), B))

error = tf.subtract(Y_label, Y_predict)
mse = tf.reduce_mean(tf.square(error))

train = tf.train.GradientDescentOptimizer(0.03).minimize(mse)

# init
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

# train
err, target = 1., 0.000001
epoch, max_epochs = 0, 5000
while err > target and epoch < max_epochs:
    epoch += 1
    err, _ = sess.run([mse, train], feed_dict={X: train_features, Y_label: train_labels})
    if epoch % 100 == 0:
        print('epoch:', epoch, 'mse:', err)
print('epoch:', epoch, 'mse:', err)

# validate
err_test = sess.run([mse], feed_dict={X: test_features, Y_label: test_labels})
print('mse test:', err_test)
