import sqlite3

# Task 1: Complex JOINs with Aggregation
conn= sqlite3.connect('../db/lesson.db')
cursor = conn.cursor()

sql = """
SELECT
    o.order_id,
    SUM(p.price * li.quantity) AS total_price
FROM
    orders o
JOIN
    line_items li ON o.order_id = li.order_id
JOIN
    products p ON li.product_id = p.product_id
GROUP BY
    o.order_id
ORDER BY
    o.order_id
LIMIT 5;
"""
cursor.execute(sql)
results=cursor.fetchall()

print('order Id | total price')
print('-----------')
for order_id, total_price in results:
    print(f"{order_id:<8} | ${total_price:.2f}")



# Task 2: Understanding Subqueries
sql_avg_order= """
SELECT
    c.customer_name,
    AVG(order_totals.total_price) AS average_total_price
FROM
    customers c
LEFT JOIN (
    SELECT
        o.customer_id AS customer_id_b,
        o.order_id,
        SUM(p.price * li.quantity) AS total_price
    FROM
        orders o
    JOIN
        line_items li ON o.order_id = li.order_id
    JOIN
        products p ON li.product_id = p.product_id
    GROUP BY
        o.order_id
) AS order_totals ON c.customer_id = order_totals.customer_id_b
GROUP BY
    c.customer_id;
    """
cursor.execute(sql_avg_order)
avg_results= cursor.fetchall()
print("\nCustomer Name | Average Total Order Price")
print("------------------------------------------")
for name, avg_price in avg_results:
    if avg_price is not None:
        print(f"{name:<14} | ${avg_price:.2f}")
    else:
        print(f"{name:<14} | $0.00")


# Task 3: An Insert Transaction Based on Data
conn.execute("PRAGMA foreign_keys = 1")

try:
    conn.execute("BEGIN")
    cursor.execute("SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons'")
    customer_id_row = cursor.fetchone()
    if not customer_id_row:
        raise Exception("Customer 'Perez and Sons' not found.")
    customer_id = customer_id_row[0]

    cursor.execute("SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris'")
    employee_id_row= cursor.fetchone()
    if not employee_id_row:
        raise Exception("Employee 'Miranda Harris' not found.")
    employee_id= employee_id_row[0]

    cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
    product_ids = [row[0] for row in cursor.fetchall()]
    if len(product_ids) < 5:
        raise Exception("Not enough products in database.")

    cursor.execute("""
        INSERT INTO orders (customer_id, employee_id, date)
        VALUES (?, ?, DATE('now'))
        RETURNING order_id
    """, (customer_id, employee_id))
    order_id_row = cursor.fetchone()
    order_id = order_id_row[0]
    for product_id in product_ids:
        cursor.execute("""
            INSERT INTO line_items (order_id, product_id, quantity)
            VALUES (?, ?, 10)
        """, (order_id, product_id))
    conn.commit()

    cursor.execute("""
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
        WHERE li.order_id = ?
    """, (order_id,))
    results = cursor.fetchall()

    print("\nLine Item ID | Quantity | Product Name")
    print("----------------------------------------")
    for line_item_id, quantity, product_name in results:
        print(f"{line_item_id:<13} | {quantity:<8} | {product_name}")

except Exception as e:
    conn.rollback()
    print("Transaction failed:", e)

# Task 4: Aggregation with HAVING
sql_employees_with_orders = """
SELECT
    e.employee_id,
    e.first_name,
    e.last_name,
    COUNT(o.order_id) AS order_count
FROM
    employees e
JOIN
    orders o ON e.employee_id = o.employee_id
GROUP BY
    e.employee_id
HAVING
    COUNT(o.order_id) > 5;
"""

cursor.execute(sql_employees_with_orders)
employee_results = cursor.fetchall()

print("\nEmployees with More Than 5 Orders")
print("-----------------------------------")
print("ID   | First Name     | Last Name      | Order Count")
print("-----|----------------|----------------|-------------")
for emp_id, first, last, count in employee_results:
    print(f"{emp_id:<4} | {first:<14} | {last:<14} | {count}")



conn.close()