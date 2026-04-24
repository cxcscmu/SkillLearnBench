[SKILL]
---
name: calculate_github_pulse_metrics
description: Calculates PR and Issue metrics (counts, average merge times, top contributors) for a given GitHub repository and date range using the gh CLI. Ensures issues and PRs are not mixed by explicitly specifying is:issue and is:pr in searches. Outputs results to a strictly structured JSON file.
---
calculate_github_pulse_metrics() {
    local repo="$1"
    local start_date="$2"
    local end_date="$3"
    local output_file="$4"

    if [ -z "$output_file" ]; then
        echo "Usage: calculate_github_pulse_metrics <repo> <start_date> <end_date>