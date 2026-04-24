You are a financial analyst in hedge fund, your task is to analyze the activities of hedge funds in q3 2025 by compare it with q2 2025. The dataset is downloaded to `/root/2025-q2` and `/root/2025-q3` folders respectively.

Questions to be answered in this task:

1. In Q3, what's the AUM of Soros Fund Management founded by George Soros?

To answer this question, first you need to fuzzy search COVERPAGE using search term "soros fund management" and find the best match. This gives you the accession_number.

Then, use this accession_number to obtain fund details including AUM.


2. From Q2 to Q3, what are the top 3 stocks that received increased investment by Pershing Square Capital Management, ranked by dollar value increase? Answer stock CUSIPs.

First, you need to obtain two accession numbers for Pershing Square Capital Management, one for Q2 and one for Q3 (accession numbers will change in reporting seasons). Next, you need to load the holdings in between two quarters and compare the change of holdings.

3. List top-5 fund managers (name) which have invested NVIDIA in terms of share value in Q3.

First, you need to search the CUSIP for NVIDIA and then find out the answer.


Format your answer to the above questions in json file called `answers.json` in `/root` folder, follow the file schema:
```json
{
    "q1_answer": number,
    "q2_answer": ["stock_cusip1", "stock_cusip2", "stock_cusip3"],
    "q3_answer": ["fund1", "fund2", "fund3", "fund4", "fund5"]
}
```
