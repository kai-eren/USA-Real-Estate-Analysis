"""
USA Real Estate Data Analysis 

- Analyze 2.2M+ real estate listings to explore relationships between price, size, and number of beds.
- Visualize median home prices and price per square foot by state.
- Tools: Python, pandas, SQLAlchemy, Seaborn, Matplotlib
"""



from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
load_dotenv()
# ------------------------------
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST", "localhost")
database = os.getenv("DB_NAME")


# ------------------------------
# Connecting to MySQL database
# ------------------------------
engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')


# ------------------------------
# Loading data and export CSVs 
# ------------------------------
df = pd.read_sql("SELECT * FROM listings_clean", engine)
df.to_csv('data/listings_clean.csv', index=False)

df_ppsf = pd.read_sql("SELECT * FROM median_ppsf_by_state", engine)
df_ppsf.to_csv('data/median_ppsf_by_state.csv', index=False)


# ------------------------------
# Convert price to thousands for easier interpretation
# ------------------------------
df['Price (in thousands)'] = df['price'] / 1000


# ------------------------------
# Rename columns for clarity
# ------------------------------
df['House Size (ft^2)'] = df['house_size'] 
df['Number of Beds'] = df['bed'] 


# ------------------------------
# Remove top 5% of Price and House Size as outliers
# ------------------------------
price_cutoff = df['Price (in thousands)'].quantile(0.95)
size_cutoff = df['House Size (ft^2)'].quantile(0.95)


# ------------------------------
# Randomly sample 300 listings for plotting clarity
# ------------------------------
df_sample_filtered = df[(df['Price (in thousands)'] <= price_cutoff) & 
                        (df['House Size (ft^2)'] <= size_cutoff)].sample(n=300, random_state=42)


# ------------------------------
# Pairplot to visualize relationships between Price, Number of Beds, and House Size
# ------------------------------
g = sns.pairplot(df_sample_filtered[['Price (in thousands)', 'Number of Beds', 'House Size (ft^2)']], 
                 diag_kind='kde', 
                 kind='reg', 
                 plot_kws={'ci': None,
        'scatter_kws': {'s': 4, 'alpha': 1, 'edgecolor': 'none'},  
        'line_kws': {'color': '#FF0000', 'alpha': 0.5, 'linewidth': 1} })

colors = ['red', '#FF00FF', 'green', '#544D4D', 'black', '#C0BA03', 'blue', 'orange', 'purple']
axes = g.axes.flatten()


# ------------------------------
# Assign a unique color to each scatter plot for visual clarity
# ------------------------------
for ax, color in zip(axes, colors):
    for collection in ax.collections:
        collection.set_facecolor(color)
    ax.set_xlim(left=0)  
    ax.set_ylim(bottom=0)


# ------------------------------
# Calculate median home price by state
# ------------------------------
median_by_city = df.groupby('state')['price'].median().reset_index()
median_by_city['Price (in thousands)'] = median_by_city['price'] / 1000


# ------------------------------
# Filter for states with at least 10,000 listings for statistical relevance
# Select top 10 states by median price
# ------------------------------
city_counts = df['state'].value_counts()
popular_cities = city_counts[city_counts >= 10000].index  
median_by_city = median_by_city.sort_values('Price (in thousands)', ascending=False).head(10)


# ------------------------------
# Bar chart: Top 10 states by median home price
# 'viridis' palette for color aesthetics
# ------------------------------
plt.figure(figsize=(10, 6))
sns.barplot(data=median_by_city.sort_values('Price (in thousands)', ascending=False),
            x='state', y='Price (in thousands)', palette='viridis')
plt.xticks(rotation=45, ha='right')
plt.title('Median Home Price by State')
plt.xlabel('State')
plt.ylabel('Median Price (in thousands)')
plt.tight_layout()


# ------------------------------
# Bar chart: Top 10 states by median price per square foot
# Rotate x-axis labels and use tight_layout for clean display
# ------------------------------
df_ppsf_top10 = df_ppsf.sort_values('median_ppsf', ascending=False).head(10)
plt.figure(figsize=(10,6))
sns.barplot(
    data=df_ppsf_top10,
    x='state',
    y='median_ppsf',
    hue='state',  
    legend=False,
    palette='hls'
)
plt.title('Top 10 States by Median Price per Square Foot')
plt.xlabel('State')
plt.ylabel('Median Price per Sq Ft ($)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()







