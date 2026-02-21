import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import plotly.express as px

# 1. Setup & Data Loading
st.set_page_config(layout="wide", page_title="Product Intelligence Dashboard")
session = get_active_session()

def load_latest_data():
    df = session.table("final_product_reviews").to_pandas()
    try:
        audit = session.table("data_audit_log").to_pandas()
    except:
        audit = pd.DataFrame(columns=['FILE_PATH', 'FILE_SIZE', 'LAST_MODIFIED', 'STATUS'])
    return df, audit

try:
    df_raw, df_audit = load_latest_data()

    # 2. Integrated Top Filter
    st.title("❄️ Product Analysis Dashboard")
    f_col1, _ = st.columns([1, 3])
    with f_col1:
        product_options = ["All Products"] + sorted(list(df_raw['PRODUCT'].unique()))
        selected_product = st.selectbox("🎯 Target Product Scope", product_options)
    
    st.divider()

    # Data Filtering
    is_all = selected_product == "All Products"
    display_df = df_raw if is_all else df_raw[df_raw['PRODUCT'] == selected_product]
    avg_sent = display_df['SENTIMENT_SCORE'].mean()

    # 3. Top KPIs
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Reviews Count", len(display_df))
    m2.metric("Avg Sentiment Score", f"{avg_sent:.2f}")
    m3.metric("Current Selection", selected_product)

    st.divider()

    # 4. Multi-Tabbed Analysis
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analytics", 
        "📝 AI Summaries", 
        "💡 Strategic Insights", 
        "🛡️ Data Health", 
        "🔍 Raw Data"
    ])

    # --- Tab 1: Analytics ---
    with tab1:
        if is_all:
            st.subheader("1. Global Product Performance Comparison")
            # 1a. Avg Sentiment by Product
            prod_avg = df_raw.groupby('PRODUCT')['SENTIMENT_SCORE'].mean().sort_values().reset_index()
            fig_avg = px.bar(prod_avg, x='PRODUCT', y='SENTIMENT_SCORE', title="Average Sentiment by Product", 
                             color='SENTIMENT_SCORE', color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_avg, use_container_width=True)

            # 1b. Volume by Product
            prod_count = df_raw.groupby('PRODUCT').size().reset_index(name='COUNT')
            fig_vol = px.bar(prod_count, x='PRODUCT', y='COUNT', title="Volume of Reviews by Product")
            st.plotly_chart(fig_vol, use_container_width=True)
            st.divider()

        # 2. Sentiment Trend (Stacked Bar)
        st.subheader("2. Sentiment Trend Analytics (Stacked)")
        fig_stacked = px.bar(
            display_df, x="DATE", y="SENTIMENT_SCORE", color="PRODUCT", 
            barmode="relative", title="Sentiment Score Over Time",
            hover_data=["PRODUCT", "FILENAME"]
        )
        fig_stacked.update_layout(hovermode="x unified")
        st.plotly_chart(fig_stacked, use_container_width=True)

        # 3. Sentiment Categorization (Donut)
        st.divider()
        st.subheader("3. Sentiment Categorization")
        fig_donut = px.pie(
            display_df, names='SENTIMENT_LABEL', hole=0.5, 
            title="Distribution of Sentiment Labels",
            color_discrete_map={'Positive':'#00CC96', 'Neutral':'#636EFA', 'Negative':'#EF553B'}
        )
        fig_donut.update_traces(textinfo='percent+label+value')
        st.plotly_chart(fig_donut, use_container_width=True)

    # --- Tab 2: AI Summaries ---
    with tab2:
        for _, row in display_df.sort_values(by='DATE', ascending=False).iterrows():
            with st.expander(f"{row['PRODUCT']} | {row['DATE']} | {row['SENTIMENT_LABEL']}:{row['SENTIMENT_SCORE']} | File: {row['FILENAME']}"):
                st.write(f"**AI Summary:** {row['SUMMARY']}")
                st.caption(f"Translated Review: {row['TRANSLATED_REVIEW']}")

    # --- Tab 3: Strategic Insights ---
    with tab3:
        st.subheader("🎯 Data-Driven Strategic Analysis")
        
        # 1. Core proportion calculation
        total_count = len(display_df)
        neg_cases = display_df[display_df['SENTIMENT_SCORE'] < -0.3]
        neg_count = len(neg_cases)
        
        # Calculate the percentage of negative reviews (Portion)
        neg_portion = (neg_count / total_count) if total_count > 0 else 0
        
        c1, c2 = st.columns([1, 2])
        with c1:
            # pie chart (displaying a visualization of the portion)
            insight_counts = display_df['SENTIMENT_LABEL'].value_counts().reset_index()
            insight_counts.columns = ['SENTIMENT_LABEL', 'COUNT']
            fig_insight = px.pie(
                insight_counts, values='COUNT', names='SENTIMENT_LABEL', hole=0.4,
                title=f"Sentiment Composition: {selected_product}",
                color='SENTIMENT_LABEL',
                color_discrete_map={'Positive':'#00CC96','Negative':'#EF553B','Neutral':'#636EFA'}
            )
            fig_insight.update_traces(hovertemplate="<b>%{label}</b><br>Portion: %{percent}<br>Total: %{value}")
            st.plotly_chart(fig_insight, use_container_width=True)
            
        with c2:
            st.write(f"### 🚨 Executive Summary: {selected_product}")
            
            # 2. Dynamic analysis based on "proportion"
            if neg_count > 0:
                # Define Portion thresholds
                if neg_portion > 0.25: # exceeding 25% is considered a serious quality crisis.
                    st.error(f"**Critical Quality Alert:** Negative feedback represents **{neg_portion:.1%}** of total reviews. This indicates a systemic failure in product quality or expectations.")
                elif neg_portion > 0.10: # 10%-25% is considered a significant pain point.
                    st.warning(f"**Significant Dissatisfaction:** **{neg_portion:.1%}** of customers are reporting issues. This exceeds the standard industry tolerance for premium products.")
                else: # Below 10% is considered within the controlled range.
                    st.info(f"**Minor Friction Detected:** Only **{neg_portion:.1%}** of the feedback is negative. While these are isolated cases, we've identified recurring keywords below.")

                # 3. NLP (Document Frequency)
                keywords = ['stitching', 'size', 'waterproof', 'smell', 'grip', 'durability', 'quality', 'price', 'warmth']
                found_keywords = {}
                for kw in keywords:
                    has_kw = neg_cases['TRANSLATED_REVIEW'].str.contains(rf'\b{kw}\b', case=False, regex=True).sum()
                    if has_kw > 0:
                        found_keywords[kw] = int(has_kw)
                
                sorted_keywords = sorted(found_keywords.items(), key=lambda x: x[1], reverse=True)

                if sorted_keywords:
                    st.write(f"**Key Pain Points (from {neg_portion:.1%} negative portion):**")
                    k_cols = st.columns(len(sorted_keywords[:5]))
                    for i, (word, count) in enumerate(sorted_keywords[:5]):
                        k_cols[i].button(f"{word.upper()} ({count})", key=f"v3_kw_{i}")
                    
                    st.divider()
                    top_issue = sorted_keywords[0][0].upper()
                    st.markdown(f"""
                    * **Strategic Insight:** Despite the overall volume, **{top_issue}** is the primary driver behind the **{neg_portion:.1%}** negative sentiment. 
                    * **Recommendation:** Focus resources on addressing **{top_issue}** to effectively reduce the dissatisfaction portion.
                    """)
            else:
                st.success(f"✅ **Exemplary Performance:** 0% negative feedback within the current scope of **{selected_product}**.")

        # 4. Distribution matrix
        st.divider()
        st.write("### 📈 Sentiment Severity Matrix")
        fig_matrix = px.scatter(
            display_df, x="DATE", y="SENTIMENT_SCORE", color="SENTIMENT_LABEL",
            size=display_df['SENTIMENT_SCORE'].abs(),
            hover_data=["PRODUCT", "FILENAME"],
            title="Severity Map (Review Score vs. Timeline)"
        )
        st.plotly_chart(fig_matrix, use_container_width=True)

    # --- Tab 4: Data Health ---
    with tab4:
        st.subheader("🛡️ Pipeline Integrity & Audit Log")
        
        # 1. Pie Chart (Portion)
        # count the number of each state to ensure the proportions are correct.
        audit_counts = df_audit['STATUS'].value_counts().reset_index()
        audit_counts.columns = ['STATUS', 'COUNT']

        # Calculate the percentage of each item
        total_files = audit_counts['COUNT'].sum()
        audit_counts['PERCENT'] = (audit_counts['COUNT'] / total_files) * 100
        
        fig_health = px.pie(
            audit_counts, 
            values='COUNT', 
            names='STATUS', 
            hole=0.6, 
            title="Ingestion Success Rate",
            color='STATUS',
            color_discrete_map={'SUCCESS':'#00CC96', 'FAILED: Invalid Format':'#EF553B', 'FAILED: Empty File':'#FECB52'}
        )
        
        # Use :.2% to automatically convert decimals to percentages and keep two decimal places.
        fig_health.update_traces(
            textinfo='percent+label',
            texttemplate="%{percent:.2%}",
            hovertemplate="<b>Status: %{label}</b><br>Count: %{value}<br>Percentage: %{percent:.2%}"
        )
        
        st.plotly_chart(fig_health, use_container_width=True)
        
        st.divider()

        # 3. Anomaly monitoring text and tables (including precise percentages)
        st.write("### 🚨 Exception Tracking")
        
        # Precise number and proportion of successes and failures
        success_row = audit_counts[audit_counts['STATUS'] == 'SUCCESS']
        success_pct = success_row['PERCENT'].values[0] if not success_row.empty else 0
        
        error_df = df_audit[df_audit['STATUS'] != 'SUCCESS']
        fail_pct = 100 - success_pct
        
        if not error_df.empty:
            st.warning(f"⚠️ Warning: Pipeline Success Rate is {success_pct:.2f}%. Failure Rate is {fail_pct:.2f}%.")
            st.write(f"Detected {len(error_df)} anomalies in the S3 bucket:")
            st.dataframe(error_df, use_container_width=True)
        else:
            st.success(f"✅ All systems healthy. Current Success Rate: {success_pct:.2f}%.")
            with st.expander("View Full Audit Log"):
                st.dataframe(df_audit, use_container_width=True)

    # --- Tab 5: Raw Data ---
    with tab5:
        st.dataframe(display_df, use_container_width=True)

except Exception as e:
    st.error(f"Dashboard Update Error: {e}")