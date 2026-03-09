Data Engineering Zoomcamp 2025 - Module 5 (Batch Processing) homework.

Data Engineering Zoomcamp 2025: Spark Homework (Module 5)
This repository contains the solutions and SQL/PySpark logic for the Module 5 homework, focusing on batch processing using Apache Spark and the November 2024 Yellow Taxi dataset.

Dataset Information
Main Data: Yellow Taxi Trip Records (November 2024)

Lookup Data: Taxi Zone Lookup CSV

Format: Parquet and CSV

Homework Answers
Question 1: Install Spark and PySpark
Task: Execute spark.version in a local session.

Answer: 3.5.0 

Question 2: Yellow November 2024 Partition Size
Task: Repartition the November 2024 Yellow Taxi data into 4 partitions and save as Parquet.

Answer: 25MB

Logic: The total dataset size (~100MB) divided by 4 partitions results in files roughly 25MB each due to Snappy compression.

Question 3: Count Records (Nov 15th)
Task: How many taxi trips started on the 15th of November?

Answer: 162,604

Query: ```python
df.filter(F.to_date(df.tpep_pickup_datetime) == "2024-11-15").count()


Question 4: Longest Trip
Task: What is the length of the longest trip in the dataset in hours?

Answer: 134.5

Query:

Python
df.withColumn('duration', (F.unix_timestamp('tpep_dropoff_datetime') - F.unix_timestamp('tpep_pickup_datetime')) / 3600) \
  .select(F.max('duration')).show()
Question 5: User Interface
Task: Which local port does the Spark UI dashboard run on?

Answer: 4040

Question 6: Least Frequent Pickup Location Zone
Task: Find the zone with the fewest pickups using a join with the zone lookup data.

Answer: Governor's Island/Ellis Island/Liberty Island

🛠️ Implementation Details
Environment Setup
To reproduce these results, initialize your Spark session as follows:

Python
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("homework_m5") \
    .getOrCreate()
The Join Logic (Q6)
To find the least frequent zone, we performed an inner join between the Fact table (Yellow Taxi) and the Dimension table (Zones):

Python
df_zones = spark.read.option("header", "true").csv('taxi_zone_lookup.csv')
df_result = df_yellow.join(df_zones, df_yellow.PULocationID == df_zones.LocationID) \
    .groupBy("Zone") \
    .count() \
    .orderBy("count", ascending=True)