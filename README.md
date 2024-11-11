
# Customer Retention and Similarity Analysis

This repository contains a Python-based project for analyzing customer behavior, retention rates, and order similarity in a retail or e-commerce platform. It uses database querying, statistical analysis, and visualization tools to derive insights.

## Features

- **Database Interaction**:
  - Securely connects to a PostgreSQL database via SSH tunneling.
  - Executes complex SQL queries to retrieve customer and order data.

- **Customer Retention Analysis**:
  - Computes retention rates over time based on customer activity.
  - Visualizes retention trends using line charts.

- **Order Similarity Detection**:
  - Identifies similarities between customer orders based on shared items.
  - Uses pandas and SQL to analyze order histories and detect patterns.

- **Visualization**:
  - Generates clear and professional plots for customer retention and similarity metrics.

## Dependencies

- `pandas`
- `psycopg2`
- `matplotlib`
- `sshtunnel`

Install dependencies using pip:
```bash
pip install pandas psycopg2 matplotlib sshtunnel
```

## File Structure

- `main.py`: Main script for database interaction and customer analysis.
- `Similarity.py`: Contains functions for computing order similarity and retention metrics.

## Usage

1. **Database Connection**:
   - Configure your database credentials in `main.py` and `Similarity.py` using environment variables for security.
   - Ensure SSH tunneling is set up to connect to the database.

2. **Run the Analysis**:
   - Use `main.py` to perform customer retention analysis.
   - Use `Similarity.py` to compute similarity scores and visualize results.

3. **Example Commands**:
   Run the main script:
   ```bash
   python main.py
   ```
   Run similarity analysis:
   ```bash
   python Similarity.py
   ```

## Visualization

- **Retention Plots**:
  - Shows customer retention trends over time.
- **Similarity Metrics**:
  - Displays similarity rates between customer orders as a percentage.

## Future Scope

- Add functionality for dynamic parameter tuning in similarity analysis.
- Expand to include more visualizations, such as heatmaps for item co-occurrence.

