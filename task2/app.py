import streamlit as st
import pandas as pd

from db import init_db, insert_feedback, fetch_all_feedback
from llm import generate_ai_outputs


init_db()

st.set_page_config(page_title="AI Feedback System", layout="wide")

page = st.sidebar.radio("Navigate", ["User Dashboard", "Admin Dashboard"])


# USER DASHBOARD

if page == "User Dashboard":
    st.title("📝 Submit Your Feedback")

    rating = st.radio("Star Rating", [1, 2, 3, 4, 5], horizontal=True)
    review = st.text_area("Write your review", height=150)

    if st.button("Submit"):
        if not review.strip():
            st.warning("Please write a review before submitting.")
        else:
            with st.spinner("Generating AI response..."):
                ai_response, ai_summary, ai_actions = generate_ai_outputs(
                    rating, review
                )

                insert_feedback(
                    rating,
                    review,
                    ai_response,
                    ai_summary,
                    ai_actions
                )

            st.success("Feedback submitted successfully!")
            st.subheader("🤖 AI Response")
            st.write(ai_response)

# ADMIN DASHBOARD
if page == "Admin Dashboard":
    st.title("📊 Admin Dashboard")

    data = fetch_all_feedback()

    if not data:
        st.info("No feedback submitted yet.")
    else:
        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Timestamp",
                "Rating",
                "Review",
                "AI Response",
                "AI Summary",
                "AI Actions"
            ]
        )

        
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])

        
        now = pd.Timestamp.now()

       
        # KPI METRICS
        
        st.subheader("📌 Key Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("⭐ Average Rating", f"{df['Rating'].mean():.2f}")

        with col2:
            st.metric("📝 Total Reviews", len(df))

        with col3:
            last_24h = df[df["Timestamp"] > now - pd.Timedelta(hours=24)]
            st.metric("⏱ Reviews (Last 24h)", len(last_24h))

        # SENTIMENT BREAKDOWN
        st.subheader("🙂 Sentiment Breakdown")

        positive = len(df[df["Rating"] >= 4])
        neutral = len(df[df["Rating"] == 3])
        negative = len(df[df["Rating"] <= 2])

        col1, col2, col3 = st.columns(3)
        col1.metric("😊 Positive (4–5)", positive)
        col2.metric("😐 Neutral (3)", neutral)
        col3.metric("☹️ Negative (1–2)", negative)

        # RATING DISTRIBUTION
        st.subheader("📊 Rating Distribution")
        rating_counts = df["Rating"].value_counts().sort_index()
        st.bar_chart(rating_counts)

        # FEEDBACK ENTRIES
        st.subheader("📋 Feedback Entries")

        for _, row in df.iterrows():
            with st.expander(
                f"⭐ {row['Rating']} — {row['Timestamp'].strftime('%Y-%m-%d %H:%M')}"
            ):
                st.markdown("**Review:**")
                st.write(row["Review"])

                st.markdown("**AI Summary:**")
                st.write(row["AI Summary"])

                st.markdown("**Recommended Actions:**")
                st.write(row["AI Actions"])
