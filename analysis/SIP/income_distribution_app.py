import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import yfinance as yf

DEFAULT_CONFIG = {
    # Income defaults
    'monthly_income': 1000,  # Default monthly income
    
    'usd_pkr_rate': yf.Ticker("PKR=X").info['regularMarketPrice'],  # Get live USD/PKR rate
    'usdt_usd_rate': yf.Ticker("USDT-USD").info['regularMarketPrice'],  # Get live USDT/USD rate
    'gbp_usd_rate': yf.Ticker("GBP=X").info['regularMarketPrice'],  # Get live GBP/USD rate
    
    # Portfolio allocation defaults
    'crypto_allocation': 10,  # Default crypto allocation percentage
    'international_allocation': 20,  # Default international exposure percentage
    
    'risk_tolerance': 'Moderate',  # Default risk profile
    'investment_horizon': 10,  # Default investment timeframe in years
    'rebalancing_freq': 'Quarterly',  # Default rebalancing frequency
    
    # Sample PKR allocations
    'pkr_allocations': {
        'Category 1': 50000,
        'Category 2': 50000, 
        'Category 3': 50000,
        'Category 4': 50000,
        'Emergency Fund': 50000
    },
    
    # Historical returns (sample CAGR)
    'historical_returns': {
        'VOO (S&P 500)': 0.09,
        'QQQ (Nasdaq 100)': 0.12,
        'VWO (Emerging Markets)': 0.06,
        'VTI (Total US Market)': 0.09,
        'Bitcoin (BTC)': 0.20,
        'Ethereum (ETH)': 0.15,
        'BND (Total Bond Market)': 0.04,
        'ARKK (Innovation ETF)': 0.08,
        'Cash/Money Market': 0.03
    },
    
    # Risk profiles
    'risk_metrics': {
        'Conservative': {'Max Drawdown': '15%', 'Volatility': 'Low', 'Recovery Time': '2-3 years'},
        'Moderate': {'Max Drawdown': '25%', 'Volatility': 'Medium', 'Recovery Time': '3-5 years'},
        'Aggressive': {'Max Drawdown': '40%', 'Volatility': 'High', 'Recovery Time': '5-7 years'}
    }
}

# Page config
st.set_page_config(
    page_title="Income Distribution & Portfolio Optimizer",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Income Distribution & Portfolio Optimizer")

# Sidebar for advanced settings
with st.sidebar:
    st.header("⚙️ Advanced Settings")
    
    # Risk tolerance
    risk_tolerance = st.selectbox(
        "Risk Tolerance:",
        ["Conservative", "Moderate", "Aggressive"],
        index=["Conservative", "Moderate", "Aggressive"].index(DEFAULT_CONFIG['risk_tolerance'])
    )
    
    # Investment horizon
    investment_horizon = st.slider(
        "Investment Horizon (Years):",
        min_value=5,
        max_value=30,
        value=DEFAULT_CONFIG['investment_horizon']
    )
    
    # Rebalancing frequency
    rebalancing_freq = st.selectbox(
        "Rebalancing Frequency:",
        ["Monthly", "Quarterly", "Semi-Annually", "Annually"],
        index=["Monthly", "Quarterly", "Semi-Annually", "Annually"].index(DEFAULT_CONFIG['rebalancing_freq'])
    )

# Input Section
col1, col2 = st.columns(2)

with col1:
    st.header("📥 Income Details")
    monthly_income = st.number_input("Monthly Income (USD):", min_value=0, value=DEFAULT_CONFIG['monthly_income'], step=100)
    conversion_rate = st.number_input("USD to PKR Rate:", min_value=0.0, value=DEFAULT_CONFIG['usd_pkr_rate'], step=1.0)

with col2:
    st.header("🎯 Portfolio Preferences")
    crypto_allocation = st.slider("Crypto Allocation %:", min_value=0, max_value=50, value=DEFAULT_CONFIG['crypto_allocation'])
    international_allocation = st.slider("International Markets %:", min_value=0, max_value=40, value=DEFAULT_CONFIG['international_allocation'])

# Fixed PKR allocations
pkr_allocations = DEFAULT_CONFIG['pkr_allocations']

total_pkr_outflow = sum(pkr_allocations.values())
usd_needed_for_pkr = total_pkr_outflow / conversion_rate
remaining_usd = monthly_income - usd_needed_for_pkr

# Display PKR breakdown
st.header("💰 PKR Allocation Breakdown")
pkr_data = []
for category, amount in pkr_allocations.items():
    pkr_data.append((category, amount))

pkr_df = pd.DataFrame(pkr_data, columns=["Category", "PKR Amount"])
st.dataframe(pkr_df, use_container_width=True)

st.info(f"Total PKR Outflow: {total_pkr_outflow:,} PKR (≈ ${usd_needed_for_pkr:.2f} USD)")

# Prevent negative allocation if income is too low
if remaining_usd < 0:
    st.error("⚠️ Your income is less than your fixed PKR requirement. Please adjust.")
else:
    # Dynamic portfolio allocation based on risk tolerance and preferences
    if risk_tolerance == "Conservative":
        base_equity = 0.60
        base_bonds = 0.30
        base_cash = 0.10
    elif risk_tolerance == "Moderate":
        base_equity = 0.75
        base_bonds = 0.20
        base_cash = 0.05
    else:  # Aggressive
        base_equity = 0.90
        base_bonds = 0.08
        base_cash = 0.02
    
    # Adjust for crypto preference
    crypto_pct = crypto_allocation / 100
    equity_pct = base_equity * (1 - crypto_pct)
    bonds_pct = base_bonds * (1 - crypto_pct)
    cash_pct = base_cash * (1 - crypto_pct)
    
    # Macro Level Distribution
    st.header("📊 Macro Level Distribution")
    
    macro_data = [
        ("PKR Expenses (Total)", usd_needed_for_pkr, total_pkr_outflow),
        ("Investments (USD)", remaining_usd * 0.85, None),
        ("USD Cash Buffer", remaining_usd * 0.10, None),
        ("Flex / Misc (USD)", remaining_usd * 0.05, None),
    ]
    
    macro_df = pd.DataFrame(macro_data, columns=["Category", "USD Amount", "PKR Amount"])
    st.dataframe(macro_df, use_container_width=True)
    
    # Enhanced Investment Portfolio
    st.header("📈 Optimized Investment Portfolio")
    
    investment_amount = remaining_usd * 0.85
    
    # Dynamic allocation based on risk tolerance and preferences
    if risk_tolerance == "Conservative":
        investment_categories = {
            'VOO (S&P 500)': 0.35,
            'BND (Total Bond Market)': 0.25,
            'VWO (Emerging Markets)': 0.10,
            'VTI (Total US Market)': 0.15,
            'Bitcoin (BTC)': crypto_pct * 0.60,
            'Ethereum (ETH)': crypto_pct * 0.40,
            'Cash/Money Market': 0.05
        }
    elif risk_tolerance == "Moderate":
        investment_categories = {
            'VOO (S&P 500)': 0.40,
            'QQQ (Nasdaq 100)': 0.20,
            'VWO (Emerging Markets)': international_allocation/100 * 0.15,
            'VTI (Total US Market)': 0.15,
            'Bitcoin (BTC)': crypto_pct * 0.60,
            'Ethereum (ETH)': crypto_pct * 0.40,
            'BND (Total Bond Market)': 0.10
        }
    else:  # Aggressive
        investment_categories = {
            'VOO (S&P 500)': 0.30,
            'QQQ (Nasdaq 100)': 0.25,
            'VWO (Emerging Markets)': international_allocation/100 * 0.20,
            'Bitcoin (BTC)': crypto_pct * 0.60,
            'Ethereum (ETH)': crypto_pct * 0.40,
            'ARKK (Innovation ETF)': 0.10,
            'VTI (Total US Market)': 0.15
        }
    
    # Remove zero allocations
    investment_categories = {k: v for k, v in investment_categories.items() if v > 0}
    
    # Normalize investment percentages to sum to 1.0
    total_pct = sum(investment_categories.values())
    if total_pct > 0:
        investment_categories = {k: v / total_pct for k, v in investment_categories.items()}
    
    micro_data = []
    for investment, pct in investment_categories.items():
        amount = investment_amount * pct
        micro_data.append((investment, amount, f"{pct*100:.1f}%"))
    
    micro_df = pd.DataFrame(micro_data, columns=["Investment", "USD Amount", "Allocation %"])
    st.dataframe(micro_df, use_container_width=True)
    
    # Portfolio Visualization
    st.header("📊 Portfolio Visualization")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart for investment allocation
        fig_pie = px.pie(
            micro_df, 
            values='USD Amount', 
            names='Investment',
            title='Investment Portfolio Allocation'
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart for macro distribution
        macro_viz_df = macro_df[macro_df['USD Amount'] > 0].copy()
        fig_bar = px.bar(
            macro_viz_df,
            x='Category',
            y='USD Amount',
            title='Macro Level Distribution',
            color='Category'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Portfolio Performance Projections
    st.header("🚀 Portfolio Performance Projections")
    
    # Historical returns (simplified)
    historical_returns = DEFAULT_CONFIG['historical_returns']
    
    # Calculate projected returns
    total_projected_return = 0
    for investment, pct in investment_categories.items():
        if investment in historical_returns:
            total_projected_return += pct * historical_returns[investment]
    
    # Projection over time
    years = list(range(1, investment_horizon + 1))
    projected_values = []
    monthly_investment = investment_amount
    
    # Portfolio projection formula (compound monthly)
    for year in years:
        total_months = year * 12
        monthly_rate = total_projected_return / 12

        if monthly_rate > 0:
            future_value = monthly_investment * (((1 + monthly_rate) ** total_months - 1) / monthly_rate)
        else:
            future_value = monthly_investment * total_months  # Fallback: No growth
        
        projected_values.append(future_value)
    
    projection_df = pd.DataFrame({
        'Year': years,
        'Projected Portfolio Value': projected_values
    })
    
    fig_projection = px.line(
        projection_df,
        x='Year',
        y='Projected Portfolio Value',
        title=f'Portfolio Projection ({investment_horizon} Years)',
        markers=True
    )
    fig_projection.update_layout(yaxis_title="Portfolio Value (USD)")
    st.plotly_chart(fig_projection, use_container_width=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Projected Annual Return",
            f"{total_projected_return*100:.1f}%",
            "Based on historical data"
        )
    
    with col2:
        final_value = projected_values[-1]
        st.metric(
            f"Portfolio Value in {investment_horizon} Years",
            f"${final_value:,.0f}",
            f"From ${monthly_investment*12:,.0f} annual investment"
        )
    
    with col3:
        total_invested = monthly_investment * 12 * investment_horizon
        total_gains = final_value - total_invested
        
        if total_invested > 0:
            roi_pct = (total_gains / total_invested) * 100
        else:
            roi_pct = 0
            
        st.metric(
            "Total Gains",
            f"${total_gains:,.0f}",
            f"{roi_pct:.1f}% return"
        )
    
    with col4:
        st.metric(
            "Annual Investment Amount",
            f"${monthly_investment*12:,.0f}",
            f"(${investment_amount:,.0f}/month)"
        )
    
    # Rebalancing Recommendations
    st.header("⚖️ Portfolio Rebalancing")
    
    st.info(f"""
    **Rebalancing Strategy**: {rebalancing_freq}
    
    **Key Recommendations**:
    - Rebalance when any asset class deviates >5% from target allocation
    - Consider tax-loss harvesting opportunities
    - Review allocation annually based on life changes
    - Maintain emergency fund of 3-6 months expenses
    """)
    
    # Risk Analysis
    st.header("⚠️ Risk Analysis")
    
    risk_metrics = DEFAULT_CONFIG['risk_metrics']
    
    risk_df = pd.DataFrame([risk_metrics[risk_tolerance]], index=[risk_tolerance])
    st.dataframe(risk_df, use_container_width=True)
    
    # Net Worth Tracker Section
    st.header("💼 Net Worth Tracker")
    
    st.info("Manually enter your current account balances for a one-time Net Worth snapshot:")
    
    account1_usd = st.number_input("Account 1 USD Balance:", min_value=0.0, value=0.0)
    account2_gbp = st.number_input("Account 2 GBP Balance:", min_value=0.0, value=0.0)
    account3_usd = st.number_input("Account 3 USD Balance:", min_value=0.0, value=0.0)
    crypto_usdt = st.number_input("Crypto Portfolio USDT Value:", min_value=0.0, value=0.0)
    pkr_balance = st.number_input("PKR Bank Balance:", min_value=0.0, value=0.0)
    other_cash = st.number_input("Other Cash (USD):", min_value=0.0, value=0.0)
    
    # Convert currencies to USD
    pkr_to_usd = pkr_balance / conversion_rate
    gbp_to_usd = account2_gbp / DEFAULT_CONFIG['gbp_usd_rate']
    crypto_usd = crypto_usdt * DEFAULT_CONFIG['usdt_usd_rate']
    
    total_net_worth = (
        account1_usd +
        gbp_to_usd +
        account3_usd +
        crypto_usd +
        pkr_to_usd +
        other_cash
    )
    
    st.success(f"**Your Total Net Worth (USD):** ${total_net_worth:,.2f}")
    
    # Create DataFrame with net worth in multiple currencies
    net_worth_row = pd.DataFrame({
        'Date': [datetime.today().strftime('%Y-%m-%d')],
        'Net Worth USD': [total_net_worth],
        'Net Worth GBP': [total_net_worth / DEFAULT_CONFIG['gbp_usd_rate']],
        'Net Worth PKR': [total_net_worth * conversion_rate]
    })
    
    # Export Section
    st.header("📤 Export Results")
    
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
        
    def save_net_worth_locally(df):
        filename = "net_worth_history.csv"
        try:
            # Try to read existing file
            existing_df = pd.read_csv(filename)
            # Always overwrite with latest data
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_csv(filename, index=False)
            return f"Updated entry in {filename}"
        except FileNotFoundError:
            # Create new file if it doesn't exist
            df.to_csv(filename, index=False)
            return f"Created new file: {filename}"
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        csv_pkr = convert_df(pkr_df)
        st.download_button("PKR Breakdown", csv_pkr, "pkr_breakdown.csv", "text/csv")
    
    with col2:
        csv_macro = convert_df(macro_df)
        st.download_button("Macro Distribution", csv_macro, "macro_distribution.csv", "text/csv")
    
    with col3:
        csv_micro = convert_df(micro_df)
        st.download_button("Investment Portfolio", csv_micro, "investment_portfolio.csv", "text/csv")
    
    with col4:
        csv_projection = convert_df(projection_df)
        st.download_button("Portfolio Projection", csv_projection, "portfolio_projection.csv", "text/csv")
    
    with col5:
        csv_networth = convert_df(net_worth_row)
        st.download_button("Net Worth Entry", csv_networth, "net_worth_entry.csv", "text/csv")
    
    with col6:
        if st.button("Save Net Worth Locally"):
            st.info(save_net_worth_locally(net_worth_row))
    
    # Footer
    st.markdown("---")
    st.markdown("*Data is for educational purposes. Past performance doesn't guarantee future results. Consider consulting a financial advisor.*")
