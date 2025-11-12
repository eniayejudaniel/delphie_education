import csv

def clean_phone_number(phone):
    phone = phone.strip()
    if phone.startswith("p:"):
        phone = phone.replace("p:", "")
    phone = phone.strip()

    if phone.startswith("p:0"):
        phone = phone.replace("p:0", "+234")

    if phone.startswith("234"):
        phone = "+" + phone

    if phone.startswith("0"):
        phone = "+234" + phone[1:]

    return phone

def process_csv(file_path):
    results = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            email = row.get("email", "").strip()
            full_name = row.get("full_name", "").strip()
            phone_number = clean_phone_number(row.get("phone_number", ""))
            
            results.append({
                "email": email,
                "full_name": full_name,
                "phone_number": phone_number
            })
    return results

# Example usage
file_path = r"C:\Users\USER\delphie_education\src\Delphie Education Facebooks Ads Leads Qualification - Qualify Leads.csv"  # 👈 Replace with your actual file path
data = process_csv(file_path)
print(data)
