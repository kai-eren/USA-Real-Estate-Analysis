# USA Real Estate Data Analysis

Analyze 2.2M+ U.S. real estate listings to uncover trends in home price, size, and number of beds, and visualize median home prices and price per square foot by state.


## Workflow
1. Cleaned and processed 2.2M+ real estate listings using SQL.
2. Exported two datasets (`listings_clean.csv` and `median_ppsf_by_state.csv`) for analysis.
3. Performed data analysis and visualization in Python using pandas, Seaborn, and Matplotlib.


## Tools
Python | pandas | SQLAlchemy | Seaborn | Matplotlib | MySQL 



## Files
- `data/` — cleaned CSV datasets  
- `images/` — visualizations  
- `scripts/` — Python analysis scripts  



## Run
```bash
git clone https://github.com/kai-eren/USA-Real-Estate-Analysis.git
pip install -r requirements.txt
python scripts/visualizer.py
```

## Visualizations

### Median Home Price by State
![Median Home Price](images/states%20by%20median%20price.png)

### Top 10 States by Price per Square Foot
![Median Price per Sq Ft](images/states%20by%20median%20sqft.png)

### Pairplot: Price, Beds, and House Size
![3x3 Visualization](images/3x3%20visual.png)


## Key Insights
- Median home prices vary widely between states.
- Positive correlation observed between house size and price, suggesting larger homes tend to command higher prices.
- Price per square foot highlights regional housing market differences.
- Relationships between price, size, and number of beds help understand value trends.



## Author
Kai Eren | MIT License
