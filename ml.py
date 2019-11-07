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
from pyspark.ml.classification import LogisticRegression, OneVsRest, LogisticRegressionModel
from pyspark.ml import Pipeline, PipelineModel
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

class Detector:
    def __init__(self):
        spark = SparkSession\
            .builder\
            .appName("Detecting-Malicious-URL App")\
            .getOrCreate()
        print('Loaded spark...')

        self.model = LogisticRegressionModel.load("model/trained_model")
        self.pipline_fit = PipelineModel.load("model/pipeline")
        print('Loaded model...')

    def predict(self, url):
        df = spark.createDataFrame([(url, 0)], ['url', 'label'])
        predict_input = self.pipline_fit.transform(df)
        predict_result = self.model.transform(predict_input)
        return int(predict_result.collect()[0]['prediction'])