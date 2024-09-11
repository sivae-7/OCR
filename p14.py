import re
import json
import pytesseract
from PIL import Image

image_path = './pdfImgaes/2024-FC-EROLLGEN-S22-175-FinalRoll-Revision2-ENG-185-WI-29.png'

image = Image.open(image_path)

ocr_text = pytesseract.image_to_string(image)

cleaned_text = re.sub(r'[^\w\s]', '', ocr_text)

# Updated regex pattern
sections = re.split(r'\n(?=\d{1,4}[\)\.,\s]?\s*)', cleaned_text)

def is_valid_voter(voter):
    return any(voter[key] for key in voter)

def parse_voter_section(section):
    lines = section.split('\n')
    print(lines)
    print(lines)
    if len(lines) <= 5:
        return []

    voter_ids = [voter_id for voter_id in lines[0].split() if len(voter_id) > 3]
    names = [name.strip() for name in lines[1].split("Name") if name.strip()]

    # Handle relation names and types
    relation_text = lines[2]
    relation_names = [rel.strip() for rel in relation_text.replace("Father Name", "").replace("Husband Name", "").replace("Mother Name", "").split("  ") if rel.strip()]
    
    # Determine the relation type (Father, Mother, Husband)
    if "Father Name" in relation_text:
        relation_type = "Father"
    elif "Mother Name" in relation_text:
        relation_type = "Mother"
    elif "Husband Name" in relation_text:
        relation_type = "Husband"
    else:
        relation_type = None  # In case no relation is found

    house_numbers = [hn.strip() for hn in lines[3].replace("House Number", "").replace("Photo", "").split("  ") if hn.strip()]

    age_gender_data = lines[4].split("Age")
    age_gender = [ag.strip().split("Gender") for ag in age_gender_data if ag.strip()]

    voters = []
    for i in range(3):  
        age = age_gender[i][0].strip() if i < len(age_gender) and len(age_gender[i]) > 0 else None
        gender = age_gender[i][1].strip() if i < len(age_gender) and len(age_gender[i]) > 1 else None

        voter = {
            "VoterID": voter_ids[i] if i < len(voter_ids) else None,
            "Name": names[i] if i < len(names) else None,
            "RelationType": relation_type,
            "RelationName": relation_names[i] if i < len(relation_names) else None,
            "HouseNumber": house_numbers[i] if i < len(house_numbers) else None,
            "Age": age,
            "Gender": gender,
        }
        if is_valid_voter(voter):
            voters.append(voter)
    
    return voters

all_voters = []
for section in sections:
    voters = parse_voter_section(section)
    if voters:
        all_voters.extend(voters)

voters_json = json.dumps(all_voters, indent=4)
print(len(all_voters))

with open("./voter_data.json", "w") as file:
    file.write(voters_json)
