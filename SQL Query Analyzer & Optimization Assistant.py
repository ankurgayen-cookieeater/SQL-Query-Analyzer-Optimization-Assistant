def analyze_query(query):
    print("\n\n========== ANALYSIS ==========")

    q = query.lower()
    score = 100
    issues = []
    risk = "LOW"

    #RULES
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

    #FINAL SCORE
    score = max(score, 0)

    #GRADE SYSTEM
    if score >= 90:
        grade = "A"
    elif score >= 75:
        grade = "B"
    elif score >= 50:
        grade = "C"
    else:
        grade = "D"

    #RISK LEVEL
    if risk != "HIGH" and score < 70:
        risk = "MEDIUM"

    #OUTPUT
    print(f"\nScore: {score}/100")
    print(f"Grade: {grade}")
    print(f"Risk Level: {risk}")

    if issues:
        print("\nIssues:")
        for severity, issue in issues:
            print(f"[{severity}] {issue}")
    else:
        print("\nQuery looks good!")

    print("================================\n")
        print("Invalid choice. Try again.")
