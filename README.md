README.md
# Avg Gross Margin Analysis

## Project Overview

This project analyzes average gross margin performance using sample sales and cost data. It combines finance analytics with light data quality validation to show how margin reporting can be made more reliable before insights are shared with business leaders.

The project calculates gross margin dollars, gross margin percentage, and average gross margin by product, customer, region, and month. It also flags records or segments that may require review, such as missing revenue, missing cost, negative margin, or unusually low margin performance.

## Business Purpose

Gross margin is a core profitability measure, but margin reporting is only useful when the underlying revenue and cost data are complete, consistent, and explainable.

This project demonstrates a practical finance workflow:

- Validate sales and cost data before analysis
- Calculate gross margin and gross margin percentage
- Summarize average margin performance across business dimensions
- Identify low-margin or negative-margin observations
- Produce outputs that can support FP&A, pricing, operational review, or executive reporting

## Key Questions Answered

- What is the overall average gross margin?
- Which products have the strongest or weakest margin performance?
- Which customers or regions show margin pressure?
- Are there records with missing, negative, or questionable financial values?
- Where should Finance focus further review before making decisions?

## Dataset

The project uses a sample CSV file with sales transaction data.

Expected fields include:

| Field | Description |
|---|---|
| transaction_id | Unique transaction identifier |
| transaction_date | Date of sale |
| customer | Customer name |
| product | Product or product category |
| region | Sales region |
| revenue | Sales revenue |
| cost_of_goods_sold | Direct cost associated with the sale |

## Calculated Metrics

| Metric | Formula |
|---|---|
| Gross Margin Dollars | revenue - cost_of_goods_sold |
| Gross Margin % | gross_margin_dollars / revenue |
| Average Gross Margin % | average of gross_margin_pct across a selected group |

## Data Quality Checks

The project includes basic validation checks for:

- Missing transaction IDs
- Duplicate transaction IDs
- Missing revenue or cost values
- Revenue less than or equal to zero
- Cost less than zero
- Negative gross margin
- Very low gross margin percentage

## Planned Outputs

The project will produce:

| Output | Purpose |
|---|---|
| gross_margin_summary.csv | Summary of average gross margin by business dimension |
| data_quality_issues.csv | Records requiring review before reporting |
| margin_flags.csv | Transactions or segments with low or negative margin |

## Why This Matters

Average gross margin analysis helps Finance and business leaders identify where profitability is strong, weak, or deteriorating. Adding data quality checks makes the analysis more reliable by separating true business signals from potential input issues.

This mirrors real-world finance transformation work where reporting integrity, operational insight, and decision readiness all matter.

## Status

Completed
