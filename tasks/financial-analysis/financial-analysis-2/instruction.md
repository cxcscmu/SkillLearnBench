You are a financial analyst in hedge fund, your task is to analyze the activities of hedge funds in q3 2025 by compare it with q2 2025. The dataset is downloaded to `/root/2025-q2` and `/root/2025-q3` folders respectively.

Questions to be answered in this task:

1. In Q3, what's the AUM of Bridgewater Associates founded by Ray Dalio?

To answer this question, first you need to fuzzy search COVERPAGE using search term "bridgewater associates" and find the best match. This gives you the accession_number.

Then, use this accession_number to obtain fund details including AUM.


2. How many stocks are held by Bridgewater Associates?

Similar to question 1, you need to first obtain the accession_number and then analyze the fund details.


3. From Q2 to Q3, what are the top 5 stocks that received increased investment by George Soros's Soros Fund Management, ranked by dollar value increase? Answer stock CUSIPs.

First, you need to obtain two accession numbers for Soros Fund Management, one for Q2 and one for Q3 (accession numbers will change in reporting seasons). Next, you need to load the holdings in between two quarters and compare the change of holdings.

4. List top-3 fund managers (name) which have invested Palantir in terms of share value in Q3.

First, you need to search the CUSIP for Palantir and then find out the answer.


Format your answer to the above questions in json file called `answers.json` in `/root` folder, follow the file schema:
```json
{
    "q1_answer": number,
    "q2_answer": number,
    "q3_answer": ["stock_cusip1", "stock_cusip2", "stock_cusip3", "stock_cusip4", "stock_cusip5"],
    "q4_answer": ["fund1", "fund2", "fund3"]
}
```
