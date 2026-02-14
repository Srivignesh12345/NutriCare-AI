def get_diet_rules(risk, bs, systolicbp):
    rules = {
        "avoid": [],
        "prefer": []
    }

    if bs > 7.8:  # High blood sugar
        rules["avoid"].append("High Sugar Foods")
        rules["prefer"].append("Low Glycemic Foods")

    if systolicbp > 130:
        rules["avoid"].append("High Sodium Foods")
        rules["prefer"].append("Potassium Rich Foods")

    if risk == "High":
        rules["prefer"].append("Iron Rich Foods")

    return rules
