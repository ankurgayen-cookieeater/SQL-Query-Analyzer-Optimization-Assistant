import mysql.connector as mycon

# --- DB CONNECTION ---
conn = mycon.connect(
    host="localhost",
    user="root",
    password="abc123",
    database="recommendation_db"
)

cursor = conn.cursor()


# --- ANALYZER FUNCTION ---
def analyze_query(query):
    print("\n\n========== ANALYSIS ==========")   # 🔥 CLEAR SEPARATOR

    q = query.lower()
    score = 100
    issues = []
    risk = "LOW"

    if "select *" in q:
        score -= 20
        issues.append("Avoid using SELECT *")

    if "select" in q and "where" not in q:
        score -= 15
        issues.append("Missing WHERE clause")

    if "select" in q and "limit" not in q:
        score -= 10
        issues.append("Consider using LIMIT")

    if "delete" in q and "where" not in q:
        score -= 50
        issues.append("DELETE without WHERE (dangerous)")
        risk = "HIGH"

    if "update" in q and "where" not in q:
        score -= 50
        issues.append("UPDATE without WHERE (dangerous)")
        risk = "HIGH"

    if risk != "HIGH" and score < 70:
        risk = "MEDIUM"

    score = max(score, 0)

    print(f"\nScore: {score}/100")
    print(f"Risk Level: {risk}")

    if issues:
        print("\nIssues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("\n✅ Query looks good!")

    print("================================\n")


# --- MAIN MENU ---
while True:
    print("\n===== SQL ANALYZER =====")
    print("1. Analyze Query")
    print("2. View Query History")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        query = input("\nEnter SQL query: ")

        # Store query in DB
        cursor.execute(
            "INSERT INTO query_history (query_text) VALUES (%s)",
            (query,)
        )
        conn.commit()

        # Analyze query
        analyze_query(query)

    elif choice == "2":
        print("\n--- QUERY HISTORY ---")
        cursor.execute("SELECT * FROM query_history")

        rows = cursor.fetchall()

        for row in rows:
            id, query_text, time = row
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{id}. {query_text} | {formatted_time}")

    elif choice == "3":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Try again.")