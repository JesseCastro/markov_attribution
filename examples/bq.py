from markov_attribution import MarkovAttribution
import pandas as pd
from pandas.io import gbq
import pandas as pd
from pandas.io import gbq
from pprint import pprint

project_id = 'big-query-144615'

top10_active_users_query = """
    SELECT
      SUM(IF(NUM >= 1,1,0)) AS conversions,
      SUM(AMOUNT) AS value,
      SUBSTR(CAMPAIGN_CHAIN,0,INSTR(CAMPAIGN_CHAIN, '::')-1) AS path,
    FROM [rax_staging.RAX_XP_STUDY_43]
    WHERE 1 = 1
    AND CONCAT(
          STRING(YEAR(TIMESTAMP(CLOSE_DATE))),
          'Q',
          CASE
            WHEN MONTH(TIMESTAMP(CLOSE_DATE)) <= 3 THEN '1'
            WHEN MONTH(TIMESTAMP(CLOSE_DATE)) >= 4 AND MONTH(TIMESTAMP(CLOSE_DATE)) <= 6 THEN '2'
            WHEN MONTH(TIMESTAMP(CLOSE_DATE)) >= 7 AND MONTH(TIMESTAMP(CLOSE_DATE)) <= 9 THEN '3'
            WHEN MONTH(TIMESTAMP(CLOSE_DATE)) >= 10 THEN '4'
          END

        )  = '2018Q1'
    AND TYPE IN ('NONE','OPPS')
    GROUP BY path, FOCUS_AREA
"""


try:
    conversionsdf = gbq.read_gbq(top10_active_users_query, project_id=project_id)
except err:
    print('Error reading the dataset')
    pprint(err)
    sys.exit()

test_data = conversionsdf.to_dict('records')
sep = ' > '
marka = MarkovAttribution(test_data, sep)
pprint(marka.get_removal('DisplayImpression'))
pprint(marka.get_channel_probabilities())
