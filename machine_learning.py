

import findspark

from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics
from furniture import *
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.conf import SparkConf
from pyspark import SparkContext
from datetime import datetime

from pyspark.sql import Row
import os
java8_location= '/usr/lib/jvm/java-8-openjdk-amd64' 
os.environ['JAVA_HOME'] = java8_location
import glob
from functools import reduce
from datetime import datetime
import sys
import json
import re
        
import pandas  as pd

def loadcols(dataset):
    col=[]
    for x in dataset.columns:
        if x == 'URL' or x == 'Malicious' or x == 'features' or x == 'label'or x == '_c0':
	        continue
        col.append(x)
    return col

class Detector:
    spark = SparkSession.builder.master("local[*]").appName("MalwareDetector").config("spark.driver.memory", "8g").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    sc = spark.sparkContext
    def __init__(self, modelpath="model"):
        self.datapath = datapath

        self.modelpath = modelpath
        modelfile = os.path.join(self.modelpath, "detector")
        if (os.path.exists(modelfile)):
            print("Load model from: ", self.modelpath)
            self.model = PipelineModel.load(modelfile)
        else:
            print("Model not found.")
                
    def loadDataset(self, datapath):
        data = []
        
        
        if ".csv" in datapath:
            dataset = self.spark.read.csv(datapath, header=True, inferSchema=True)
            cols =loadcols(dataset)
	
        assembler = VectorAssembler(inputCols=cols, outputCol="features")
        dataset = assembler.transform(dataset.fillna(0))
        dataset = dataset.withColumn("label", dataset['Malicious'])
        return dataset
    
    def trainModel(self, trainingData):
        """ Ham huan luyen du lieu
        Mac dinh training toan bo du lieu trong dataset splitratio 100% training, 0% testing
        """
        labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(trainingData)
        featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures",maxCategories=4).fit(trainingData)
        rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol= "indexedFeatures", numTrees=30,maxDepth=5, maxBins=32, seed=None,impurity="gini")
        labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=labelIndexer.labels)
        pipeline = Pipeline(stages=[labelIndexer, featureIndexer, rf, labelConverter])
        model = pipeline.fit(trainingData)
        model.write().overwrite().save(os.path.join(self.modelpath, "detector"))
        return model
    
    def evaluate(self, model=None, trainingData=None, testingData=None):
        """ Ham kiem thu model, in ra man hinh do do chinh xac va thoi gian tinh toan
        """
        time_train = 0
        time_test = 0
        
        if (not trainingData):
            trainingData = self.trainingData
        if (not testingData):
            testingData = self.testingData
            
        if (not model):
            
            print("Training...")
            start_train = datetime.now()
            model = self.trainModel(trainingData)
            time_train = datetime.now() - start_train
        
        
        
        print("Testing...")
        start_test = datetime.now()
        predictions = model.transform(testingData)
        time_test = datetime.now() - start_test

        
        print("{:*^100}".format(""))
        print("Training time: ", time_train)
        print("Testing time: ", time_test)
        
        featureImportances = {}
        fi = model.stages[2].featureImportances
        features = loadcols(self.dataset)
        index = 0
        for value in fi:
            featureImportances[features[index]] = value
            index = index + 1
        fiSorted = sorted(featureImportances.items(), key=lambda x: x[1], reverse=True)
        print("{:*^100}".format(" Feature Importances "))
        f = open("features_importance.txt", "w")
        for feature in fiSorted:
            if feature[1] > 0.000:
                print("{!s} : {:.4%}".format(feature[0].strip(), feature[1]))
            f.write("{!s}\n".format(feature[0].strip()))
        f.close()
        
        print("{:*^100}".format(" Evaluate for Flow "))
        
        print("Total predictions:", predictions.count())
        predictions.select("prediction", "indexedLabel", "label").groupBy("label").count().show()
        
        predictionAndLabels = predictions.select("prediction", "indexedLabel").rdd
        metrics = MulticlassMetrics(predictionAndLabels)

        print("Confusion Matrix:")
        for line in metrics.confusionMatrix().toArray():
            print(line)
        
        print("TPR: {:.3%} \tFPR: {:.3%}".format(metrics.truePositiveRate(1.0), metrics.falsePositiveRate(1.0)))
        print("TNR: {:.3%} \tFNR: {:.3%}".format(metrics.truePositiveRate(0.0), metrics.falsePositiveRate(0.0)))

        print("Precision: {:.3%} \tRecall: {:.3%} \tAccuracy: {:.3%}".format(metrics.precision(1.0), metrics.recall(1.0), metrics.accuracy))
        
        print(metrics.accuracy)

        print("{:*^100}".format(""))
        
    
    def predict(self, datapath="data/dataset.csv"):
        furniture=feature_extract(url,0)
        if furniture ==-1 :
			print("url is die")
			return -1

        filename="data/predictions.csv"
        df= pd.DataFrame(furniture)
        df.to_csv(filename,index='false')

        self.predictingData = self.loadDataset(filename)
        self.predictingData = self.predictingData.repartition(300).cache()
        predictions = self.model.transform(self.predictingData)
        df= predictions.select('prediction').collect()
        return df[0].asDict()["prediction"]
	
def detect(md,url):	
	if md==0 :
		detector = Detector(mode=md)
		detector.evaluate()
	elif md ==1 :
		if not re.search('^http',url):
			if scanport(url)==-1:
			    url ='http://'+url
			else :
			    url =scanport(url)
		furniture=feature_extract(url,0)
		if furniture ==-1 :
			print("url is die")
			return -1
		else:
			filename="data/predictions.csv"
			df= pd.DataFrame(furniture)
			df.to_csv(filename,index='false')
			detector = Detector(mode=md,datapath=filename)
			return detector.predict()
	else:
        print("you input wrong ")
        return -2


if __name__ == "__main__":
    detector = Detector()
    res = detector.predict("https://www.facebook.com")
    print(res)

		



