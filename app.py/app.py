import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Luxury Brand Intelligence",
    page_icon="💎",
    layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("data/Luxury_Brand_Analysis.xlsx")
    return df
df = load_data()

st.sidebar.title("💎 Luxury Brand Intelligence")
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "🏆 Brand Ranking",
        "⚖️ Brand Comparison",
        "🌍 Market & Sustainability",
        "🤖 Brand Clustering",
        "🧠 Recommendation Engine",
        "📋 Data Explorer"
    ])


if page == "🏠 Overview":
    st.title("💎 Luxury Brand Intelligence Dashboard")
    st.markdown("""**Explore luxury brands using business analytics,
        machine learning and personalized recommendation.**
        """)

    total_brands = df["Brands"].nunique()
    avg_price = df["Average_Price"].mean()
    avg_reach = df["Global Reach Score"].mean()
    avg_sustainability = df[
        "Sustainability Score"
    ].mean()


    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "💎 Total Brands",
        total_brands
    )
    col2.metric(
        "💰 Average Price",
        f"${avg_price:,.0f}"
    )
    col3.metric(
        "🌍 Avg Global Reach",
        f"{avg_reach:.1f}%"
    )
    col4.metric(
        "🌱 Avg Sustainability",
        f"{avg_sustainability:.1f}")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:

        tier_counts = (
            df["Luxury Tier"]
            .value_counts()
            .reset_index())
        tier_counts.columns = [
            "Luxury Tier",
            "Brands"]
        fig = px.pie(
            tier_counts,
            names="Luxury Tier",
            values="Brands",
            title="Luxury Tier Distribution")
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        top_brands = (df[["Brands","Luxury Tier"]].sort_values("Brands",ascending=False).head(10))
        fig = px.bar(top_brands.sort_values("Brands"),
            x="Luxury Tier",
            y="Brands",
            orientation="h",
            title="Top 10 Luxury Brands")
        st.plotly_chart(fig,use_container_width=True)


elif page == "🏆 Brand Ranking":
    st.title("🏆 Luxury Brand Ranking")
    ranking = (
        df[
            [
                "Brands",
                "Parent Company",
                "Luxury Tier",
                "Average_Price",
                "Global Reach Score",
                "Sustainability Score"]].sort_values("Brands",ascending=False))

    st.dataframe(ranking,use_container_width=True,hide_index=True)
    st.subheader("Top Luxury Brands")
    top10 = ranking.head(10)
    fig = px.bar(top10.sort_values("Brands"),
        x="Global Reach Score",
        y="Brands",
        orientation="h",
        title="Top 10 Luxury Brands")
    st.plotly_chart(fig,use_container_width=True)


elif page == "⚖️ Brand Comparison":
    st.title("⚖️ Compare Luxury Brands")
    brands = sorted(df["Brands"].dropna().unique())
    col1, col2 = st.columns(2)
    with col1:brand1 = st.selectbox("Select Brand 1",brands)
    with col2:brand2 = st.selectbox("Select Brand 2",brands,index=1 if len(brands) > 1 else 0)

    b1 = df[df["Brands"] == brand1].iloc[0]
    b2 = df[df["Brands"] == brand2].iloc[0]

    comparison = pd.DataFrame({
        "Metric": [
            "Average Price",
            "Price Ceiling",
            "Stores",
            "Products",
            "Countries",
            "Sustainability",
            "Heritage Age"
        ],
        brand1: [
            b1["Average_Price"],
            b1["Price_Ceiling"],
            b1["Number of Stores"],
            b1["Products Offered"],
            b1["Countries Available"],
            b1["Sustainability Initiatives"],
            b1["Founded Age"]
        ],
        brand2: [
            b2["Average_Price"],
            b2["Price_Ceiling"],
            b2["Number of Stores"],
            b2["Products Offered"],
            b2["Countries Available"],
            b2["Sustainability Initiatives"],
            b2["Founded Age"]
        ]
    }
)

    st.dataframe(comparison,use_container_width=True,hide_index=True)

    metrics = [
        "Global Reach Score",
        "Sustainability Initiatives",
        "Number of Stores",
        "Products Offered",
        "Founded Age",
        "Average_Price"
    ]

    labels = [
        "Global Reach",
        "Sustainability",
        "Stores",
        "Products",
        "Heritage",
        "Price"]
    values1 = [b1[m] for m in metrics]
    values2 = [b2[m] for m in metrics]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values1,theta=labels,fill="toself",name=brand1))
    fig.add_trace(go.Scatterpolar(r=values2,theta=labels,fill="toself",name=brand2))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0, 1])),title=f"{brand1} vs {brand2}")
    st.plotly_chart(fig,use_container_width=True)


elif page == "🌍 Market & Sustainability":
    st.title("🌍 Market & Sustainability Intelligence")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(
            df,
            x="Global Reach Score",
            y="Average_Price",
            size="Number of Stores",
            color="Luxury Tier",
            hover_name="Brands",
            title="Price vs Global Reach",
            log_y=True)
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        sustainability = (df.groupby("Luxury Tier")["Sustainability Score"].mean().reset_index()
        )

        fig = px.bar(
            sustainability,
            x="Luxury Tier",
            y="Sustainability Score",
            title="Sustainability by Luxury Tier")
        st.plotly_chart(fig,use_container_width=True)

    st.subheader("🌱 Most Sustainable Brands")
    sustainable = (
        df[[
                "Brands",
                "Luxury Tier",
                "Sustainability Score"]].sort_values("Sustainability Score",ascending=False).head(15))
    st.dataframe(sustainable,use_container_width=True,hide_index=True)

elif page == "🤖 Brand Clustering":
    st.title("🤖 Luxury Brand Clustering")
    if "Cluster" not in df.columns:
        st.warning("Cluster column not found in dataset.")

    else:
        fig = px.scatter(
            df,
            x="PCA1",
            y="PCA2",
            color=df["Cluster"].astype(str),
            hover_name="Brands",
            hover_data=[
                "Luxury Tier",
                "Average_Price",
                "Global Reach Score",
                "Sustainability Score"],
            title="Luxury Brand Clusters")
        st.plotly_chart(
            fig,
            use_container_width=True)
        st.subheader("Cluster Profiles")
        cluster_profile = (
            df.groupby("Cluster")[
                [
                    "Average_Price",
                    "Number of Stores",
                    "Products Offered",
                    "Countries Available",
                    "Sustainability Score",
                    "Founded Age"]].mean().round(2))
        st.dataframe(cluster_profile,use_container_width=True)
        
elif page == "🧠 Recommendation Engine":
    st.title("🧠 Luxury Brand Recommendation Engine")
    st.write("Find the luxury brands that best match your preferences.")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Target Gender",sorted(df["Target Gender"].dropna().unique()))
        tier = st.selectbox("Preferred Luxury Tier",sorted(df["Luxury Tier"].dropna().unique()))
    with col2:
        budget = st.number_input(
            "Budget ($)",
            min_value=100,
            max_value=2000000,
            value=50000,
            step=1000)
        sustainability = st.slider("Importance of Sustainability",
            min_value=0,
            max_value=5,
            value=3)
        
    def calculate_score(row):
        score = 0
        if (row["Target Gender"] == gender or row["Target Gender"] == "Male & Female"):
            score += 20
        if row["Luxury Tier"] == tier:
            score += 20
        if not pd.isna(row["Average_Price"]):
            difference = abs(row["Average_Price"] - budget)
            budget_score = max(0,20 - (difference / budget * 20))
            score += budget_score
        sustainability_score = min(row["Sustainability Initiatives"] * 4,20)
        score += (sustainability_score *(sustainability / 5))
        score += (row["Global Reach Score"] / 100) * 20
        return min(score, 100)
    
    if st.button("🔍 Find Best Brands",use_container_width=True):
        recommendations = df.copy()
        recommendations["Compatibility Score"] = recommendations.apply(calculate_score,axis=1)
        recommendations = (
            recommendations[
                [
                    "Brands",
                    "Luxury Tier",
                    "Average_Price",
                    "Global Reach Score",
                    "Sustainability Initiatives",
                    "Compatibility Score"
                    ]].sort_values("Compatibility Score",ascending=False).head(10))
        st.success(
            f"🏆 Best Match: "
            f"{recommendations.iloc[0]['Brands']}")
        st.metric(
            "Compatibility Score",
            f"{recommendations.iloc[0]['Compatibility Score']:.1f}%")
        st.dataframe(
            recommendations,
            use_container_width=True,
            hide_index=True)
elif page == "📋 Data Explorer":
    st.title("📋 Luxury Brand Dataset")
    st.write(
        f"Dataset contains "
        f"**{len(df):,} brands**.")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True)
