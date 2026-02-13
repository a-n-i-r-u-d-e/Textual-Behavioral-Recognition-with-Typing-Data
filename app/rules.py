def is_idle(features):
    if not features:
        return True

    return (
        features.get("typing_speed", 0) == 0
        and features.get("scroll_rate", 0) == 0
        and features.get("idle_ratio", 1.0) > 0.8
    )

def rule_based_confusion(features):
    score = 0
    if features["backspace_rate"] > 0.3:
        score += 1
    if features["pause_count"] >= 2:
        score += 1
    if features["scroll_changes"] >= 4:
        score += 1
    return score >= 2
