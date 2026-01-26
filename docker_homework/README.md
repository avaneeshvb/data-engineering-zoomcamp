#To start pgadmin and postgres db use the below command: 

docker compose up
-----------------------------------------------------------------

#To build the image of ingest script run the below command:

docker build -t homework_ingest:v001 .
------------------------------------------------------------------
#To run the ingest script and load the data in posgres sql use the below command: 

docker run -it   --network=docker_homework_default   homework_ingest:v001     --pg-user=postgres     --pg-pass=postgres     --pg-host=db     --pg-port=5432     --pg-db=ny_taxi     --green-parquet=green_tripdata_2025-11.parquet     --zones-csv=taxi_zone_lookup.csv     --chunk-green=10000     --chunk-zones=5000
