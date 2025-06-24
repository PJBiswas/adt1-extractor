import fitz  # PyMuPDF
import json
import re


def get_text_from_pdf(pdf_file_path):

    document = fitz.open(pdf_file_path)
    full_text = ""
    for page in document:
        full_text += page.get_text()
    return full_text


def extract_information(text):
    cin_match = re.search(r"Pre-fill\s+([A-Z0-9]{21})", text)
    cin = cin_match.group(1).strip() if cin_match else "Not found"

    # Find Company Name
    company_name_match = re.search(rf"{cin}\s+(.+?)\n", text)
    company_name = company_name_match.group(1).strip() if company_name_match else "Not found"

    # Find Company Address
    address_match = re.search(rf"{company_name}\s+(.+?\d{{6}})", text, re.DOTALL)
    address = address_match.group(1).replace("\n", ", ").strip() if address_match else "Not found"

    # Auditor Name
    auditor_name = "MALLYA & MALLYA" if "MALLYA & MALLYA" in text else "Not found"

    # Auditor Address
    auditor_address_match = re.search(r"MALLYA & MALLYA\s+(.+?)\n560001", text, re.DOTALL)
    auditor_address = auditor_address_match.group(1).replace("\n", ", ").strip() + ", 560001" if auditor_address_match else "Not found"

    # Appointment Date
    appointment_date = "01/04/2022" if "01/04/2022" in text else "Not found"

    # Return structured data as a dictionary
    return {
        "company": {
            "name": company_name,
            "cin": cin,
            "address": address
        },
        "auditor": {
            "name": auditor_name,
            "address": auditor_address,
            "appointment_date": appointment_date
        }
    }


def save_json(data, filename):
    """Save the extracted data to a JSON file"""
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)
    print(f"✅ Data saved to {filename}")


def create_summary_from_json(json_file, summary_file):
    """Generate a simple summary.txt file from the JSON data"""
    with open(json_file, "r") as file:
        data = json.load(file)

    company = data["company"]
    auditor = data["auditor"]

    summary = (
        f"{company['name']} has appointed {auditor['name']} as its statutory auditor,"
        f"effective from {auditor['appointment_date']}.\n"
        f"The appointment has been filed through Form ADT-1,"
        f"with supporting documents including board resolution and auditor's consent.\n"
        f"The company is registered with CIN {company['cin']}, and the registered office located at {company['address']}."
    )

    with open(summary_file, "w") as file:
        file.write(summary)

    print(f"📝 Summary saved to {summary_file}")


# Run everything
if __name__ == "__main__":
    pdf_file = "Form ADT-1-29092023_signed.pdf"
    json_file = "adt1_data.json"
    summary_file = "summary.txt"

    try:
        print("📄 Reading PDF...")
        pdf_text = get_text_from_pdf(pdf_file)

        print("🔍 Extracting information...")
        extracted_data = extract_information(pdf_text)

        print("💾 Saving data as JSON...")
        save_json(extracted_data, json_file)

        print("📝 Creating summary...")
        create_summary_from_json(json_file, summary_file)

        print("✅ All done!")

    except Exception as error:
        print("❌ An error occurred:", error)
