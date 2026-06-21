def classify_question(question):

    q = question.lower()

    if "revenue" in q:
        return "revenue"

    elif "demand" in q:
        return "demand"

    elif "rating" in q:
        return "rating"

    elif "seller" in q:
        return "seller"

    elif "listing" in q:
        return "listing"

    return "unknown"