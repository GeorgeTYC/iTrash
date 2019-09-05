import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

def calcSiftFeature(img):
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#cv2.imshow("gray",gray)
	#cv2.waitKey(2000)
	sift = cv2.xfeatures2d.SIFT_create(200) # max number of SIFT points is 200
	kp, des = sift.detectAndCompute(gray, None)
	return des


def calcFeatVec(features, centers):
	featVec = np.zeros((1, 50))
	for i in range(0, features.shape[0]):
		fi = features[i]
		diffMat = np.tile(fi, (50, 1)) - centers
		sqSum = (diffMat**2).sum(axis=1)
		dist = sqSum**0.5
		sortedIndices = dist.argsort()
		idx = sortedIndices[0] # index of the nearest center
		featVec[0][idx] += 1	
	return featVec


def initFeatureSet(trainset_path):
	file_list = os.listdir(trainset_path)
	for file_name in file_list:
		featureSet = np.float32([]).reshape(0,128)
		print("Extract features from TrainSet " + file_name + ":")
		img_list = os.listdir(trainset_path+"/"+file_name)
		for item in img_list:
			img_name = trainset_path+'\\'+file_name + '\\'+item
			img = cv2.imread(img_name)
			size = img.shape
			height = size[0]
			width = size[1]
			if height > width:
				img = img[int((height-width)/2):int((height+width)/2),0:width]
			else:
				img = img[0:height,int((width-height)/2):int((height+width)/2)]
			
			img = cv2.resize(img,(500,500))
			des = calcSiftFeature(img)
			if des is not None:
				featureSet = np.append(featureSet, des, axis=0)

		featCnt = featureSet.shape[0]
		print(str(featCnt)+" features in "+file_name+" \n")
		if featureSet.shape[0] <= 10:
			continue
		# save featureSet to file
		filename = "temp/features/"+file_name+".npy"
		np.save(filename, featureSet)

def learnVocabulary(trainset_path):
	wordCnt = 50
	file_list = os.listdir(trainset_path)
	for file_name in file_list:
		if file_name == 'empty':
			continue
		filename = "temp/features/"+file_name+".npy"
		features = np.load(filename)

		print("Learn vocabulary of " + file_name + "...")
		# use k-means to cluster a bag of features
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.1)
		compactness, labels, centers = cv2.kmeans(features, K = 50, bestLabels = None, criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.1), attempts = 20, flags = cv2.KMEANS_RANDOM_CENTERS)

		# save vocabulary(a tuple of (labels, centers)) to file
		filename = "temp/vocabulary/"+file_name+".npy"
		np.save(filename, (labels, centers))
		print("Done\n")

def trainClassifier(trainset_path):
	trainData = np.float32([]).reshape(0, 50)
	response = np.int32([])
	
	dictIdx = 0

	file_list = os.listdir(trainset_path)
	
	for file_name in file_list:
		if file_name == 'empty':
			continue
		path_dir = trainset_path+"/"+file_name+"/"
		labels, centers = np.load("temp/vocabulary/" + file_name + ".npy", allow_pickle=True)
		
		print("Init training data of " + file_name + "...")
		img_list = os.listdir(trainset_path+"/"+file_name)
		count = 0
		for item in img_list:
			count += 1
			img_name = os.path.join(trainset_path+'/'+file_name, item)
			img = cv2.imread(img_name)
			size = img.shape
			height = size[0]
			width = size[1]
			if height > width:
				img = img[int((height-width)/2):int((height+width)/2),0:width]
			else:
				img = img[0:height,int((width-height)/2):int((height+width)/2)]
			img = cv2.resize(img,(500,500))
			features = calcSiftFeature(img)
			featVec = calcFeatVec(features, centers)
			trainData = np.append(trainData, featVec, axis=0)

		res = np.repeat([dictIdx], count)
		response = np.append(response, res)
		dictIdx += 1
		print("Done\n")

	print("Now train svm classifier...")
	trainData = np.float32(trainData)
	response = response.reshape(-1, 1)
	svm = cv2.ml.SVM_create()
	svm.setKernel(cv2.ml.SVM_RBF)
	svm.train(trainData,cv2.ml.ROW_SAMPLE, response) # select best params
	svm.save("svm.clf")
	print("Done\n")

def classify(testset_path):
	svm = cv2.ml.SVM_load("svm.clf")

	total = 0; correct = 0; dictIdx = 0
	file_list = os.listdir(testset_path)

	for file_name in file_list:
		count = 0
		crt = 0

		path_dir = testset_path+"/"+file_name+"/"

		labels, centers = np.load("temp/vocabulary/" + file_name + ".npy", allow_pickle=True)
		#print(centers)
		print("Classify on testSet " + file_name + ":")

		img_list = os.listdir(testset_path+"/"+file_name)
		for item in img_list:
			count +=1
			img_name = os.path.join(testset_path+'/'+file_name, item)
			img = cv2.imread(img_name)
			size = img.shape
			height = size[0]
			width = size[1]
			if height > width:
				img = img[int((height-width)/2):int((height+width)/2),0:width]
			else:
				img = img[0:height,int((width-height)/2):int((height+width)/2)]
			img = cv2.resize(img,(500,500))
			
			features = calcSiftFeature(img)
			if features is None:
				continue
			featVec = calcFeatVec(features, centers)
			case = np.float32(featVec)
			if (dictIdx == (svm.predict(case))[1].item()):
				crt += 1
				
		print("Accuracy: " + str(crt) + " / " + str(count) + "\n")
		total += count
		correct += crt
		dictIdx += 1

	print("Total accuracy: " + str(correct) + " / " + str(total))
	return 1

def getLabel(testset_path,img):
	svm = cv2.ml.SVM_load("svm.clf")
	labellist = os.listdir(testset_path)
	img = cv2.imread(img)
	height = img.shape[0]
	width = img.shape[1]
	if height > width:
		img = img[int((height - width) / 2):int((height + width) / 2), 0:width]
	else:
		img = img[0:height, int((width - height) / 2):int((height + width) / 2)]
	img = cv2.resize(img, (500, 500))
	features = calcSiftFeature(img)
	if features is None:
		return None




if __name__ == "__main__":
	trainset_path = "data/resized"
	#testset_path = "data/resized"
	initFeatureSet(trainset_path)
	learnVocabulary(trainset_path)
	trainClassifier(trainset_path)
	# judge = classify(testset_path)
	# if judge == None:
	# 	print("empty")
	# elif judge == 1:
	# 	print("Classification finished")