# NHANES BigQuery Data

The US [National Health and Nutrition Examination Survey](https://www.cdc.gov/nchs/nhanes/index.htm) (NHANES) is a wonderful source of data to understand American health and diet.  The default tooling for the data provided by NCHS is SAS.  Working with the data in Google BigQuery allows for an effective processing and joining against other large datasets.

Documentation on various table contents and data fields is available at the [NHANES Documentation](https://wwwn.cdc.gov/nchs/nhanes/Default.aspx)

## Instructions

Public BigQuery datasets are available under project-id: `nhanes-277516`

To browse the tables, goto the [BigQuery console](https://console.cloud.google.com/bigquery) and add select "+ ADD DATA" then select "Pin a project" and type in `nhanes-277516`.  You will then see the nhanes project in your tree list and you can expand it to see various datasets and tables.

NHANES_2015_2016 is the most complete dataset so far.

## Sample Query

Sample Query to answer the question "What is the average Systolic Blood Pressure for people with various amounts of educaiton?"

    SELECT DMDEDUC2, AVG(BPXSY1) as AvgSystolic, COUNT(*) as CNT
    FROM `nhanes-277516.NHANES_2015_2016.DEMO_I`
    INNER JOIN `nhanes-277516.NHANES_2015_2016.BPX_I` USING(SEQN)
    GROUP BY DMDEDUC2
    ORDER BY DMDEDUC2 DESC

Row | DMDEDUC2 | AvgSystolic | CNT |
| ---- | -------- | ----------- | --- |
1 | 9.0 | 124.0 | 3 |
2 | 5.0 | 122.12078431372545 | 1366
3 |4.0 |124.76872536136676 |1621
4 |3.0 |126.74113475177322 | 1186
5 | 2.0 | 128.3743842364532 | 643
6 | 1.0 |130.78896103896105 |655
7 |null |107.22227797290526 |4070


# Querying across years.

While the NHANES has morphed over the years in the data that is collected, much is the same and can be queried across years.  Here is an example of the above query across 4 years.

    SELECT * FROM (
        SELECT DMDEDUC2, AVG(BPXSY1) as AvgSystolic, COUNT(*) as CNT
        FROM (
            SELECT SEQN, DMDEDUC2 FROM `nhanes-277516.NHANES_2013_2014.DEMO`
            UNION ALL
            SELECT SEQN, DMDEDUC2 FROM `nhanes-277516.NHANES_2015_2016.DEMO`)
        AS BIGDEMO
        INNER JOIN (
            SELECT SEQN, BPXSY1 FROM `nhanes-277516.NHANES_2013_2014.BPX`
            UNION ALL
            SELECT SEQN, BPXSY1 FROM `nhanes-277516.NHANES_2015_2016.BPX`)
        AS BPX
        ON(BIGDEMO.SEQN = BPX.SEQN)
        GROUP BY DMDEDUC2
        ORDER BY DMDEDUC2 DESC
    )
    WHERE CNT > 100 AND DMDEDUC2 IS NOT NULL;
Areas that could use improvement:
* SEQN is represented as a float when it should be an int.
* Coded enums should use more human readable versions (see DMDEDUC2 in the example above)
* Flush out more of past year's data tables.


This uses the python xport library for reading and converting SAS files provided by CDC.  Some things get lost in translation of the schema.



