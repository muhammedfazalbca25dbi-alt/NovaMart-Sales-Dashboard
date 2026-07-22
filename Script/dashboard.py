import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="NovaMart Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 NovaMart Sales Dashboard")
st.caption("Version 4 | Muhammed Fazal")

@st.cache_data
def load_data():

    nova_mart = pd.read_csv(r"C:\Users\muham\OneDrive\Documents\Project2_NovaMart_Streamlit\Project2_NovaMart_Streamlit\data\novamart_clean.csv") 

    rename_columns = {
        "region_y": "region",
        "category_y": "category",
        "sub_category_y": "sub_category"
    }

    nova_mart.rename(columns=rename_columns, inplace=True)

    nova_mart.drop(
        columns=[
            "region_x",
            "category_x",
            "sub_category_x"
        ],
        errors="ignore",
        inplace=True
    )

    return nova_mart

nova_mart = load_data()

st.sidebar.title("Filters")

segment = st.sidebar.multiselect(
    "Select Segment",
    sorted(nova_mart["segment"].dropna().unique()),
    default=sorted(nova_mart["segment"].dropna().unique())
)

region = st.sidebar.multiselect(
    "Select Region",
    sorted(nova_mart["region"].dropna().unique()),
    default=sorted(nova_mart["region"].dropna().unique())
)

filtered_df = nova_mart[
    (nova_mart["segment"].isin(segment))
    &
    (nova_mart["region"].isin(region))
]

st.subheader("Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

st.subheader("Key Performance Indicators")

total_sales = filtered_df["sales"].sum()

customer_count = filtered_df["customer_id"].nunique()

average_order_value = filtered_df["sales"].mean()

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "👥 Customers",
    customer_count
)

col3.metric(
    "🛒 Average Order",
    f"${average_order_value:,.2f}"
)

st.markdown("---")
st.header("Charts & Tables")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Sales by Segment",
    "🍩 Segment Share",
    "📈 Monthly Orders",
    "📋 Top Customers"
])

with tab1:

    st.subheader("Sales by Segment")

    sales_segment = (
        filtered_df
        .groupby("segment")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(sales_segment)

    st.write("### Sales Summary")

    st.dataframe(
        sales_segment.reset_index().rename(
            columns={
                "segment": "Segment",
                "sales": "Total Sales"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

with tab2:

    st.subheader("Segment Share of Sales")

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.pie(
        sales_segment,
        labels=sales_segment.index,
        autopct="%1.1f%%",
        startangle=90,
        radius=0.80,
        pctdistance=0.75,
        labeldistance=1.05,
        wedgeprops=dict(width=0.30),
        textprops={"fontsize": 10}
    )

    ax.set_aspect("equal")

    st.pyplot(fig)

with tab3:


    st.subheader("Monthly Orders per Segment")

    monthly_orders = (
        filtered_df
        .groupby(["order_month", "segment"])
        .size()
        .unstack(fill_value=0)
    )

    st.line_chart(monthly_orders)
with tab4:

    st.subheader("Top 10 Customers by Sales")

    top_customers = (
        filtered_df
        .groupby("customer_name")["sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    top_customers.columns = [
        "Customer Name",
        "Total Sales"
    ]

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")
st.header("NumPy Insights")

threshold = np.percentile(filtered_df["sales"], 90)

top_spenders = filtered_df[
    filtered_df["sales"] >= threshold
]

customer_count = top_spenders["customer_id"].nunique()

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"Top 10% Sales Threshold\n\n${threshold:,.2f}"
    )

with col2:
    st.info(
        f"Top Spending Customers\n\n{customer_count}"
    )

st.write("### Top Spending Records")

st.dataframe(
    top_spenders[
        [
            "customer_name",
            "segment",
            "region",
            "sales"
        ]
    ].sort_values(
        by="sales",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.header("Download")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)

st.markdown("---")
st.header("Dashboard Summary")

summary1, summary2 = st.columns(2)

with summary1:
    st.write("### Dataset Statistics")
    st.write(f"**Rows:** {len(filtered_df):,}")
    st.write(f"**Columns:** {filtered_df.shape[1]}")
    st.write(f"**Segments:** {filtered_df['segment'].nunique()}")
    st.write(f"**Regions:** {filtered_df['region'].nunique()}")

with summary2:
    st.write("### Sales Statistics")
    st.write(f"**Highest Sale:** ${filtered_df['sales'].max():,.2f}")
    st.write(f"**Lowest Sale:** ${filtered_df['sales'].min():,.2f}")
    st.write(f"**Average Sale:** ${filtered_df['sales'].mean():,.2f}")
    st.write(f"**Total Orders:** {len(filtered_df):,}")

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:gray;">
        <h4>📊 NovaMart Sales Dashboard</h4>
        <p>Version 4 Project Submission</p>
        <p>Prepared by <b>Muhammed Fazal</b></p>
    </div>
    """,
    unsafe_allow_html=True
)