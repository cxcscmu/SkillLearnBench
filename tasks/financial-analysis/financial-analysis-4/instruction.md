You are a financial analyst in hedge fund, your task is to analyze the activities of hedge funds in q3 2025 by compare it with q2 2025. The dataset is downloaded to `/root/2025-q2` and `/root/2025-q3` folders respectively.

Questions to be answered in this task:

1. In Q3, what's the AUM of Pershing Square Capital Management founded by Bill Ackman?

To answer this question, first you need to fuzzy search COVERPAGE using search term "pershing square capital management" and find the best match. This gives you the accession_number.

Then, use this accession_number to obtain fund details including AUM.


2. How many stocks are held by Pershing Square Capital Management?

Similar to question 1, you need to first obtain the accession_number and then analyze the fund details.


3. From Q2 to Q3, what is the top 1 stock that received increased investment by Soros Fund Management, ranked by dollar value increase? Answer stock CUSIP.

First, you need to obtain two accession numbers for Soros Fund Management, one for Q2 and one for Q3 (accession numbers will change in reporting seasons). Next, you need to load the holdings in between two quarters and compare the change of holdings.

4. List top-1 fund manager (name) which has invested Tesla in terms of share value in Q3.

First, you need to search the CUSIP for Tesla and then find out the answer.


Format your answer to the above questions in json file called `answers.json` in `/root` folder, follow the file schema:
```json
{
    "q1_answer": number,
    "q2_answer": number,
    "q3_answer": ["stock_cusip1"],
    "q4_answer": ["fund1"]
}
```
