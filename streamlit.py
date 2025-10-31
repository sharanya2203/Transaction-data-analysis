import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Transactional Data Analysis", layout="wide")
st.title("💰 Transactional Data Analysis Dashboard")

# Developer credit
st.markdown("### 👨‍💻 Developed by *Sharanya*")

# --- File Upload Section ---
uploaded_file = st.file_uploader("📂 Upload your transactional CSV file", type="csv")

if uploaded_file is not None:
    # Read the file
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # --- Column Mapping based on your dataset ---
    amt_col = 't_amt'
    cat_col = 'services'
    subcat_col = 'products_used'
    cust_col = 'cust_id'
    city_col = 'city'
    state_col = 'state'
    pay_col = 't_details'  # assumed to contain payment or transaction details

    # --- Data Cleaning ---
    df['t_date'] = pd.to_datetime(df['t_date'], errors='coerce')
    df[amt_col] = pd.to_numeric(df[amt_col], errors='coerce')
    df[subcat_col] = df[subcat_col].astype(str)
    df[pay_col] = df[pay_col].astype(str)

    st.success("✅ File uploaded successfully!")
    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    # --- Dropdown Menu ---
    questions = [
        "1 Total sales amount across all transactions",
        "2 Month with highest total transaction amount",
        "3 Average transaction amount per customer",
        "4 Trend of total sales over months",
        "5 Highest single transaction amount recorded",
        "6 Service category contributing most to total revenue",
        "7 Product generating highest revenue",
        "8 Average transaction amount variation between services",
        "9 Number of unique customers",
        "10 Customers who spent the most overall",
        "11 Average number of transactions per customer",
        "12 Customers who purchased in multiple categories",
        "13 Percentage of repeat buyers",
        "14 Product category with highest total sales",
        "15 Most popular services by transaction count",
        "16 For each service, most frequently purchased product type",
        "17 Average transaction amount per product type",
        "18 Services where customers spend significantly more",
        "19 State with highest total sales",
        "20 City with highest number of transactions",
        "21 Average spending per transaction in each state",
        "22 Services popular in specific states",
        "23 States buying most Outdoor Recreation products",
        "24 Compare average spending between California and Texas",
        "25 Quarter with highest sales",
        "26 Month-by-month total sales variation",
        "27 Total number of transactions per month",
        "28 Season when sports equipment sales spike",
        "29 Number of credit transactions",
        "30 Total revenue from credit transactions",
        "31 Difference in average spending between credit and debit customers",
        "32 States/cities to focus marketing high-value products",
        "33 Should more Exercise & Fitness inventory be stocked",
        "34 Product categories with high sales but low average amounts",
        "35 Underperforming service categories needing offers"
    ]

    choice = st.selectbox("🧭 Select your question:", questions)

    # --- Logic for each question ---
    if choice == questions[0]:
        total = df[amt_col].sum()
        st.metric("💵 Total Sales Amount", f"${total:,.2f}")

    elif choice == questions[1]:
        df['Month'] = df['t_date'].dt.month_name()
        monthly = df.groupby('Month')[amt_col].sum().sort_values(ascending=False)
        st.bar_chart(monthly)
        st.write(f"🏆 Highest month: *{monthly.idxmax()}* (${monthly.max():,.2f})")

    elif choice == questions[2]:
        avg = df.groupby(cust_col)[amt_col].mean().mean()
        st.metric("📈 Avg Transaction Amount per Customer", f"${avg:,.2f}")

    elif choice == questions[3]:
        monthly_sales = df.groupby(df['t_date'].dt.to_period('M'))[amt_col].sum().to_timestamp()
        st.line_chart(monthly_sales)
        st.write("📅 Trend of total sales over months")

    elif choice == questions[4]:
        st.metric("💰 Highest Transaction Amount", f"${df[amt_col].max():,.2f}")

    elif choice == questions[5]:
        revenue = df.groupby(cat_col)[amt_col].sum().sort_values(ascending=False)
        st.bar_chart(revenue)
        st.write(f"🏆 Top Service Category: *{revenue.idxmax()}* (${revenue.max():,.2f})")

    elif choice == questions[6]:
        product_rev = df.groupby(subcat_col)[amt_col].sum().sort_values(ascending=False)
        st.bar_chart(product_rev)
        st.write(f"🏆 Highest Revenue Product: *{product_rev.idxmax()}* (${product_rev.max():,.2f})")

    elif choice == questions[7]:
        avg_service = df.groupby(cat_col)[amt_col].mean()
        st.bar_chart(avg_service)
        st.write("📊 Average transaction amount per service category")

    elif choice == questions[8]:
        st.metric("👥 Unique Customers", df[cust_col].nunique())

    elif choice == questions[9]:
        top_customers = df.groupby(cust_col)[amt_col].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_customers)
        st.write("🏆 Top 10 customers by total spend")

    elif choice == questions[10]:
        avg_txn_per_cust = df.groupby(cust_col).size().mean()
        st.metric("🧾 Avg Transactions per Customer", f"{avg_txn_per_cust:.2f}")

    elif choice == questions[11]:
        multi_cat = df.groupby(cust_col)[cat_col].nunique()
        multi_buyers = multi_cat[multi_cat > 1]
        st.write(f"👥 Customers with multi-category purchases: {multi_buyers.count()}")

    elif choice == questions[12]:
        repeat = df[cust_col].value_counts()
        repeat_buyers = (repeat > 1).sum()
        pct = (repeat_buyers / df[cust_col].nunique()) * 100
        st.metric("🔁 Repeat Buyers %", f"{pct:.2f}%")

    elif choice == questions[13]:
        cat_sales = df.groupby(cat_col)[amt_col].sum().sort_values(ascending=False)
        st.bar_chart(cat_sales)

    elif choice == questions[14]:
        st.bar_chart(df[cat_col].value_counts())
        st.write("📦 Most popular services by transaction count")

    elif choice == questions[15]:
        freq = df.groupby([cat_col, subcat_col]).size().reset_index(name='Count')
        st.dataframe(freq.sort_values('Count', ascending=False).head(10))

    elif choice == questions[16]:
        avg_prod = df.groupby(subcat_col)[amt_col].mean().sort_values(ascending=False)
        st.bar_chart(avg_prod)

    elif choice == questions[17]:
        top_services = df.groupby(cat_col)[amt_col].mean().sort_values(ascending=False)
        st.bar_chart(top_services)

    elif choice == questions[18]:
        state_sales = df.groupby(state_col)[amt_col].sum().sort_values(ascending=False)
        st.bar_chart(state_sales)

    elif choice == questions[19]:
        city_txns = df[city_col].value_counts().head(10)
        st.bar_chart(city_txns)

    elif choice == questions[20]:
        avg_state = df.groupby(state_col)[amt_col].mean().sort_values(ascending=False)
        st.bar_chart(avg_state)

    elif choice == questions[21]:
        combo = df.groupby([state_col, cat_col]).size().reset_index(name="Count")
        st.dataframe(combo)

    elif choice == questions[22]:
        outdoor = df[df[subcat_col].str.contains("Outdoor", case=False, na=False)]
        outdoor_states = outdoor.groupby(state_col)[amt_col].sum()
        st.bar_chart(outdoor_states)

    elif choice == questions[23]:
        ca = df[df[state_col].str.contains("California", case=False, na=False)][amt_col].mean()
        tx = df[df[state_col].str.contains("Texas", case=False, na=False)][amt_col].mean()
        st.metric("CA Avg Spending", f"${ca:,.2f}")
        st.metric("TX Avg Spending", f"${tx:,.2f}")

    elif choice == questions[24]:
        df['Quarter'] = df['t_date'].dt.to_period('Q')
        q_sales = df.groupby('Quarter')[amt_col].sum().to_timestamp()
        st.bar_chart(q_sales)

    elif choice == questions[25]:
        monthly = df.groupby(df['t_date'].dt.month_name())[amt_col].sum()
        st.line_chart(monthly)

    elif choice == questions[26]:
        count_month = df.groupby(df['t_date'].dt.month_name()).size()
        st.bar_chart(count_month)

    elif choice == questions[27]:
        sports = df[df[subcat_col].str.contains("Sports", case=False, na=False)]
        monthly_sports = sports.groupby(df['t_date'].dt.month_name())[amt_col].sum()
        st.line_chart(monthly_sports)

    elif choice == questions[28]:
        credit_txn = df[df[pay_col].str.contains("Credit", case=False, na=False)]
        st.metric("💳 Credit Transactions", len(credit_txn))

    elif choice == questions[29]:
        credit_rev = df[df[pay_col].str.contains("Credit", case=False, na=False)][amt_col].sum()
        st.metric("💳 Credit Revenue", f"${credit_rev:,.2f}")

    elif choice == questions[30]:
        avg_credit = df[df[pay_col].str.contains("Credit", case=False, na=False)][amt_col].mean()
        avg_debit = df[df[pay_col].str.contains("Debit", case=False, na=False)][amt_col].mean()
        st.metric("Credit Avg", f"${avg_credit:,.2f}")
        st.metric("Debit Avg", f"${avg_debit:,.2f}")

    elif choice == questions[31]:
        high_value = df.groupby(state_col)[amt_col].mean().sort_values(ascending=False).head(5)
        st.bar_chart(high_value)

    elif choice == questions[32]:
        fitness = df[df[subcat_col].str.contains("Exercise", case=False, na=False)]
        st.metric("🏋 Exercise & Fitness Total Sales", f"${fitness[amt_col].sum():,.2f}")

    elif choice == questions[33]:
        cat_compare = df.groupby(cat_col)[amt_col].agg(['sum', 'mean'])
        st.dataframe(cat_compare.sort_values('sum', ascending=False))

    elif choice == questions[34]:
        avg_rev = df.groupby(cat_col)[amt_col].mean()
        st.bar_chart(avg_rev)
        st.write("🧾 Low performing categories might need offers")

    # --- Summary Section ---
    st.markdown("---")
    st.subheader("📘 Dataset Summary")
    st.markdown("""
    This transactional dataset contains detailed information about customer purchases, including transaction amounts, product categories, services, payment types, and locations.  
    It allows businesses to explore *customer spending behavior, **popular product categories, and **regional sales trends*.  
    Insights from this dashboard can help:
    - 🧭 Identify top-performing products and services  
    - 💡 Detect underperforming areas for promotional strategies  
    - 🏙 Understand geographical variations in customer demand  
    - 💳 Compare payment preferences (Credit vs. Debit)  
    - 📈 Plan marketing and inventory decisions strategically  

    Overall, this dashboard serves as a *comprehensive analytical tool* for understanding sales performance, customer loyalty, and market opportunities.
    """)

else:
    st.info("👆 Please upload your transactional CSV file to begin.")
