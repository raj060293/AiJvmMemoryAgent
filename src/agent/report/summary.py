
def build_summary(issues):
    summary = {
        "total_issues" : len(issues),
        "high_confidence" : 0,
        "medium_confidence": 0,
        "risk_level": "LOW"
    }

    for issue in issues:
        if issue.confidence == "High":
            summary["high_confidence"] += 1
        elif issue.confidence == "Medium":
            summary["medium_confidence"] += 1
        else:
            summary["low_confidence"] += 1

    if summary["high_confidence"] > 0:
        summary["risk_level"] = "HIGH"
    elif summary["medium_confidence"] > 0:
        summary["risk_level"] = "MEDIUM"

    return summary