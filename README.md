# ❄️ Snowflake-CortexAI-Marketing-Pipeline

An end-to-end cloud data solution that transforms unstructured customer feedback (PDF/DOCX) into prioritized business strategies using **Snowflake Cortex AI**, **Streamlit**, and **Advanced NLP**.

# 📌 Project Background 

In the modern retail and manufacturing sectors, customer feedback often arrives in unstructured formats like PDF reports or Word documents, creating a "data silo." Traditional sentiment analysis often fails to provide context or prioritize issues based on business impact.

**Snowflake-CortexAI-Marketing-Pipeline** breaks these silos by leveraging LLM-powered document parsing and automated sentiment scoring. This project interprets data through a **Portion-Based Logic** to determine if an issue is an isolated incident or a systemic manufacturing failure.

# 🛠️ Analyzing Tools
- **Data Warehouse & AI Engine**: [Snowflake Data Cloud](https://www.snowflake.com/) (Cortex AI: `PARSE_DOCUMENT`, `SENTIMENT`, `SUMMARIZE`).
- **Backend & Logic**: Python (Snowpark) & SQL.
- **Visualization**: Streamlit & Plotly Express.

# 📊 Exploratory Data Analysis & System Logic

### 1. Interactive Command Center (Global Filter)
The dashboard features a dynamic filtering system that allows users to toggle between a global view or specific product scopes, recalculating all KPIs and insights in real-time.
<br>
<img src="Images/01_dashboard_filter.gif" width="800">
<br>

### 2. Global Performance & Volume Comparison
We analyze the **Average Sentiment by Product** alongside the **Volume of Reviews**. This dual-axis perspective helps stakeholders identify products that may have high sentiment but low sample sizes, or popular products facing quality erosion.
<br>
<img src="images/02_avg_sentiment_bar.jpg" width="800">
<br>
<img src="images/03_review_volume_bar.jpg" width="800">
<br>

### 3. Sentiment Trend & Categorization
- **Stacked Trend Analysis**: Visualizes the evolution of sentiment scores over time, allowing for correlation with specific production dates.
- **Sentiment Categorization**: A professional donut chart displaying the distribution of Positive, Neutral, and Negative labels.
<br>
<img src="images/04_sentiment_trend.jpg" width="800">
<br>
<img src="images/05_sentiment_donut.jpg" width="800">
<br>

### 4. AI-Powered Summarization (Tab 2)
Leveraging Snowflake Cortex, the system automatically generates concise summaries for each review, translating raw feedback into executive-ready bullet points.
<br>
<img src="images/06_ai_summaries.jpg" width="800">
<br>

### 5. Strategic Root Cause Analysis (Tab 3)
This tab uses **Portion-Based Logic** to trigger alerts and **NLP Keyword Extraction** (Document Frequency) to identify specific friction points like `Durability` or `Price`. The **Sentiment Severity Matrix** further maps reviews to pinpoint critical outliers.
<br>
<img src="images/07_strategic_analysis.jpg" width="800">
<br>
<img src="images/08_severity_matrix.jpg" width="800">
<br>

### 6. Pipeline Integrity & Audit Log (Tab 4)
A dedicated monitor for Data Engineering health. It tracks ingestion success rates (formatted to two decimal places) and provides **Exception Tracking** for files that failed the format or size validation.
<br>
<img src="images/09_data_health.jpg" width="800">
<br>
<br>
<img src="images/10_exception_tracking.jpg" width="800">
<br>

### 7. Granular Raw Data (Tab 5)
Provides full transparency by allowing users to drill down into the processed tabular data for manual verification or export.
<br>
<img src="images/11_raw_data.gif" width="800">
<br>

# 📂 Repository Structure
- `app.py`: Main Streamlit application.
- `sql/`: Snowflake configuration for Stages and Cortex functions.
- `images/`: Dashboard screenshots for documentation.

---
<i>Developed by **SungChian Wen** | MSBA at University of California, Irvine.</i>
