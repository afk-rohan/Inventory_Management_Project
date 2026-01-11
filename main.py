from models.user_manager import UserManager
from models.order_manager import OrderManager
from visualizations import (
    plot_sales_by_state,
    plot_status_distribution,
    plot_sales_by_category,
    plot_sales_trend
)

# Initialize managers
user_manager = UserManager()
order_manager = OrderManager()

# Create users
user_manager.create_user("admin", "123", "Manager")
user_manager.create_user("junior", "123", "Junior Manager")

print("=== Inventory Management & Analytics System ===")

# Login
username = input("Username: ")
password = input("Password: ")

if not user_manager.authenticate(username, password):
    print("Invalid Login")
    exit()

# Load data
order_manager.load_data("data/amazon_sale_report.csv")
print("Orders Loaded:", len(order_manager.orders))

# Main menu loop
while True:
    print("\n1. Search Cancelled Orders")
    print("2. Top 5 Products by Amount")
    print("3. Sales by City")
    print("4. Category Performance")
    print("5. Customer Lifetime Value")
    print("6. Bar Chart: Sales by Ship-State")
    print("7. Pie Chart: Order Status Distribution")
    print("8. Bar Chart: Sales by Category")
    print("9. Line Chart: Sales Trend Over Time")
    print("10. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        orders = order_manager.search_by_status("cancelled")
        for o in orders[:10]:
            print(o)
        print("Total Cancelled Orders:", len(orders))

    elif choice == "2":
        top = order_manager.top_n_by_amount(5)
        for sku, amount in top:
            print("SKU:", sku, "Amount:", amount)

    elif choice == "3":
        city = input("Enter City: ")
        print("Total Sales:", order_manager.sales_by_city(city))

    elif choice == "4":
        data = order_manager.category_performance()
        for cat, val in data.items():
            print(cat, "Amount:", val["amount"], "Qty:", val["qty"])

    elif choice == "5":
        clv_data = order_manager.clv()
        for k in list(clv_data.keys())[:10]:
            print("Order ID:", k, "CLV:", clv_data[k])

    elif choice == "6":
        plot_sales_by_state(order_manager.orders)

    elif choice == "7":
        plot_status_distribution(order_manager.orders)

    elif choice == "8":
        plot_sales_by_category(order_manager.category_performance())

    elif choice == "9":
        plot_sales_trend(order_manager.orders)

    elif choice == "10":
        print("Exiting system...")
        break

    else:
        print("Invalid option. Please try again.")
