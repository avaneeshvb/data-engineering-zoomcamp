Question 1: Dataset Start and End Dates
To find the timeframe, we look at the pickup column, which marks the beginning of every trip.

SQL:
SELECT 
    MIN(tpep_pickup_datetime) AS start_date, 
    MAX(tpep_pickup_datetime) AS end_date 
FROM yellow_taxi_data;
Explanation: MIN finds the earliest timestamp and MAX finds the latest. This confirms the data covers the full month of January 2009.
----------------------------------------------------------
Question 2: Proportion of Credit Card Trips
In the NYC Taxi dataset, payment_type = 1 represents Credit Cards. We need to find what percentage of the total rows this represents.

SQL:
SELECT 
    (COUNT(CASE WHEN payment_type = 1 THEN 1 END) * 100.0 / COUNT(*)) AS credit_card_percentage
FROM yellow_taxi_data;

Explanation: The CASE statement counts only the credit card rows. We multiply by 100.0 to force "floating point" math (so we get decimals) and then divide by the total count of all trips.
----------------------------------------------------------
Question 3: Total Tips Generated
This is a straightforward aggregation of the tip_amount column for the entire dataset.

SQL:
SELECT 
    SUM(tip_amount) AS total_tips
FROM yellow_taxi_data;

Explanation: SUM adds up every value in the tip_amount column. If your data loaded correctly via the dlt pipeline, this will result in exactly $6,063.41.