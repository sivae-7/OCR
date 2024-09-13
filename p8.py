import re
import json
import pytesseract
from PIL import Image
import os

folder_path = './images'

def is_valid_voter(voter):
    if voter.get('VoterID'):
        return any(voter[key] for key in voter)
    return False

def parse_voter_section(section, part_No, ward_No, constituency_Name, section_Name):
    lines = section.split('\n')
    if len(lines) <= 5:
        return []

    voter_ids = [voter_id for voter_id in lines[0].split() if len(voter_id) > 3]
    names = [name.strip() for name in lines[1].split("Name") if name.strip()]

    relation_text = lines[2]
    relation_names = [rel.strip() for rel in relation_text.replace("Father Name", "").replace("Husband Name", "").replace("Mother Name", "").replace("Other", "").split("  ") if rel.strip()]
    
    if "Father Name" in relation_text:
        relation_type = "Father"
    elif "Mother Name" in relation_text:
        relation_type = "Mother"
    elif "Husband Name" in relation_text:
        relation_type = "Husband"
    else:
        relation_type = "Other"  

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
            "SectionName" : section_Name,
            "WardNo" : ward_No,
            "PartNO" : part_No,
            "constituencyName" : constituency_Name
                            }
        if is_valid_voter(voter):
            voters.append(voter)
    
    return voters


all_voters = []
i=1
j=0
for filename in os.listdir(folder_path):
    print(i, "  ",filename)
    i=i+1
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)

        ocr_text = pytesseract.image_to_string(image)

        cleaned_text = re.sub(r'[^\w\s]', '', ocr_text)
        sections = re.split(r'\n(?=\d{1,4}[\)\.,\s]?\s*)', cleaned_text)

        header = list(filter(lambda x: x.strip(), (sections[0]).split('\n')))
        header_text = ' '.join(header)
        numbers = re.findall(r'\d+', header_text)
        numbers = [int(num) for num in numbers]
        constituency_No = numbers[0]
        part_No = numbers[1]
        ward_No = ""
        if(len(numbers)>2):
            ward_No = numbers[3]
            

        def process_first_string(text):
            text = re.sub(r'Assembly Constituency No and Name\s*|\s*Part No\s*\d+', '', text)
            text = re.sub(r'\d+', '', text)
            return text.strip()

        def process_second_string(text):
            text = re.sub(r'Section No and Name\s*|\s*wd\d*|\s*WARD NO\s*\d*', '', text)
            text = re.sub(r'\d+', '', text)
            return text.strip()

        constituency_Name = process_first_string(header[0])
        section_Name = ""
        if(len(numbers) > 2):
            section_Name = process_second_string(header[1])

        subSections = re.split(r'\n(?=\w{1,4}\s+\w{1,4}\d{6,9}[\)\.,\s]?\s*)', sections[0])
        if(len(subSections)>1):
            sections.append(subSections[1])
        sections = sections[1:]
        # sections[0] = re.sub(r'\s+', ' ', sections[0]).strip()
        for section in sections:
            if(len(section)>500):
                subSections = re.split(r'\n(?=\w{1,4}\s+\w{1,4}\d{6,9}[\)\.,\s]?\s*)', section)
                if len(subSections)==1:
                    subSections = re.split(r'\n(?=(RRNO|FRNO|RRN)[\)\.,\s]?\s*)', section)
                for subSection in subSections:
                    if(len(subSection)>100 and subSection != subSections[0]):
                        sections.append(subSection)

            pattern = r'^\s*(\d{1,4}|\w{1,4})\s+'
            section = re.sub(pattern, '', section)
            voters = parse_voter_section(section, part_No, ward_No, constituency_No, section_Name)
            if voters:  
                all_voters.extend(voters)
        print("------",len(all_voters)-j)
        j=len(all_voters)
voters_json = json.dumps(all_voters, indent=4)
print(f"Total voters extracted: {len(all_voters)}")

with open("./voter_data.json", "w") as file:
    file.write(voters_json)

print("Voter data extracted and saved to 'voter_data.json'.")
