import mysql.connector as mycon

# DB CONNECTION
conn = mycon.connect(
    host="localhost",
    user="root",
    password="abc123",
    database="recommendation_db"
)

cursor = conn.cursor()


# ANALYZER FUNCTION
def analyze_query(query):
    print("\n========== ANALYSIS ==========")

    q = query.lower()
    score = 100
    issues = []
    risk = "LOW"

    # RULES
    if "select *" in q:
        score -= 20
        issues.append(("MEDIUM", "Avoid using SELECT *"))

    if "select" in q and "where" not in q:
        score -= 15
        issues.append(("MEDIUM", "Missing WHERE clause"))

    if "select" in q and "limit" not in q:
        score -= 10
        issues.append(("LOW", "Consider using LIMIT"))

    if "delete" in q and "where" not in q:
        score -= 50
        issues.append(("HIGH", "DELETE without WHERE (dangerous)"))
        risk = "HIGH"

    if "update" in q and "where" not in q:
        score -= 50
        issues.append(("HIGH", "UPDATE without WHERE (dangerous)"))
        risk = "HIGH"

    score = max(score, 0)

    # GRADE
    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    elif score >= 50:
        grade = "C"
    else:
        grade = "D"

    # RISK LEVEL
    if risk != "HIGH" and score < 70:
        risk = "MEDIUM"

    # OUTPUT
    print(f"Score: {score}/100")
    print(f"Grade: {grade}")
    print(f"Risk Level: {risk}")

    if issues:
        print("\nIssues:")
        for severity, issue in issues:
            print(f"[{severity}] {issue}")
    else:
        print("\nQuery looks good")

    print("================================\n")


# MAIN LOOP
while True:
    print("\n===== SQL ANALYZER =====")
    print("1. Analyze Query")
    print("2. View Query History")
    print("3. Show Analytics")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        query = input("\nEnter SQL query: ")

        cursor.execute(
            "INSERT INTO query_history (query_text) VALUES (%s)",
            (query,)
        )
        conn.commit()

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
        print("\n===== ANALYTICS DASHBOARD =====")

        cursor.execute("SELECT query_text FROM query_history")
        rows = cursor.fetchall()

        total = len(rows)
        select_star = 0
        missing_where = 0
        dangerous = 0

        for row in rows:
            q = row[0].lower()

            if "select *" in q:
                select_star += 1

            if "select" in q and "where" not in q:
                missing_where += 1

            if ("delete" in q and "where" not in q) or ("update" in q and "where" not in q):
                dangerous += 1

        print(f"\nTotal Queries: {total}")
        print(f"SELECT * usage: {select_star}")
        print(f"Missing WHERE: {missing_where}")
        print(f"Dangerous Queries: {dangerous}")

        print("================================\n")

    elif choice == "4":
        print("Exiting...")
        break

    else:
        print("Invalid choice. Try again.")
