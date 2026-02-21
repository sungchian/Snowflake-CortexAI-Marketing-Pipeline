# ❄️ Snow-Insight: Enterprise AI Product Intelligence Pipeline

An end-to-end cloud data solution that transforms unstructured customer feedback (PDF/DOCX) into prioritized business strategies using **Snowflake Cortex AI**, **Streamlit**, and **Advanced NLP**.

# 📌 Project Background 

In the modern retail and manufacturing sectors, customer feedback often arrives in unstructured formats like PDF reports or Word documents, creating a "data silo" where valuable insights are trapped. Traditional sentiment analysis often fails to provide context or prioritize issues based on business impact.

**Snow-Insight** breaks these silos by leveraging LLM-powered document parsing and automated sentiment scoring. This project doesn't just show "positive" or "negative" scores—it interprets the data through a **Portion-Based Logic** to determine if an issue is an isolated incident or a systemic manufacturing failure.

Our project questions include:
- **How can we extract high-quality text from unstructured binary files (PDF/DOCX) without manual entry?**
- **What is the real-time "Dissatisfaction Portion" for each product line?**
- **Which specific product attributes (e.g., Durability, Sizing) are driving negative sentiment?**
- **How do we ensure 100% data integrity from S3 ingestion to the final dashboard?**

# 🛠️ Analyzing Tools

- **Data Warehouse & AI Engine**: [Snowflake Data Cloud](https://www.snowflake.com/). We utilized **Snowflake Cortex AI** (`PARSE_DOCUMENT`, `SENTIMENT`, `SUMMARIZE`) to handle the heavy lifting of unstructured data processing.
- **Backend Framework**: **Python (Snowpark)** was used to bridge the gap between Snowflake’s data processing and the frontend application.
- **Visualization & Frontend**:
    - **Streamlit**: For building the enterprise-grade interactive dashboard.
    - **Plotly Express**: To create reactive charts with professional-grade formatting (e.g., precise percentage labels to two decimal places).
- **Data Governance**: **SQL** for building a real-time Audit Log system to monitor pipeline health and file ingestion status.

# 📊 Exploratory Data Analysis & System Logic

- **1. Global Product Performance Comparison**
  We analyze the average sentiment and review volume across all product categories. This high-level view allows executives to identify which products are thriving and which require immediate attention.
  <br>
  <img src="images/analytics_kpi.jpg" width="800">
  <br>

- **2. Sentiment Trend Analytics (Stacked)**
  By visualizing sentiment scores over time in a stacked bar format, we can pinpoint specific dates where negative feedback surged, enabling us to trace issues back to specific manufacturing dates or batches.
  <br>
  <img src="images/sentiment_trend.jpg" width="800">
  <br>

- **3. Strategic Insights: Portion-Based Decision Logic**
  The dashboard automatically categorizes the "Negative Portion" to trigger different levels of business response. If the portion exceeds 25%, a **Critical Quality Alert** is issued, indicating a systemic failure rather than a minor friction.
  <br>
  <img src="images/strategic_insights.jpg" width="800">
  <br>

- **4. NLP Root Cause Analysis (Keyword Frequency)**
  Using Document Frequency (DF) analysis, the system scans all negative reviews for recurring keywords like `DURABILITY`, `PRICE`, or `SIZING`. This tells us exactly *why* customers are unhappy, providing actionable data for the R&D team.
  <br>
  <img src="images/keyword_nlp.jpg" width="800">
  <br>

- **5. Pipeline Integrity & Ingestion Health**
  To maintain enterprise-level reliability, we implemented a **Data Health Monitor**. It tracks the ingestion success rate from AWS S3, ensuring that even failed formats or empty files are accounted for and displayed with 99.99% precision.
  <br>
  <img src="images/data_health.jpg" width="800">
  <br>

# 📂 Repository Structure
- `app.py`: The core Streamlit application logic and UI components.
- `sql_setup/`: Contains SQL scripts for Snowflake Stages, Directory Tables, and Cortex AI integration.
- `images/`: High-resolution screenshots of the dashboard for documentation.
- `requirements.txt`: List of Python libraries required to run the project.

---
<i>Developed by **SungChian Wen** | MSBA at University of California, Irvine.</i>
