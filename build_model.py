from pyspark.ml.feature import Tokenizer, RegexTokenizer
from pyspark.ml.classification import LinearSVC
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType
from pyspark.ml.feature import NGram,HashingTF, IDF
from pyspark.ml.feature import StandardScaler
from pyspark.sql.functions import lit
from pyspark.mllib.feature import StandardScaler, StandardScalerModel
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.util import MLUtils
from pyspark.ml.classification import LogisticRegression, OneVsRest
from pyspark.ml import Pipeline
from pyspark.sql import Row
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import Word2Vec
from sklearn.metrics import confusion_matrix
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.ml.classification import NaiveBayes
from pyspark import SparkContext
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.conf import SparkConf

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("Detecting-Malicious-URL App")\
        .getOrCreate()

    data_df = spark.read.csv(path='model/dataset.csv',
        sep=',',
        encoding='UTF-8',
        comment=None,
        header=True, 
        inferSchema=True
    )

    malicious = data_df.filter("label = 1")
    bening = data_df.filter("label = 0")

    sampleRatio = malicious.count() / data_df.count()
    sample_bening = bening.sample(False, sampleRatio)

    sampled = malicious.unionAll(sample_bening)


    #Tokennize the TrainData - sparse the URL string into words
    regexTokenizer = RegexTokenizer(inputCol="url", outputCol="Words", pattern="\\W")

    #CountVectorizer converts the the words into feature vectors - Thi is used as it gives better results
    countVectors = CountVectorizer(inputCol=regexTokenizer.getOutputCol(), outputCol="rawfeatures", vocabSize=10000, minDF=5)

    #
    idf = IDF(inputCol=countVectors.getOutputCol(), outputCol="features") 

    #create the pipline 
    pipeline = Pipeline(stages=[regexTokenizer, countVectors, idf ])

    # Fit the pipeline to training documents.
    # Pass 'sampled' in the param to set Balanced datasets
    pipelineFit = pipeline.fit(sampled)

    dataset = pipelineFit.transform(sampled)

    lr = LogisticRegression(maxIter=10000, regParam=0.3, elasticNetParam=0, family = "binomial")
    # Train model using logisitic regression
    lrModel = lr.fit(dataset)

    lrModel.save("mode/trained_model")

    print("Done job")

