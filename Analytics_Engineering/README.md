(Q3):
SELECT COUNT(*) FROM fct_monthly_zone_revenue;

Top Green Zone 2020 (Q4):
SELECT zone, SUM(revenue_monthly_total_amount) FROM fct_monthly_zone_revenue WHERE service_type = 'Green' AND EXTRACT(YEAR FROM revenue_month) = 2020 GROUP BY 1 ORDER BY 2 DESC LIMIT 1;

Green Trips Oct 2019 (Q5):
SELECT SUM(total_monthly_trips) FROM fct_monthly_zone_revenue WHERE service_type = 'Green' AND revenue_month = '2019-10-01';