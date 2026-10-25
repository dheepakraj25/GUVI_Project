
import streamlit as st
import pandas as pd
import mysql.connector

st.title("Uber Eats Restaurant Intelligence System")

def connect_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ubereats"
    )
    return db

def run_query(query):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute(query)
    data = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    result = pd.DataFrame(data, columns=columns)

    cursor.close()
    db.close()

    return result

page = st.sidebar.selectbox("Choose Page",["Dashboard", "Restaurant Q&A", "Order Q&A"])

if page == "Dashboard":

    st.header("Dashboard")

    choice = st.selectbox( "Select Dataset", ["Restaurants", "Orders"] )

    if choice == "Restaurants":
        query = "SELECT * FROM restaurants LIMIT 100"
    else:
        query = "SELECT * FROM orders LIMIT 100"

    result = run_query(query)

    st.dataframe(result, use_container_width=True)

elif page == "Restaurant Q&A":

    st.header("Restaurant Business Questions")

    question = st.selectbox(
        "Choose a Question",
        [
            "1. Top Rated Locations",
            "2. Most Restaurants by Location",
            "3. Online Ordering Analysis",
            "4. Table Booking Analysis",
            "5. Average Rating by Cost",
            "6. Restaurant Pricing Segments",
            "7. Most Common Cuisines",
            "8. Highest Rated Cuisines",
            "9. Niche Cuisines",
            "10. Restaurant Cost Analysis"
        ]
    )

    if st.button("Show Result"):

        if question == "1. Top Rated Locations":
            query = """ SELECT location, AVG(rate) AS average_rating FROM restaurants
                WHERE rate IS NOT NULL GROUP BY location ORDER BY average_rating DESC """

        elif question == "2. Most Restaurants by Location":
            query = """ SELECT location, COUNT(*) AS total_restaurants FROM restaurants
                GROUP BY location ORDER BY total_restaurants DESC """

        elif question == "3. Online Ordering Analysis":
            query = """ SELECT online_order, COUNT(*) AS total_restaurants, AVG(rate) AS average_rating
                FROM restaurants WHERE rate IS NOT NULL GROUP BY online_order """

        elif question == "4. Table Booking Analysis":
            query = """ SELECT book_table, COUNT(*) AS total_restaurants, AVG(rate) AS average_rating
                FROM restaurants WHERE rate IS NOT NULL GROUP BY book_table """

        elif question == "5. Average Rating by Cost":
            query = """ SELECT approx_cost, AVG(rate) AS average_rating
                FROM restaurants WHERE rate IS NOT NULL GROUP BY approx_cost ORDER BY approx_cost """

        elif question == "6. Restaurant Pricing Segments":
            query = """ SELECT CASE WHEN approx_cost < 300 THEN 'Low Cost' WHEN approx_cost <= 700 THEN 'Medium Cost' ELSE 'Premium Cost'
                    END AS pricing_segment, COUNT(*) AS total_restaurants FROM restaurants GROUP BY pricing_segment """

        elif question == "7. Most Common Cuisines":
            query = """ SELECT cuisines, COUNT(*) AS total_restaurants FROM restaurants
                WHERE cuisines IS NOT NULL GROUP BY cuisines ORDER BY total_restaurants DESC LIMIT 10 """

        elif question == "8. Highest Rated Cuisines":
            query = """ SELECT cuisines, AVG(rate) AS average_rating FROM restaurants
                WHERE rate IS NOT NULL GROUP BY cuisines ORDER BY average_rating DESC LIMIT 10 """

        elif question == "9. Niche Cuisines":
            query = """ SELECT cuisines, COUNT(*) AS total_restaurants FROM restaurants WHERE cuisines IS NOT NULL
                GROUP BY cuisines HAVING COUNT(*) <= 10 ORDER BY total_restaurants DESC """

        else:
            query = """ SELECT approx_cost, COUNT(*) AS total_restaurants, AVG(rate) AS average_rating
                FROM restaurants WHERE rate IS NOT NULL GROUP BY approx_cost ORDER BY approx_cost"""

        result = run_query(query)

        st.dataframe(result, use_container_width=True)

else:

    st.header("Order Business Questions")

    question = st.selectbox(
        "Choose a Question",
        [
            "1. Total Orders",
            "2. Total and Average Order Value",
            "3. Most Used Payment Methods",
            "4. Discount Usage Analysis",
            "5. Orders by Pricing Segment"
        ]
    )

    if st.button("Show Order Result"):

        if question == "1. Total Orders":
            query = """ SELECT COUNT(*) AS total_orders FROM orders """

        elif question == "2. Total and Average Order Value":
            query = """ SELECT SUM(order_value) AS total_order_value, AVG(order_value) AS average_order_value FROM orders """

        elif question == "3. Most Used Payment Methods":
            query = """ SELECT payment_method, COUNT(*) AS total_orders FROM orders GROUP BY payment_method ORDER BY total_orders DESC """

        elif question == "4. Discount Usage Analysis":
            query = """SELECT discount_used, COUNT(*) AS total_orders, AVG(order_value) AS average_order_value
                FROM orders GROUP BY discount_used """

        else:
            query = """ SELECT pricing_segment, COUNT(*) AS total_orders,
                       SUM(order_value) AS total_order_value FROM orders GROUP BY pricing_segment """

        result = run_query(query)

        st.dataframe(result, use_container_width=True)
