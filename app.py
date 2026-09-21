from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
LOCAL_DATA = BASE_DIR / 'data' / 'election_data.csv'
# Optional: paste a Google Sheets CSV export URL here.
GOOGLE_SHEET_CSV_URL = ''

st.set_page_config(page_title='Election Data Analytics Dashboard', page_icon='📊', layout='wide')

@st.cache_data
def load_data():
    if GOOGLE_SHEET_CSV_URL.strip():
        try:
            df = pd.read_csv(GOOGLE_SHEET_CSV_URL.strip())
            source = 'Google Sheet CSV URL'
        except Exception:
            df = pd.read_csv(LOCAL_DATA)
            source = 'Local sample CSV (Google Sheet load failed)'
    else:
        df = pd.read_csv(LOCAL_DATA)
        source = 'Local sample CSV'

    required = {
        'Region', 'Constituency', 'Registered_Voters', 'Votes_Cast',
        'Candidate', 'Party', 'Votes_Received', 'Rank'
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')

    df['Turnout_Percent'] = (df['Votes_Cast'] / df['Registered_Voters'] * 100).round(2)
    winner_votes = df.groupby('Constituency')['Votes_Received'].transform('max')
    df['Is_Winner'] = df['Votes_Received'].eq(winner_votes)
    df['Winner_Votes'] = winner_votes
    return df, source

try:
    df, source = load_data()
except Exception as exc:
    st.error(str(exc))
    st.stop()

st.title('Election Data Analytics Dashboard')
st.caption('Neutral descriptive analysis for an educational project. The bundled dataset is synthetic and for demonstration only.')

with st.sidebar:
    st.header('Filters')
    regions = st.multiselect('Region', sorted(df['Region'].unique()), default=sorted(df['Region'].unique()))
    parties = st.multiselect('Party', sorted(df['Party'].unique()), default=sorted(df['Party'].unique()))
    filtered = df[df['Region'].isin(regions) & df['Party'].isin(parties)].copy()
    st.info(f'Data source: {source}')

if filtered.empty:
    st.warning('No rows match the selected filters.')
    st.stop()

constituency_votes = filtered.groupby('Constituency', as_index=False).agg(
    Registered_Voters=('Registered_Voters', 'max'),
    Votes_Cast=('Votes_Cast', 'max')
)
constituency_votes['Turnout_Percent'] = constituency_votes['Votes_Cast'] / constituency_votes['Registered_Voters'] * 100
winner = filtered[filtered['Is_Winner']]

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric('Constituencies', f"{filtered['Constituency'].nunique():,}")
k2.metric('Registered voters', f"{constituency_votes['Registered_Voters'].sum():,.0f}")
k3.metric('Votes cast', f"{constituency_votes['Votes_Cast'].sum():,.0f}")
k4.metric('Average turnout', f"{constituency_votes['Turnout_Percent'].mean():.1f}%")
top2 = filtered.groupby('Constituency')['Votes_Received'].apply(lambda s: s.nlargest(2).tolist())
margin_values = [vals[0] - vals[1] for vals in top2 if len(vals) == 2]
avg_margin = sum(margin_values) / len(margin_values) if margin_values else 0
k5.metric('Avg. winning margin', f"{avg_margin:,.0f}")

page = st.radio('Dashboard page', ['1. Executive Overview', '2. Party & Region Analysis', '3. Turnout & Margin Analysis'], horizontal=True)

if page == '1. Executive Overview':
    st.subheader('What is happening?')
    st.bar_chart(filtered[filtered['Is_Winner']].groupby('Party')['Votes_Received'].sum().sort_values(ascending=False))
    col1, col2 = st.columns(2)
    with col1:
        st.write('**Party vote totals**')
        st.dataframe(filtered.groupby('Party')['Votes_Received'].sum().sort_values(ascending=False).rename('Votes'), use_container_width=True)
    with col2:
        st.write('**Region turnout**')
        region_turnout = filtered.groupby('Region').agg(Registered_Voters=('Registered_Voters','sum'), Votes_Cast=('Votes_Cast','sum'))
        region_turnout['Average Turnout %'] = (region_turnout['Votes_Cast'] / region_turnout['Registered_Voters'] * 100).round(2)
        st.dataframe(region_turnout[['Average Turnout %']].sort_values('Average Turnout %'), use_container_width=True)

elif page == '2. Party & Region Analysis':
    st.subheader('How is it changing across groups?')
    party_region = filtered.groupby(['Region', 'Party'], as_index=False)['Votes_Received'].sum()
    st.bar_chart(party_region.pivot(index='Region', columns='Party', values='Votes_Received').fillna(0))
    st.write('**Winning candidate table**')
    show_cols = ['Region', 'Constituency', 'Candidate', 'Party', 'Votes_Received']
    st.dataframe(filtered[filtered['Is_Winner']][show_cols].sort_values(['Region', 'Constituency']), use_container_width=True)

else:
    st.subheader('What could go wrong? Where should attention go?')
    col1, col2 = st.columns(2)
    with col1:
        st.write('**Turnout by region**')
        region_turnout = filtered.groupby('Region').agg(Registered_Voters=('Registered_Voters', 'sum'), Votes_Cast=('Votes_Cast', 'sum'))
        region_turnout['Turnout_Percent'] = region_turnout['Votes_Cast'] / region_turnout['Registered_Voters'] * 100
        st.bar_chart(region_turnout['Turnout_Percent'].sort_values())
    with col2:
        st.write('**Winning margin by constituency**')
        temp = filtered[filtered['Is_Winner']].copy()
        second = filtered.groupby('Constituency')['Votes_Received'].apply(lambda s: s.nlargest(2).iloc[-1]).rename('Runner_Up_Votes')
        temp = temp.merge(second, on='Constituency')
        temp['Margin'] = temp['Votes_Received'] - temp['Runner_Up_Votes']
        st.bar_chart(temp.set_index('Constituency')['Margin'].sort_values())

st.divider()
st.subheader('Recommended action from the analysis')
st.write('Use the dashboard to identify regions requiring deeper data-quality checks or additional segmentation. This project does not make political recommendations.')
