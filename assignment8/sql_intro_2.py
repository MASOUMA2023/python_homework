import sqlite3
import pandas as pd
import os

db_path = os.path.join("..", "db", "lesson.db")

conn = sqlite3.connect(db_path)

query = '''
SELECT 
    line_items.line_item_id,
    line_items.quantity,
    line_items.product_id,
    products.product_name,
    products.price
FROM line_items
JOIN products ON line_items.product_id = products.product_id
'''

df = pd.read_sql_query(query, conn)
print("\n--- Initial DataFrame ---")
print(df.head())

df['total'] = df['quantity'] * df['price']
print("\n--- DataFrame with Total Column ---")
print(df.head())

summary_df = df.groupby('product_id').agg({
    'line_item_id': 'count',
    'total': 'sum',
    'product_name': 'first'
}).rename(columns={'line_item_id': 'order_count'})

summary_df = summary_df.sort_values('product_name')
print("\n--- Summary DataFrame ---")
print(summary_df.head())


summary_path = os.path.join("order_summary.csv")
summary_df.to_csv(summary_path)

print(f"\nSummary written to {summary_path}")