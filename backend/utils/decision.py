def final_decision(score):
    if score >= 70:
        return "GENUINE"
    elif score >= 40:
        return "SUSPICIOUS"
    else:
        return "FORGED"
