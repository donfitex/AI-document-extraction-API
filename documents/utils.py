import re
from datetime import datetime

def extract_structured_data(text):
    data = {}

    # 💰 Extract amount (₦, $, etc.)
    amount_match = re.search(r"(₦|\$)?\s?(\d{1,3}(?:[,]\d{3})*(?:\.\d{2})?)", text)
    if amount_match:
        data["amount"] = amount_match.group(2).replace(",", "")
        data["currency"] = amount_match.group(1) or "NGN"

    # 📅 Extract date
    date_match = re.search(r"(\d{2}[/-]\d{2}[/-]\d{4})", text)
    if date_match:
        try:
            parsed_date = datetime.strptime(date_match.group(1), "%d/%m/%Y")
            data["date"] = parsed_date.strftime("%Y-%m-%d")
        except:
            data["date"] = date_match.group(1)

    return data