import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset once
@st.cache_data
def load_data():
    data = pd.read_csv("final_cleaned_output.csv")
    data["Filing Date"] = pd.to_datetime(data["Filing Date"])
    data["Return Date"] = pd.to_datetime(data["Return Date"])
    data["YearMonth"] = data["Return Date"].dt.to_period("M").dt.to_timestamp()
    return data

data = load_data()

# Load S&P 500 benchmark data
sp500 = pd.read_csv("SP500_historical.csv")
sp500["date"] = pd.to_datetime(sp500["date"])
sp500["Year"] = sp500["date"].dt.year
sp500.columns = sp500.columns.str.strip()
sp500 = sp500.rename(columns={"Return": "SP500_Return"})

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Annual Returns by Company", "10K Cosine Similarity vs Monthly Return Over Time", "Report"], key="nav", label_visibility="visible")
st.markdown("<style>.stRadio > div{gap: 1.2em !important;} .block-container { padding-top: 1rem !important; }</style>", unsafe_allow_html=True)

# ---------- Page: Home ----------
if page == "Home":
    st.title("Home")
    st.write("Welcome to our Dashboard!")

    st.markdown("""
    This project was inspired by the research paper [Lazy Prices](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1658471), which explores the predictive power of textual changes in 10-K filings. Our analysis aims to replicate and extend these findings through our own implementation.

    The code and data processing for this dashboard were completed in the following GitHub repository: [Final Project Repository](https://github.com/martifigueres/Final-Project-HPST.git).
    """)

    st.markdown("""
    This dashboard explores the relationship between changes in the language of 10-K filings and subsequent stock returns. 
    We have created various visualizations of our data to help our users understand the correlation between changes in 10-K filings and company stock returns. 
    """)

    st.markdown("### Explore the Sections")
    st.markdown("""
    - **Annual Returns by Company**: Visualize yearly stock returns around 10-K filings for each company along with color-coding depending on degree of change in each year's 10-K.
    - **Cosine Similarity vs Monthly Return**: Compare changes in 10-K language with subsequent returns.
    - **Report**: Read about the full methodology, data processing, and motivation behind this analysis.
    """)

# ---------- Page: Annual 10-K Returns by Company ----------
elif page == "Annual Returns by Company":
    st.markdown("<h1 style='margin-top: 0;'>Annual Returns by Company</h1>", unsafe_allow_html=True)

    st.sidebar.header("Select a Company")
    all_symbols = sorted(data["Symbol"].unique())
    selected_symbol = st.sidebar.selectbox("Choose a company:", all_symbols)

    bin_colors = {
        1: "#ff0000",
        2: "#ffa700",
        3: "#fff400",
        4: "#a3ff00",
        5: "#2cba00"
    }

    bin_labels = {
        1: "Bin 1 (largest change in 10-K)",
        2: "Bin 2",
        3: "Bin 3",
        4: "Bin 4",
        5: "Bin 5 (smallest change in 10-K)"
    }

    if selected_symbol:
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot S&P 500 returns as faint line
        sp500_filtered = sp500[sp500["Year"] >= 2004]
        ax.plot(sp500_filtered["Year"], sp500_filtered["SP500_Return"], color="#bbbbbb", linewidth=2, alpha=0.6)

        # Plot selected company with bin coloring
        symbol_df = data[data["Symbol"] == selected_symbol]
        yearly = symbol_df.groupby("Year").agg({"Return": "mean", "Bins": "first"}).reset_index()
        yearly = yearly.sort_values("Year")

        for i in range(len(yearly) - 1):
            x_vals = [yearly["Year"].iloc[i], yearly["Year"].iloc[i+1]]
            y_vals = [yearly["Return"].iloc[i], yearly["Return"].iloc[i+1]]
            bin_val = yearly["Bins"].iloc[i]
            color = bin_colors.get(bin_val, "#000000")
            ax.plot(x_vals, y_vals, color=color, linewidth=3)

        ax.set_title("Yearly Returns Around 10-K Filing", fontsize=16)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Return", fontsize=12)

        ax.axhline(y=0, color='#dddddd', linewidth=1, linestyle='-', alpha=0.5)

        all_years = sorted(set(yearly["Year"]).union(sp500_filtered["Year"] if not sp500_filtered.empty else []))
        ax.set_xticks(all_years)
        ax.set_xticklabels([str(y) if y % 2 == 0 else ' ' for y in all_years])

        st.pyplot(fig)

        st.markdown("### Line Color Legend")
        sp500_note = "<span style='color:#bbbbbb; font-weight:bold;'>■</span> S&P 500 Annual Return"
        st.markdown(f"<div style='font-size:16px; margin-bottom:0.5em'>{sp500_note}</div>", unsafe_allow_html=True)

        bin_legend = "&emsp;".join(
            [f"<span style='color:{bin_colors[b]}; font-weight:bold;'>■</span> {bin_labels[b]}" for b in sorted(bin_colors)]
        )
        st.markdown(f"<div style='font-size:16px;'>{bin_legend}</div>", unsafe_allow_html=True)
    else:
        st.info("Please select a company to view the chart.")

# ---------- Page: Cosine Similarity vs Monthly Return Over Time ----------
elif page == "10K Cosine Similarity vs Monthly Return Over Time":
    st.markdown("<h1 style='margin-top: 0;'>Cosine Similarity vs Monthly Return Over Time</h1>", unsafe_allow_html=True)

    symbols = sorted(data["Symbol"].unique())
    selected_symbol = st.sidebar.selectbox("Choose a company:", symbols)

    firm_df = data[data["Symbol"] == selected_symbol].copy()

    filing_series = firm_df.groupby("Filing Date")["Cosine Similarity"].first().sort_index()
    monthly_return = firm_df.groupby("YearMonth")["Return"].mean().rolling(3, min_periods=1).mean()

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(filing_series.index, filing_series.values, 'o-', color="blue", label="Cosine Similarity")
    ax1.set_ylabel("Cosine Similarity", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.plot(monthly_return.index, monthly_return.values, '-s', color="#cc6600", label="Return (smoothed)")
    ax2.set_ylabel("Return (%)", color="#cc6600")
    ax2.tick_params(axis="y", labelcolor="#cc6600")

    plt.title(f"{selected_symbol} - Cosine Similarity & Returns Over Time")
    fig.tight_layout()

    st.pyplot(fig)
    st.markdown("**Note:** Cosine Similarity is based on filing date (blue), returns are monthly with 3-month smoothing (orange).")

# ---------- Page: Report ----------
else:
    st.title("Report")
    st.markdown("## Method")
    st.markdown("""
10-K filings  are rich sources of data about a firm's financial health, strategy, and risk factors. However, due to their length and complexity, investors may not fully process all the nuanced information they contain. The "Lazy Prices" paper, which this code closely aligns with, posits that changes in the language used in these filings can signal important shifts in a company's prospects. The authors demonstrate that these textual changes have predictive power for future stock returns, suggesting that the market underreacts to this information initially.

To empirically investigate this theory, this repo is designed to contain code that performs textual analysis tasks on the 10-K files from 1993 to 2024 for the S&P 500 firms.

These tasks are performed within the file named TextualAnalysis.ipynb : 

- Data Acquisition and Loading: The first step is to gather all the 10-K filings to analyse. There's three ways to go about this:

    - One could fetch the documents using the SEC EDGAR downloader.  This method provides the most direct access to the original data but requires significant amount of time to process, clean and prepare the text for analysis.
    - One can also download a giant 50 GB folder of all 10-X files in a zipped format. The raw text files are cleaned by removing non-textual data, structural markup, and irrelevant headers/footers to isolate the textual content for analysis.
    - Alternatively, one can also use the Loughran-McDonald 10-K Document Dictionaries file. This 15.8GB (unzipped) text file contains word counts for each word in the LM dictionary for every 10-K filing in the dataset. This was the quickest option, and we decided to use it. 


- Now that the data is prepared, for the actual textual analysis, we determined it would be best to utilise the cosine similarity to measure the changes in the texts.

    - Our code extracts word counts from the 10-K dictionary for each S&P 500 firm. These counts are converted into numerical vectors, with each dimension representing a word's frequency.
    - Cosine similarity is calculated to compare word count vectors between consecutive years. Cosine distance (1 - cosine similarity) quantifies the year-over-year change in textual content.

- Next, the cosine distances are merged with financial data (stock returns) for S&P 500 firms. This merge connects textual changes to how the market values the firms.
- Filing dates are incorporated to ensure accurate timing of information and returns.

- The data was sorted into five bins each year based on Cosine Similarity, ranking firms from those with the least change in their 10-K filings (Bin 1) to those with the most change (Bin 5).

Our final data set contains the following attributes (columns):

| Symbol      | CIK | Filing Date | Filing Year  | Cosine Distance | Cosine Similarity | Return Measures | Bin |

The team has created some graphs and visuals in the Visualization.ipynb file to gather some interesting findings from the work.
    """)


    st.markdown("## Findings")
    st.markdown("""
- **High similarity bins outperforming all other bins**: The analysis indicates that portfolios composed of firms with high 10-K filing similarity (Bin 5) demonstrated the strongest performance over the long term. This suggests that companies with consistent disclosures, ie going long on "non-changers", tend to provide better returns.

- **Mixed Results for some bins**: Contrary to some expectations, the performance of portfolios with lower similarity filings (Bins 1-3) was not uniformly poor. While Bin 3 underperformed, Bins 1, 2, and 4 showed varying degrees of positive returns, with Bins 2 and 4 showing strong performance, though not as strong as Bin 5.   

- **The correlation matrix revealed** that there isn't a straightforward linear relationship between cosine similarity and short-term returns. This implies that the impact of textual similarity on stock performance might depend on other factors specific to the firm.
    """)

    st.markdown("## Conclusions")
    st.markdown("""
Our version of re-replicating the original paper generally supports the idea that textual similarity in 10-K filings has predictive power for future stock returns.

Our original hypothesis that similar disclosures are associated with stronger long-term stock performance. Significant changes or novelty in financial disclosures might signal increased risk or uncertainty, potentially leading to weaker or more inconsistent returns.
    """)

    st.markdown("## Takeaways")
    st.markdown("""
- Investors may benefit from paying attention to the consistency of language in 10-K filings, as it can provide insights into a firm's future prospects.

- While high similarity generally correlates with positive returns, it's crucial to consider other firm-specific characteristics to get a complete picture, as we did not attempt to prove a casual link between the two.

- Further research could explore the specific types of textual changes or sentiment analysis that are most predictive of stock performance and the reasons behind the market's reaction to these changes.
    """)

    # Final images
    st.image("pics/pic1.png")
    st.image("pics/pic2.png", use_container_width=True)
