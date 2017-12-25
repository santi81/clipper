from __future__ import absolute_import, print_function
import os
import sys
import requests
import json
import numpy as np
import time
import logging

cur_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.abspath('%s/util_direct_import/' % cur_dir))
from util_package import mock_module_in_package as mmip
import mock_module as mm

from pyspark.ml.linalg import Vectors
from pyspark.sql import SparkSession, Row
from pyspark.ml.classification import LogisticRegression
from clipper_admin import ClipperConnection, DockerContainerManager


cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath("%s/../clipper_admin" % cur_dir))
from clipper_admin.deployers.gRPCpyspark import deploy_pyspark_model

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%y-%m-%d:%H:%M:%S',
    level=logging.INFO)

logger = logging.getLogger(__name__)

app_name = "pyspark-sparkml-test"
model_name = "pyspark-sparkml-model"


def normalize(x):
    return x.astype(np.double) / 255.0


def objective(y, pos_label):
    # prediction objective
    if y == pos_label:
        return 1
    else:
        return 0


def parseData(line, obj, pos_label):
    fields = line.strip().split(',')
    return (obj(int(fields[0]), pos_label),
            Vectors.dense(normalize(np.array(fields[1:]))))


def predict(spark, model, xs):
    df = spark.sparkContext.parallelize(
        [Row(features=Vectors.dense(x)) for x in xs]).toDF()
    result = model.transform(df).select('prediction').collect()
    return ([str(x[0]) for x in result])


def train_logistic_regression(trainDF):
    mlr = LogisticRegression(maxIter=100, regParam=0.03)
    mlrModel = mlr.fit(trainDF)
    return mlrModel


def deploy_model(sc,
                clipper_conn,
                model,
                version,
                link_model=False,
                predict_fn=predict):
    deploy_pyspark_model(clipper_conn, model_name, version, "integers",
                         predict_fn, model, sc)


def get_test_point():
    return [np.random.randint(255) for _ in range(784)]


if __name__ == "__main__":
    pos_label = 3
    try:
        spark = SparkSession\
                .builder\
                .appName("clipper-pyspark-ml")\
                .getOrCreate()
        sc = spark.sparkContext
        args = {"ports": {"7000/tcp": 7000}}
        clipper_conn = ClipperConnection(DockerContainerManager(
            extra_container_kwargs=args
        ))
        train_path = os.path.join(cur_dir, "data/train.data")
        trainRDD = spark.sparkContext.textFile(train_path).map(
            lambda line: parseData(line, objective, pos_label)).cache()
        trainDf = spark.createDataFrame(trainRDD, ["label", "features"])
        version = 1
        lr_model = train_logistic_regression(trainDf)
        deploy_model(
                sc, clipper_conn, lr_model, version, link_model=True)
    except Exception as e:
        logger.exception("Exception")
        sys.exit(1)
