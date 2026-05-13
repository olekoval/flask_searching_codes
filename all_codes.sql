WITH ehealth AS (
SELECT 
    v.code, 
    v.description, 
    CASE 
        WHEN d.kwd_name = 'eHealth/ICD10_AM/condition_codes' THEN 'ICD10'
        ELSE'LOINC'
    END AS record_type
FROM core.dim_rpt_dictionary_values AS v
INNER JOIN core.dim_rpt_dictionaries AS d 
    ON v.dictionary_id = d.id
WHERE v.is_current = 'Y' 
  AND d.is_current = 'Y'
  AND d.kwd_name IN ('eHealth/ICD10_AM/condition_codes', 
                     'eHealth/LOINC/observation_codes')
),
actions AS (
SELECT
       code,
       kwd_name AS description,
	   'ACTION' AS record_type 
  FROM core.dim_rpt_services
 WHERE is_current = 'Y' 
   AND is_active
)

SELECT *
  FROM ehealth  
UNION ALL
SELECT *
  FROM actions




  