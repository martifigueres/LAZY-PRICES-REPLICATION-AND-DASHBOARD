# Project Description

Cohen et al (2020) examined the language and construction of 10-K filings and showed that a “portfolio that shorts “changers” and buys “nonchangers” earns up to 188 basis points per month in alpha (over 22% per year) in the future.” This suggests that traders do not trade on the information reflected in changes in 10-K, possibly due to inattentiveness to this signal or difficulties in obtaining it. 
We are going to attempt to replicate their findings on data before the first draft of their paper was made public (2010) and extend the data to see if the results hold up after publication. 
This exercise will help us 
Understand if we can replicate their key findings
Show if the publication of this paper led to traders to begin pricing in this signal faster (and thus erode its value).

### Sketch of Plan
We need to construct several datasets. 


The first is a (FIRM, FILING) level dataset.This will be sorted by firm and then the date of the filing. The key variable in this dataset will be the similarity of the firm’s filing with the corresponding one from a year prior. There are multiple ways to measure similarity.


The second is a (FIRM, MONTH) level dataset with returns. 


### The key results in the paper come from 
1. Turning the first dataset into a quintile bins (within each year). These are the 5 portfolios. 
2. Then combining this with the second dataset (lagging and filling the bin indicator forward up to 5 months). Now, the second dataset has become a (FIRM, MONTH) return dataset but for most firm-month, which know which PORTFOLIO the firm is in.
3. Turn this into a (MONTH, PORTFOLIO) dataset containing the returns for that portfolio each month. Equal-weighted portfolio returns is fine. 
4. (The authors in the paper do these steps many times with slight changes. They do it with value-weighted portfolio returns. They do it where the quintile bins are defined via Cosine. And then defined via Jaccard. And so on… So they have many versions of the MONTH-PORTFOLIO return data, under different choices of return aggregation and how portfolios are formed, under difference restrictions on which firms are in the sample, etc.)


The resulting (MONTH, PORTFOLIO) dataset can be combined with the market return, and the 3 and 5 factors to make the main table in the paper (below, where Q1-Q5 are the bins/portfolios), and we can use code from the textbook to do it.



### Outputs 
We can make this table using data from before 2010, and then using data after 2010. The hope is that the pre-2010 results will look similar to this. The post-2010 results might be weaker. 
We can plot the returns for our 5 portfolios and the Q5-Q1 long-short portfolio as in the textbook.
If we get this far, and WE WILL, there is a lot of other stuff we can try.

### Resources
1. CRSP Monthly Data - We need to ask the professor to share this with us. 
2. Lazy Prices Paper (official here, working paper here). This includes lots of info about steps in the data analysis. 
3. The official page has some poorly documented code in the PERL and Stata languages under “Supporting Information”. These are useful! 
4. Software Repository for Accounting and Finance | University of Notre Dame is Bill McDonald’s resource webpage. 
In addition to all the information there about how he does textual analysis, he has a one-click zip containing Cleaned 10-X Files. The “X” in “10-X” is a placeholder, so this includes 10-Ks, 10-Qs, and associated filings. This file is 50GB zipped and covers 1993 to 2024!
There is a Master Index Data page that contains MasterIndex_Aggregate_10X_1993-2024.txt. This is useful as well. 
