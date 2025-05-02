
## Purpose

#### Check out our [website](https://hannahmgordon-fronttoback-codewebsite-6jii0p.streamlit.app/) to explore our team's work!

#### The data cleaning and text analysis related tasks are performed in the TextualAnalysis.ipynb .

#### The team has created some graphs and visuals in the Visualization.ipynb file to gather some interesting findings from the work.

10-K filings  are rich sources of data about a firm's financial health, strategy, and risk factors. However, due to their length and complexity, investors may not fully process all the nuanced information they contain. The "Lazy Prices" paper, which this code closely aligns with, posits that changes in the language used in these filings can signal important shifts in a company's prospects. 

"Changes to the language and construction of financial reports also have strong implications for firms’ future returns: a portfolio that shorts “changers” and buys “non-changers” earns up to 188 basis points in monthly alphas (over 22% per year) in the future." 

The authors demonstrate that these textual changes have predictive power for future stock returns, suggesting that the market underreacts to this information initially. Hence, the term "Lazy Prices".

To empirically investigate this theory, this repo is designed to contain code that performs textual analysis tasks on the 10-K files from 1993 to 2024 for the S&P 500 firms.

#### These tasks are performed within the file named TextualAnalysis.ipynb : 

- Data Acquisition and Loading: The first step is to gather all the 10-K filings to analyse. There's three ways to go about this:

    - One could fetch the documents using the SEC EDGAR downloader.  This method provides the most direct access to the original data but requires significant amount of time to process, clean and prepare the text for analysis.
    - One can also download a giant 50 GB folder of all 10-X files in a zipped format. The raw text files are cleaned by removing non-textual data, structural markup, and irrelevant headers/footers to isolate the textual content for analysis.
    - Alternatively, one can also use the Loughran-McDonald 10-K Document Dictionaries file. This 15.8GB (unzipped) text file contains word counts for each word in the LM dictionary for every 10-K filing in the dataset. This was the quickest option, and we decided to use it. This takes 45-60 minutes to download. 


- Now that the data is prepared, for the actual textual analysis, we determined it would be best to utilise the cosine similarity to measure the changes in the texts.

    - Our code extracts word counts from the 10-K dictionary for each S&P 500 firm. These counts are converted into numerical vectors, with each dimension representing a word's frequency.
    - Cosine similarity is calculated to compare word count vectors between consecutive years. Cosine distance (1 - cosine similarity) quantifies the year-over-year change in textual content.

- Next, the cosine distances are merged with financial data (stock returns) for S&P 500 firms. This merge connects textual changes to how the market values the firms.
- Filing dates are incorporated to ensure accurate timing of information and returns.

- The data was sorted into five bins each year based on Cosine Similarity, ranking firms from those with the least change in their 10-K filings (Bin 1) to those with the most change (Bin 5).

#### Our final data set contains the following attributes (columns):

| Symbol      | CIK | Filing Date | Filing Year  | Cosine Distance | Cosine Similarity | Return Measures | Bin |

#### Findings:

- High similarity bins outperforming all other bins: The analysis indicates that portfolios composed of firms with high 10-K filing similarity (Bin 5) demonstrated the strongest performance over the long term. This suggests that companies with consistent disclosures, ie going long on "non-changers", tend to provide better returns.

- Mixed Results for some bins: Contrary to some expectations, the performance of portfolios with lower similarity filings (Bins 1-3) was not uniformly poor. While Bin 3 underperformed, Bins 1, 2, and 4 showed varying degrees of positive returns, with Bins 2 and 4 showing strong performance, though not as strong as Bin 5.   

- The correlation matrix revealed that there isn't a straightforward linear relationship between cosine similarity and short-term returns. This implies that the impact of textual similarity on stock performance might depend on other factors specific to the firm.   

#### Conclusions:

- Our version of re-replicating the original paper generally supports the idea that textual similarity in 10-K filings has predictive power for future stock returns.   

- Our original hypothesis that similar disclosures are associated with stronger long-term stock performance. Significant changes or novelty in financial disclosures might signal increased risk or uncertainty, potentially leading to weaker or more inconsistent returns.   

#### Takeaways:

Investors may benefit from paying attention to the consistency of language in 10-K filings, as it can provide insights into a firm's future prospects.

While high similarity generally correlates with positive returns, it's crucial to consider other firm-specific characteristics to get a complete picture, as we did not attempt to prove a casual link between the two.

Further research could explore the specific types of textual changes or sentiment analysis that are most predictive of stock performance and the reasons behind the market's reaction to these changes.


