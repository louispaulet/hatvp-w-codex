import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ASSET_DIR = 'report_assets'
os.makedirs(ASSET_DIR, exist_ok=True)

# 1. Asset distribution histogram
person_df = pd.read_csv('stock_analysis/output/person_stock_report.csv')
plt.figure(figsize=(8,6))
plt.hist(person_df['total_valuation']/1e6, bins=50, color='steelblue', edgecolor='black')
plt.xlabel('Total valuation (million €)')
plt.ylabel('Number of declarants')
plt.title('Distribution of total valuation among declarants')
plt.tight_layout()
plt.savefig(os.path.join(ASSET_DIR, 'fig1_asset_distribution.png'))
plt.close()

# 2. Sector exposure pie chart
norm_df = pd.read_csv('stock_analysis/output/normalized_stocks.csv')
index_names = set(pd.read_csv('stock_analysis/output/indexes/cac40.csv')['clean_name'])
index_names |= set(pd.read_csv('stock_analysis/output/indexes/sbf120.csv')['clean_name'])
index_names |= set(pd.read_csv('stock_analysis/output/indexes/sp500.csv')['clean_name'])
sector_df = norm_df[norm_df['clean_name'].isin(index_names)].copy()

sector_map = {
    'CREDIT AGRICOLE': 'Finance',
    'BNP PARIBAS': 'Finance',
    'SOCIETE GENERALE': 'Finance',
    'AXA': 'Finance',
    'ENGIE': 'Energy',
    'TOTALENERGIES': 'Energy',
    'EDF': 'Energy',
    'AIR LIQUIDE': 'Industry',
    'VEOLIA': 'Utilities',
    'ORANGE': 'Telecom',
    'SANOFI': 'Healthcare',
    'MICROSOFT': 'Technology',
    'AMAZON': 'Technology',
    'ACCENTURE': 'Technology',
    'KRAFT HEINZ': 'Consumer',
    'LINDE': 'Industry',
}
sector_df['sector'] = sector_df['clean_name'].map(sector_map).fillna('Other')
sector_counts = sector_df.groupby('sector')['evaluation'].sum().sort_values(ascending=False)
plt.figure(figsize=(8,6))
sector_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
plt.ylabel('')
plt.title('Sector exposure of declared holdings')
plt.tight_layout()
plt.savefig(os.path.join(ASSET_DIR, 'fig2_sector_exposure.png'))
plt.close()

# 3. Gender distribution heatmap for spouse occupations
spouse_df = pd.read_csv('spouse_occupation_gender_counts.csv')
spouse_df['total'] = spouse_df['male'] + spouse_df['female']
top = spouse_df.nlargest(10, 'total').set_index('occupation')[['male','female']]
plt.figure(figsize=(8,6))
sns.heatmap(top, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Gender')
plt.ylabel('Spouse occupation')
plt.title('Gender distribution by spouse occupation (top 10)')
plt.tight_layout()
plt.savefig(os.path.join(ASSET_DIR, 'fig3_spouse_gender_heatmap.png'))
plt.close()
