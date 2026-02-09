-- Creating the External Table
CREATE OR REPLACE EXTERNAL TABLE `your_project.your_dataset.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your_bucket_name/yellow_tripdata_2024-*.parquet']
);

-- Creating the Native (Regular) Table
CREATE OR REPLACE TABLE `your_project.your_dataset.yellow_tripdata_non_partitioned` AS
SELECT * FROM `your_project.your_dataset.external_yellow_tripdata`;


Answers:

Question 1:
SELECT COUNT(*) 
FROM `your_project.your_dataset.yellow_tripdata_non_partitioned`;

Question 2:
SELECT COUNT(DISTINCT(PULocationID)) 
FROM `your_project.your_dataset.external_yellow_tripdata`;

SELECT COUNT(DISTINCT(PULocationID)) 
FROM `your_project.your_dataset.yellow_tripdata_non_partitioned`;


Question 3:
One Column: Scans only the data for PULocationID (155 MB).

Two Columns: Scans the data for PULocationID AND DOLocationID (310 MB).

Conclusion: To save costs in BigQuery, never use SELECT *. Only select the columns you actually need.

Question 4:
SELECT COUNT(*)
FROM `your_project.your_dataset.yellow_tripdata_non_partitioned`
WHERE fare_amount = 0;


Question 5:
CREATE OR REPLACE TABLE `your_project.your_dataset.yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `your_project.your_dataset.external_yellow_tripdata`;


Question 6:

SELECT DISTINCT VendorID
FROM `your_project.your_dataset.yellow_tripdata_non_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

SELECT DISTINCT VendorID
FROM `your_project.your_dataset.yellow_tripdata_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

The massive drop in data processed (from 310 MB to 27 MB) is the reason why partitioning is critical for production environments. 
It directly impacts cost and speed

Question 7:
The external table was created using the uris parameter pointing to gs://your-bucket-name/*.parquet. Therefore, the data remains in Google Cloud Storage (GCS), and BigQuery acts as a compute engine to query those files directly.

Question 8:
False. While clustering improves performance for large datasets by organizing data based on specific columns, it is not recommended for small tables (typically < 1 GB) or when query patterns do not frequently use the clustered columns for filtering or aggregation.

Question 9:
A SELECT count(*) query on a native table estimates 0 bytes because BigQuery retrieves the row count directly from the table's metadata rather than scanning the actual data files.