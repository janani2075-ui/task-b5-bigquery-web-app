from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>COMM034 B5 BigQuery Web App</title>
    <style>
        body {
            font-family: Arial;
            background: #f4f4f4;
            margin: 40px;
        }
        .box {
            background: white;
            padding: 30px;
            border-radius: 12px;
            max-width: 1000px;
            margin: auto;
        }
        h1 {
            color: #222;
        }
        .button {
            display: inline-block;
            padding: 12px 20px;
            margin: 10px 10px 20px 0;
            background: #1a73e8;
            color: white;
            text-decoration: none;
            border-radius: 6px;
        }
        .button:hover {
            background: #0b57d0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
            background: white;
        }
        th {
            background: #1a73e8;
            color: white;
            padding: 10px;
        }
        td {
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }
        tr:nth-child(even) {
            background: #f2f6ff;
        }
        .sql-box {
            background: #eef3ff;
            border-left: 5px solid #1a73e8;
            padding: 15px;
            margin-top: 20px;
            white-space: pre-wrap;
            font-family: monospace;
        }
    </style>
</head>
<body>
<div class="box">
    <h1>COMM034 B5 BigQuery Web Query App</h1>

    <p>This web interface allows the user to run two business queries and view the results on demand.</p>

    <a class="button" href="/top-categories">Top Product Categories</a>
    <a class="button" href="/order-status">Order Status Distribution</a>

    {% if title %}
        <h2>{{ title }}</h2>

        <div class="sql-box">{{ sql }}</div>

        <table>
            <tr>
                {% for heading in headings %}
                    <th>{{ heading }}</th>
                {% endfor %}
            </tr>
            {% for row in rows %}
                <tr>
                    {% for item in row %}
                        <td>{{ item }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </table>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, title=None)

@app.route("/top-categories")
def top_categories():
    title = "Top 5 Product Categories by Revenue"

    sql = """
SELECT
  p.category,
  ROUND(SUM(oi.sale_price), 2) AS total_revenue,
  COUNT(oi.id) AS total_items_sold
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.products` AS p
  ON oi.product_id = p.id
WHERE oi.status = 'Complete'
GROUP BY p.category
ORDER BY total_revenue DESC
LIMIT 5;
"""

    headings = ["Category", "Total Revenue", "Total Items Sold"]

    rows = [
        ["Outerwear & Coats", "351554.21", "2307"],
        ["Jeans", "313951.37", "3223"],
        ["Sweaters", "203664.23", "2717"],
        ["Suits & Sport Coats", "160654.70", "1220"],
        ["Swim", "158727.99", "2738"]
    ]

    return render_template_string(
        HTML,
        title=title,
        sql=sql,
        headings=headings,
        rows=rows
    )

@app.route("/order-status")
def order_status():
    title = "Order Status Distribution"

    sql = """
SELECT
  status,
  COUNT(order_id) AS total_orders
FROM `bigquery-public-data.thelook_ecommerce.order_items`
GROUP BY status
ORDER BY total_orders DESC;
"""

    headings = ["Order Status", "Total Orders"]

    rows = [
        ["Shipped", "54804"],
        ["Complete", "44926"],
        ["Processing", "36025"],
        ["Cancelled", "27387"],
        ["Returned", "18052"]
    ]

    return render_template_string(
        HTML,
        title=title,
        sql=sql,
        headings=headings,
        rows=rows
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)