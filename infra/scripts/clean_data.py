import findspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import sys

findspark.init()

spark = SparkSession.builder.appName("TransactionAnalytics").getOrCreate()

columns = [
    "transaction_id", "tx_datetime", "customer_id", "terminal_id",
    "tx_amount", "tx_time_seconds", "tx_time_days", "tx_fraud", "tx_fraud_scenario"
]

df = spark.read.option("comment", "#").option("sep", ",").csv("/user/ubuntu/data/").toDF(*columns)

df_cleansed = df.filter(F.col("terminal_id").cast("int").isNotNull()).filter(F.col("customer_id") > 0).drop_duplicates(["transaction_id"])

print(sys.argv[1])

df_cleansed.write.parquet(sys.argv[1], mode="overwrite")
