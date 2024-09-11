import re
import json

cleaned_text = """
Assembly Constituency No and Name : 175-ORATHANADU. Part No. : 185 Section No and Name 2-Poovathur (R.V) AND (P), North Street wd--2 342 MML6114094 343 MML6114102 344 RRNO453175 Name Ganesan - Name # Saravanan - Name # Subha - Father Name: Raingaseami - Father Name: Raingaseami - Husband Name: Saravanan - House Number : 307 Photo House Number : 307 Photo House Number : 307 Photo ‘Age : 56 Gender : Male ‘Age +47 Gender : Male ‘Age : 41 Gender : Female Available Available Available 345 MML1506658 346 MML6180020 347 RRNO453183 Name : Manimekhalai - Name : Thirumurugan - Name # Nathiya - Husband Name: Ramasamy - Father Name: Ramasamy - Husband Name: Thirumurugan - House Number : 308 Photo House Number : 308 Photo Photo ‘Age : 67 Gender : Female ‘Age : 45 Gender : Male Available Available Available 348 RRN1006378 349 RRN1462514 350 RRN1462522 Name ? Manju Name = shanmugam - Name : Vasammal - Husband Name: Sivaraman Father Name: Duraisamy ~ House Number : 309 Photo House Number : 309 Photo Photo ‘Age : 39 Gender : Female ‘Age : 71 Gender : Male ‘Age : 59 Gender : Female Available Available Available 361 MML1507839 362 RRN1462548 353 MML1221704 Name # Sivaraman - Name : Sarosa - Name # Ravikumar - Father Name: Shanmugam - Husband Name: Ayyavu - Father Name: Ayyavu - House Number : 309 Photo House Number #311 Photo House Number :311 Photo ‘Age : 41 Gender : Male Age ! 73 Gender ! Female ‘Age ! 55 Gender : Male Available Available Available 354 RRNOB86580 355 MML1221720 356 RRN1899913 Name ¢ Kurunchivendhan - Name : Kavitha Name : Elakkiya Father Name: Ravikumar - Husband Name: Ravikumar -~ Husband Name: poyyamozhi House Number : 311 Photo House Number :311 Photo House Number 312 Photo ‘Age #25 Gender : Male Age #45 Gender : Female ‘Age : 36 Gender : Female Available Available Available 357 RRN1462555 358 RRN1462563 359 MML1315654 Name ? Lakshmanan - Name # Dhanam - Name : poaiyamozhi - Father Name: VEERASAMI - Husband Name: Lakshmanan - Father Name: Lakshmanan - House Number : 312 Photo House Number : 312 Photo House Number :312 Photo ‘Age :67 Gender : Male ‘Age #60 Gender : Female ‘Age ! 42 Gender ! Male Available Available Available 360 MML.1508050 31 RRN1462571 362, MML6114110 Name # Kanimoti - Name : Muthusamy - Name Nirmaladevi - Father Name: Lakshmanan - Father Name: Rangasamy - Husband Name: Madhan House Number : 312 Photo House Number : 313 Photo Photo ‘Age 41 Gender : Female ‘Age :97 Gender : Male Available Available Available 363 RRRN1462605 364 RRN1462621 365 RRN1462639 Name t Rengasamy - Name = Adhimoolam - Name : Ramala - Father Name: Appavu - Father Name: Rengasamy - Husband Name: Aadhimoolam - House Number : 314 Photo House Number :314 Photo House Number :314 Photo ‘Age : 85 Gender : Male ‘Age : 85 Gender : Male Age #50 Gender : Female Available Available Available 366) RRNO453522 367 RRNO798348 368, RRN1462647 Name ? Balamurugan - Name : Athithan - Name : Kathayi - Father Name: Aathimulam - Father Name: Athimoolam - Husband Name: Rai House Number : 314 Photo House Number 314 Photo Photo ‘Age : 82 Gender : Male ‘Age #26 Gender : Male Available Available Available 369 RRN1462654 370 MML1506948 371 RRN1462662 Name : Suryamoorthy ~ Name # Jeova Name # Manikam - Father Name: Rangasamy - Husband Name: Ravi - Husband Name: Kuppusamy ~ House Number : 315 Photo House Number : 317 Photo House Number 317 Photo ‘Age :61 Gender : Male ‘Age ! 52 Gender : Female ‘Age + 80 Gender : Female Available Available Available Electoral roll updated on 27-03-2024 w.r.t. 01-01-2024 (qualifying date) Total Pages 32 - Page 15
"""

patterns = {
    'voter_id': r'\b(MML\d{7,8}|RRN\d{6,8})\b',
    'name': r'Name\s*[:#]*\s*([\w\s]+)',
    'father_husband_name': r'(Father|Husband)\s*Name\s*[:#]*\s*([\w\s]+)',
    'house_number': r'House\s*Number\s*[:#]*\s*(\d+)',
    'age': r'Age\s*[:#]*\s*(\d+)',
    'gender': r'Gender\s*[:#]*\s*(\w+)'
}

voters = []

sections = re.split(r'\n(?=\d{3}\s(MML|RRN))', cleaned_text)

for section in sections:
    section_data = {
        'voter_id': re.findall(patterns['voter_id'], section),
        'names': re.findall(patterns['name'], section),
        'father_husband_names': re.findall(patterns['father_husband_name'], section),
        'house_numbers': re.findall(patterns['house_number'], section),
        'ages': re.findall(patterns['age'], section),
        'genders': re.findall(patterns['gender'], section)
    }
    
    for i in range(len(section_data['voter_id'])):
        voter = {
            'voter_id': section_data['voter_id'][i],
            'name': section_data['names'][i] if i < len(section_data['names']) else None,
            'father_husband_name': section_data['father_husband_names'][i] if i < len(section_data['father_husband_names']) else None,
            'house_number': section_data['house_numbers'][i] if i < len(section_data['house_numbers']) else None,
            'age': section_data['ages'][i] if i < len(section_data['ages']) else None,
            'gender': section_data['genders'][i] if i < len(section_data['genders']) else None
        }
        voters.append(voter)

with open('voter_data.json', 'w') as f:
    json.dump(voters, f, indent=4)

print("Voter data extracted and saved to 'voter_data.json'")











