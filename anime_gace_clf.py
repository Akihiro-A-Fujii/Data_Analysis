#coding: utf-8

import cv2
import os
import six
import datetime

import chainer
from chainer import optimizers
from chainer import cuda		# For GPU
import chainer.functions as F
import chainer.links as L
import chainer.serializers as S

import numpy as np


xp = cuda.cupy		## For GPU

class clf_bake(chainer.Chain):
    def __init__(self):

        super(clf_bake, self).__init__(
            conv1 =  F.Convolution2D(3, 16, 5, pad=2),
            conv2 =  F.Convolution2D(16, 32, 5, pad=2),
            l3    =  F.Linear(6272, 256),
            l4    =  F.Linear(256, 10) #10 class classification
        )

    def clear(self):
        self.loss = None
        self.accuracy = None

    def forward(self, X_data, y_data, train=True):
        self.clear() #
        X_data = chainer.Variable(xp.asarray(X_data), volatile=not train)
        y_data = chainer.Variable(xp.asarray(y_data), volatile=not train)
        h = F.max_pooling_2d(F.relu(self.conv1(X_data)), ksize = 5, stride = 2, pad =2)
        h = F.max_pooling_2d(F.relu(self.conv2(h)), ksize = 5, stride = 2, pad =2)
        h = F.dropout(F.relu(self.l3(h)), train=train)
        y = self.l4(h)
        return F.softmax_cross_entropy(y, y_data), F.accuracy(y, y_data)






def getDataSet():
	#Create Data List
	X_train = []
	X_test = []
	y_train = []
	y_test = []
	fleet_dic = {0:'MOBU',1:'FUBUKI',2:'MUTSUKI',3:'KONGO',4:'HIEI',5:'HARUNA',6:'KIRISHIMA', 7:'NAGATO',8:'MUTSU',9:'YUDACHI'}

	for i in range(0,10):
		path = "/home/akihiro/programs/kao-ninshiki/kan-colle/face/50x50_face/" #Directory path
		imgList = os.listdir(path+str(fleet_dic[i]))#Call Charactor key as number
		#Devide data to 4:1( train:test)
		imgNum = len(imgList)
		cutNum = imgNum - imgNum/5
		for j in range(len(imgList)):
			imgSrc = cv2.imread(path+str(fleet_dic[i])+"/"+imgList[j])
			if imgSrc is None:continue

			if j < cutNum:
				X_train.append(imgSrc)
				y_train.append(i)
			else:
				X_test.append(imgSrc)
				y_test.append(i)
	return X_train,y_train,X_test,y_test




def train():
	X_train,y_train,X_test,y_test = getDataSet()
	X_train = xp.array(X_train).astype(xp.float32).reshape((len(X_train),3, 50, 50)) / 255
	y_train = xp.array(y_train).astype(xp.int32)
	X_test = xp.array(X_test).astype(xp.float32).reshape((len(X_test),3, 50, 50)) / 255
	y_test = xp.array(y_test).astype(xp.int32)
	model = clf_bake()
	cuda.get_device(0).use() 	## For GPU
	model.to_gpu()			## For GPU 
	optimizer = optimizers.Adam()
	optimizer.setup(model)

	epochNum = 50
	batchNum = 50
	epoch = 1

	while epoch <= epochNum:
		print("epoch: {}".format(epoch))
		print(datetime.datetime.now())

		trainImgNum = len(y_train)
		testImgNum = len(y_test)

		sumAcr = 0
		sumLoss = 0

		perm = np.random.permutation(trainImgNum)

		for i in six.moves.range(0, trainImgNum, batchNum):
			X_batch = X_train[perm[i:i+batchNum]]
			y_batch = y_train[perm[i:i+batchNum]]

			optimizer.zero_grads()
			loss, acc = model.forward(X_batch, y_batch)
			loss.backward()
			optimizer.update()

			sumLoss += float(loss.data) * len(y_batch)
			sumAcr += float(acc.data) * len(y_batch)
		print('train mean loss={}, accuracy={}'.format(sumLoss / trainImgNum, sumAcr / trainImgNum))

		#---test---
		sumAcr = 0
		sumLoss = 0

		perm = np.random.permutation(testImgNum)

		for i in six.moves.range(0, testImgNum, batchNum):
			X_batch = X_test[perm[i:i+batchNum]]
			y_batch = y_test[perm[i:i+batchNum]]
			loss, acc = model.forward(X_batch, y_batch, train=False)

			sumLoss += float(loss.data) * len(y_batch)
			sumAcr += float(acc.data) * len(y_batch)
		print('test  mean loss={}, accuracy={}'.format(
			sumLoss / testImgNum, sumAcr / testImgNum))
		epoch += 1
		S.save_hdf5('model'+str(epoch+1), model)

train()
