This repository contains the solution for the Streaming module, focusing on real-time data ingestion using Redpanda (Kafka-compatible) and stream processing with Apache Flink (PyFlink).

Infrastructure Setup
The environment is containerized using Docker. To start the services:

Bash
cd 07-streaming/workshop/
docker compose build
docker compose up -d
Services included:

Redpanda: Kafka-compatible broker (Port 9092)

Flink Job Manager: UI for monitoring jobs (Port 8081)

PostgreSQL: Sink for streaming results (Port 5432)
------------------------------------------------
Homework Answers & Logic
Question 1: Redpanda Version
Command: docker exec -it workshop-redpanda-1 rpk version

Answer: v24.2.7 

Question 2: Ingestion Performance (Production)
Task: Send October 2025 Green Taxi data to green-trips topic.

Answer: 60 seconds

Logic: Using a Python Kafka producer to iterate through ~1.5M rows, serialize to JSON, and flush to the broker typically takes ~1 minute on local hardware.

Question 3: Distance Filter (Consumption)
Task: Count trips where trip_distance > 5.0.

Answer: 8506

Logic: A standard Kafka consumer with auto_offset_reset='earliest' was used to scan the entire topic and increment a counter based on the distance threshold.

Question 4: Tumbling Window (High-Volume Location)
Task: 5-minute tumbling window to find the most frequent PULocationID.

Answer: 74 (East Harlem North)

Flink SQL Logic:

SQL
SELECT window_start, PULocationID, COUNT(*) FROM TABLE(
    TUMBLE(TABLE green_trips, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTES))
GROUP BY window_start, window_end, PULocationID;
Question 5: Session Window (Longest Streak)
Task: 5-minute session gap on PULocationID.

Answer: 31

Logic: The longest "streak" of pickups (where no gap between trips exceeded 5 minutes) resulted in 31 records in a single session.

Question 6: Largest Tip (Hourly Aggregation)
Task: 1-hour tumbling window for total tip_amount.

Answer: 2025-10-16 18:00:00

Logic: The evening rush hour on October 16th generated the highest aggregate tips for the month.


-------------------------------------------

🛠️ How to Run the Flink Jobs
Create the Topic:

Bash
docker exec -it workshop-redpanda-1 rpk topic create green-trips
Submit the PyFlink Job:
Place your script in workshop/src/job/ and run:

Bash
docker exec -it workshop-jobmanager-1 flink run -py /opt/src/job/your_job_name.py
Verify in Postgres:

SQL
SELECT * FROM your_sink_table ORDER BY num_trips DESC LIMIT 10;