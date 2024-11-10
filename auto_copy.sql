COPY bq2_data.joined_flights_full_weather
FROM 's3://airline-is459/data-source/for_autocopy/'
IAM_ROLE 'arn:aws:iam::820242926303:role/service-role/AmazonRedshift-CommandsAccessRole-20241017T010122'
FORMAT AS CSV
IGNOREHEADER 1
DELIMITER ','
JOB CREATE joined_table_job
AUTO ON;
