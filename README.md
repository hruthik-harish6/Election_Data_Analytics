# Election Data Analytics Dashboard

## Project purpose
This is a beginner-friendly Python data analytics project designed around the IBM SkillsBuild / BharatCares dashboard approach shown in the training: **Data -> Information -> Insight -> Decision -> Action**.

The project is intentionally descriptive and neutral. It does not predict election outcomes or recommend a political choice.

**Important:** The included CSV contains **synthetic educational data** so the project runs immediately. Replace it with the dataset from your Google Sheet before submission, while keeping the required column names or adapting the notebook's column-mapping cell.

## Files
- `Election_Data_Analytics.ipynb` - complete notebook for IBM Bob / Jupyter / VS Code
- `app.py` - optional Streamlit dashboard
- `data/election_data.csv` - runnable sample dataset
- `requirements.txt` - Python dependencies
- `Election_Data_Analytics_Report.docx` - editable project report
- `Election_Data_Analytics_Report.pdf` - final report PDF

## Required dataset columns
`Region, Constituency, Registered_Voters, Votes_Cast, Candidate, Party, Votes_Received, Rank`

## Run in VS Code
1. Open this folder in VS Code.
2. Create/activate a Python environment.
3. Install dependencies:
   `pip install -r requirements.txt`
4. For the notebook, open `Election_Data_Analytics.ipynb` and run all cells.
5. For the dashboard, run:
   `streamlit run app.py`

## Using a Google Sheet
The dashboard can read a Google Sheet **CSV export URL**. In `app.py`, set:

`GOOGLE_SHEET_CSV_URL = 'YOUR_CSV_EXPORT_URL'`

The local sample CSV remains the fallback, so the project still runs if the URL is unavailable.

## Dashboard structure
### Page 1 - Executive Overview
KPIs, party vote totals, and region turnout.

### Page 2 - Party & Region Analysis
Vote totals by region and party plus a winning-candidate table.

### Page 3 - Turnout & Margin Analysis
Turnout by region and winning margins by constituency.

## Project limitations
- Synthetic data is not actual election data.
- Results describe the supplied dataset only.
- No causal or predictive political conclusions are made.
