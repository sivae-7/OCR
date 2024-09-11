import re

# Raw data
cleaned_text = """
Assembly Constituency No and Name : 175-ORATHANADU. Part No. : 185 Section No and Name 2-Poovathur (R.V) AND (P), North Street wd--2 342 MML6114094 343 MML6114102 344 RRNO453175 Name Ganesan Name Saravanan Name Subha Father Name: Raingaseami Father Name: Raingaseami Husband Name: Saravanan House Number : 307 Photo House Number : 307 Photo House Number : 307 Photo Age : 56 Gender : Male Age 47 Gender : Male Age : 41 Gender : Female 345 MML1506658 346 MML6180020 347 RRNO453183 Name Manimekhalai Name Thirumurugan Name Nathiya Husband Name: Ramasamy Father Name: Ramasamy Husband Name: Thirumurugan House Number : 308 Photo House Number : 308 Photo Photo Age : 67 Gender : Female Age : 45 Gender : Male Age : 59 Gender : Female 348 RRN1006378 349 RRN1462514 350 RRN1462522 Name Manju Name shanmugam Name Vasammal Husband Name: Sivaraman Father Name: Duraisamy House Number : 309 Photo House Number : 309 Photo Photo Age : 39 Gender : Female Age : 71 Gender : Male Age : 59 Gender : Female 361 MML1507839 362 RRN1462548 353 MML1221704 Name Sivaraman Name Sarosa Name Ravikumar Father Name: Shanmugam Husband Name: Ayyavu Father Name: Ayyavu House Number : 309 Photo House Number : 311 Photo House Number : 311 Photo Age : 41 Gender : Male Age : 73 Gender : Female Age : 55 Gender : Male 354 RRNOB86580 355 MML1221720 356 RRN1899913 Name Kurunchivendhan Name Kavitha Name Elakkiya Father Name: Ravikumar Husband Name: Ravikumar Husband Name: poyyamozhi House Number : 311 Photo House Number : 311 Photo House Number 312 Photo Age 25 Gender : Male Age 45 Gender : Female Age : 36 Gender : Female 357 RRN1462555 358 RRN1462563 359 MML1315654 Name Lakshmanan Name Dhanam Name poaiyamozhi Father Name: VEERASAMI Husband Name: Lakshmanan Father Name: Lakshmanan House Number : 312 Photo House Number : 312 Photo House Number : 312 Photo Age :67 Gender : Male Age 60 Gender : Female Age 42 Gender : Male 360 MML1508050 31 RRN1462571 362 MML6114110 Name Kanimoti Name Muthusamy Name Nirmaladevi Father Name: Lakshmanan Father Name: Rangasamy Husband Name: Madhan House Number : 312 Photo House Number : 313 Photo Photo Age 41 Gender : Female Age :97 Gender : Male 363 RRRN1462605 364 RRN1462621 365 RRN1462639 Name Rengasamy Name Adhimoolam Name Ramala Father Name: Appavu Father Name: Rengasamy Husband Name: Aadhimoolam House Number : 314 Photo House Number : 314 Photo House Number : 314 Photo Age : 85 Gender : Male Age : 85 Gender : Male Age 50 Gender : Female 366 RRNO453522 367 RRNO798348 368 RRN1462647 Name Balamurugan Name Athithan Name Kathayi Father Name: Aathimulam Father Name: Athimoolam Husband Name: Rai House Number : 314 Photo House Number 314 Photo Photo Age : 82 Gender : Male Age 26 Gender : Male 369 RRN1462654 370 MML1506948 371 RRN1462662 Name Suryamoorthy Name Jeova Name Manikam Father Name: Rangasamy Husband Name: Ravi Husband Name: Kuppusamy House Number : 315 Photo House Number : 317 Photo House Number : 317 Photo Age :61 Gender : Male Age 52 Gender : Female Age 80 Gender : Female Electoral roll updated on 27-03-2024 w.r.t. 01-01-2024 (qualifying date) Total Pages 32 - Page 15
"""

# Define regex patterns for extracting data
patterns = {
    "voter_id": r"(\d{3} \w{3,}|\d{3} \w{7,})",
    "name": r"Name\s*([^\s]+)",
    "father_name": r"Father Name:\s*([^\s]+)",
    "husband_name": r"Husband Name:\s*([^\s]+)",
    "house_number": r"House Number\s*:\s*(\d+)",
    "age_gender": r"Age\s*:\s*(\d+)\s*Gender\s*:\s*(Male|Female)"
}

# Extract and clean data
def extract_info(text, patterns):
    data = []
    for voter_id in re.findall(patterns["voter_id"], text):
        name_match = re.search(rf"Name\s*([^\s]+)", text)
        name = name_match.group(1) if name_match else ""
        father_name_match = re.search(rf"Father Name:\s*([^\s]+)", text)
        father_name = father_name_match.group(1) if father_name_match else ""
        husband_name_match = re.search(rf"Husband Name:\s*([^\s]+)", text)
        husband_name = husband_name_match.group(1) if husband_name_match else ""
        house_number_match = re.search(rf"House Number\s*:\s*(\d+)", text)
        house_number = house_number_match.group(1) if house_number_match else ""
        age_gender_match = re.search(rf"Age\s*:\s*(\d+)\s*Gender\s*:\s*(Male|Female)", text)
        age_gender = age_gender_match.groups() if age_gender_match else ("", "")
        
        data.append({
            "voter_id": voter_id,
            "name": name,
            "father_name": father_name,
            "husband_name": husband_name,
            "house_number": house_number,
            "age": age_gender[0],
            "gender": age_gender[1]
        })
    return data

# Extracted data
cleaned_data = extract_info(cleaned_text, patterns)

# Print cleaned data for review
for record in cleaned_data:
    print(record)
