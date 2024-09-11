import json
import re


cleaned_text = """
Assembly Constituency No and Name : 175-ORATHANADU. Part No. : 185
Section No and Name 2-Poovathur (R.V) AND (P), North Street wd--2
342 MML6114094 343 MML6114102 344 RRNO453175
Name Ganesan - Name # Saravanan - Name # Subha -
Father Name: Raingaseami - Father Name: Raingaseami - Husband Name: Saravanan -
House Number : 307 Photo House Number : 307 Photo House Number : 307 Photo
‘Age : 56 Gender : Male ‘Age +47 Gender : Male ‘Age : 41 Gender : Female
Available Available Available
345 MML1506658 346 MML6180020 347 RRNO453183
Name : Manimekhalai - Name : Thirumurugan - Name # Nathiya -
Husband Name: Ramasamy - Father Name: Ramasamy - Husband Name: Thirumurugan -
House Number : 308 Photo House Number : 308 Photo Photo
‘Age : 67 Gender : Female ‘Age : 45 Gender : Male
Available Available Available
348 RRN1006378 349 RRN1462514 350 RRN1462522
Name ? Manju Name = shanmugam - Name : Vasammal -
Husband Name: Sivaraman Father Name: Duraisamy ~
House Number : 309 Photo House Number : 309 Photo Photo
‘Age : 39 Gender : Female ‘Age : 71 Gender : Male ‘Age : 59 Gender : Female
Available Available Available
361 MML1507839 362 RRN1462548 353 MML1221704
Name # Sivaraman - Name : Sarosa - Name # Ravikumar -
Father Name: Shanmugam - Husband Name: Ayyavu - Father Name: Ayyavu -
House Number : 309 Photo House Number #311 Photo House Number :311 Photo
‘Age : 41 Gender : Male Age ! 73 Gender ! Female ‘Age ! 55 Gender : Male
Available Available Available
354 RRNOB86580 355 MML1221720 356 RRN1899913
Name ¢ Kurunchivendhan - Name : Kavitha Name : Elakkiya
Father Name: Ravikumar - Husband Name: Ravikumar -~ Husband Name: poyyamozhi
House Number : 311 Photo House Number :311 Photo House Number 312 Photo
‘Age #25 Gender : Male Age #45 Gender : Female ‘Age : 36 Gender : Female
Available Available Available
357 RRN1462555 358 RRN1462563 359 MML1315654
Name ? Lakshmanan - Name # Dhanam - Name : poaiyamozhi -
Father Name: VEERASAMI - Husband Name: Lakshmanan - Father Name: Lakshmanan -
House Number : 312 Photo House Number : 312 Photo House Number :312 Photo
‘Age :67 Gender : Male ‘Age #60 Gender : Female ‘Age ! 42 Gender ! Male
Available Available Available
360 MML.1508050 31 RRN1462571 362, MML6114110
Name # Kanimoti - Name : Muthusamy - Name  Nirmaladevi -
Father Name: Lakshmanan - Father Name: Rangasamy - Husband Name: Madhan
House Number : 312 Photo House Number : 313 Photo Photo
‘Age 41 Gender : Female ‘Age :97 Gender : Male
Available Available Available
363 RRRN1462605 364 RRN1462621 365 RRN1462639
Name t Rengasamy - Name = Adhimoolam - Name : Ramala -
Father Name: Appavu - Father Name: Rengasamy - Husband Name: Aadhimoolam -
House Number : 314 Photo House Number :314 Photo House Number :314 Photo
‘Age : 85 Gender : Male ‘Age : 85 Gender : Male Age #50 Gender : Female
Available Available Available
366) RRNO453522 367 RRNO798348 368, RRN1462647
Name ? Balamurugan - Name : Athithan - Name : Kathayi -
Father Name: Aathimulam - Father Name: Athimoolam - Husband Name: Rai
House Number : 314 Photo House Number 314 Photo Photo
‘Age : 82 Gender : Male ‘Age #26 Gender : Male
Available Available Available
369 RRN1462654 370 MML1506948 371 RRN1462662
Name : Suryamoorthy ~ Name # Jeova Name # Manikam -
Father Name: Rangasamy - Husband Name: Ravi - Husband Name: Kuppusamy ~
House Number : 315 Photo House Number : 317 Photo House Number 317 Photo
‘Age :61 Gender : Male ‘Age ! 52 Gender : Female ‘Age + 80 Gender : Female
Available Available Available
"""

cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)

sections = re.split(r'\n(?=\d{3}[\)\.,\s]?\s*(MML|RRN|RRRN))', cleaned_text)

def parse_voter_section(section):
    lines = section.split('\n')
    print(len(lines))
    if(len(lines)<=5):
        return []

    voter_ids = [voter_id for voter_id in lines[0].split() if len(voter_id) > 3]

    names = [name.strip() for name in lines[1].split("Name") if name.strip()]

    relation_names = [rel.strip() for rel in lines[2].replace("Father Name", "").replace("Husband Name", "").split("  ") if rel.strip()]

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
            "Relation": relation_names[i] if i < len(relation_names) else None,
            "HouseNumber": house_numbers[i] if i < len(house_numbers) else None,
            "Age": age,
            "Gender": gender,
        }
        voters.append(voter)
    
    return voters

all_voters = []
for section in sections:
    voters = parse_voter_section(section)
    all_voters.extend(voters)

voters_json = json.dumps(all_voters, indent=4)

with open("./voter_data.json", "w") as file:
    file.write(voters_json)


