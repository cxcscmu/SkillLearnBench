---
name: question_processor
description: Use this to ingest the task file and orchestrate the multi-step retrieval and formatting workflow.
---
To execute the task:
1. **Load Data**: Read `/root/question.txt` to parse the question ID and the raw question query.
2. **Process Loop**: For each question, invoke the `enterprise_data_retrieval` skill to get the raw answer data.
3. **Aggregate**: Store results in a local dictionary and calculate tokens for each entry using the logic defined in `answer_formatter_and_tracker`.
4. **Finalize**: Use `answer_formatter_and_tracker` to write the finalized dict to `/root/answer.json`.