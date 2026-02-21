-- ================================================================
-- SECTION 1: Environment & Storage Integration Setup
-- ================================================================

-- Create Warehouse and Database Context
CREATE WAREHOUSE IF NOT EXISTS MARKETING_WH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60;
CREATE DATABASE IF NOT EXISTS REVIEW_DB;
CREATE SCHEMA IF NOT EXISTS REVIEW_DB.RAW_DATA;
USE SCHEMA REVIEW_DB.RAW_DATA;

-- Configure Cloud Storage Integration (S3 to Snowflake)
-- Note: Replace Role ARN and Storage Locations with your specific AWS configurations
CREATE OR REPLACE STORAGE INTEGRATION s3_unstructured_int
   TYPE = EXTERNAL_STAGE
   STORAGE_ALLOWED_LOCATIONS = ('s3://your-bucket-name/') 
   STORAGE_PROVIDER = 'S3'
   ENABLED = TRUE
   STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::xxxxxxxxxxxx:role/Snowflake_S3_Role';

-- Verify Integration Configuration
DESC INTEGRATION s3_unstructured_int;

-- Define External Stage for Unstructured Document Files (PDF/DOCX)
CREATE OR REPLACE STAGE review_word_stage
   STORAGE_INTEGRATION = s3_unstructured_int
   URL = 's3://your-bucket-name/'
   DIRECTORY = (ENABLE = TRUE);

-- Synchronize Metadata with S3 Bucket
ALTER STAGE review_word_stage REFRESH;

-- ================================================================
-- SECTION 2: Data Validation & Ingestion Auditing
-- ================================================================

-- Create an Audit Log table to monitor ingestion health and file integrity
CREATE OR REPLACE TABLE data_audit_log AS
SELECT 
    RELATIVE_PATH as file_path,
    SIZE as file_size,
    LAST_MODIFIED,
    CASE 
        -- Validation Logic: Only .docx and .pdf files are supported
        WHEN RELATIVE_PATH NOT LIKE '%.docx' AND RELATIVE_PATH NOT LIKE '%.pdf' 
            THEN 'FAILED: Invalid Format'
        WHEN SIZE = 0 THEN 'FAILED: Empty File'
        ELSE 'SUCCESS'
    END as status
FROM DIRECTORY(@review_word_stage);

-- Review Audit results for Pipeline Health Monitoring
SELECT * FROM data_audit_log ORDER BY status DESC;