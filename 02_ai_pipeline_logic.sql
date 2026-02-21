-- ================================================================
-- SECTION 3: Unstructured Data Parsing with Snowflake Cortex
-- ================================================================

-- Step 1: Use Cortex PARSE_DOCUMENT to extract raw text and layout from binary files
CREATE OR REPLACE TEMPORARY TABLE files_temp AS
SELECT 
    REPLACE(REGEXP_SUBSTR(RELATIVE_PATH, '[^/]+$'), '%2e', '.') as filename,
    SNOWFLAKE.CORTEX.PARSE_DOCUMENT(
        @review_word_stage, 
        RELATIVE_PATH, 
        {'mode': 'layout'}
    ):content::STRING AS raw_layout
FROM DIRECTORY(@review_word_stage)
WHERE RELATIVE_PATH LIKE '%.docx' OR RELATIVE_PATH LIKE '%.pdf';

-- ================================================================
-- SECTION 4: Feature Extraction & AI Analysis Pipeline
-- ================================================================

-- Step 2: Extract structured fields using Regex and apply Cortex AI functions
CREATE OR REPLACE TABLE final_product_reviews AS
WITH extracted_data AS (
    SELECT 
        filename,
        -- Extract metadata using regular expressions from unstructured text
        REGEXP_SUBSTR(raw_layout, 'Product: (.*?)\n', 1, 1, 'e') as product,
        REGEXP_SUBSTR(raw_layout, 'Date: (202[0-9]-[0-9]{2}-[0-9]{2})', 1, 1, 'e') as date,
        -- Capture the core review content following the header
        REGEXP_SUBSTR(raw_layout, '## Customer Review[\\s\\n]+([\\s\\S]*?)$', 1, 1, 'es') as customer_review
    FROM files_temp
)
SELECT 
    filename,
    product,
    date,
    -- 1. Translate multi-language reviews to English for standardized processing
    SNOWFLAKE.CORTEX.TRANSLATE(customer_review, 'auto', 'en') as translated_review,
    -- 2. Generate AI-powered executive summaries
    SNOWFLAKE.CORTEX.SUMMARIZE(translated_review) as summary,
    -- 3. Calculate sentiment polarity score (-1.0 to 1.0)
    SNOWFLAKE.CORTEX.SENTIMENT(translated_review) as sentiment_score,
    -- 4. Categorize sentiment based on enterprise-standard thresholds
    CASE 
        WHEN sentiment_score > 0.5 THEN 'Positive'
        WHEN sentiment_score < -0.3 THEN 'Negative'
        ELSE 'Neutral' 
    END as sentiment_label
FROM extracted_data;

-- Final Verification of Structured AI Insights
SELECT * FROM final_product_reviews;