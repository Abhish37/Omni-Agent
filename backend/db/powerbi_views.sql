-- Power BI Views for Omni-Agent Dashboard

-- 1. High-Level Executive Summary View
CREATE OR REPLACE VIEW v_executive_summary AS
SELECT 
    DATE(date) as transaction_date,
    COUNT(*) as total_transactions,
    SUM(amount) as total_volume,
    SUM(CASE WHEN is_anomaly = true THEN 1 ELSE 0 END) as flagged_anomalies_count,
    SUM(CASE WHEN is_anomaly = true THEN amount ELSE 0 END) as flagged_anomalies_volume
FROM transactions
GROUP BY DATE(date);

-- 2. Vendor Risk Analysis View
CREATE OR REPLACE VIEW v_vendor_risk AS
SELECT 
    vendor,
    COUNT(*) as total_documents,
    SUM(amount) as total_spent,
    AVG(anomaly_score) as avg_risk_score,
    SUM(CASE WHEN is_anomaly = true THEN 1 ELSE 0 END) as flagged_count
FROM transactions
GROUP BY vendor
ORDER BY avg_risk_score DESC;

-- Power BI Instructions:
-- 1. Open Power BI Desktop.
-- 2. Select 'Get Data' -> 'PostgreSQL database'.
-- 3. Enter Server: localhost, Database: omni_agent.
-- 4. In the Navigator, select the views 'v_executive_summary' and 'v_vendor_risk'.
-- 5. Build dashboard visuals directly against these pre-aggregated views to ensure real-time performance.
