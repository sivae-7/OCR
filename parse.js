const fs = require('fs');

// This is the OCR output text; replace this with the actual extracted text
const ocrText = fs.readFileSync('./output.txt', 'utf8');

// Split the text by cards using 'Name :' as a delimiter
const cardSections = ocrText.split(/Name\s*:/);

const cardsData = [];

cardSections.forEach((section) => {
  if (section.trim()) {
    const card = {};

    // Extract Name
    const nameMatch = section.match(/^([A-Za-z\s]+)/);
    if (nameMatch) {
      card.name = nameMatch[1].trim();
    }

    // Extract Father or Husband Name
    const relationMatch = section.match(/(Father|Husband) Name\s*:\s*([A-Za-z\s]+)/);
    if (relationMatch) {
      card.relationType = relationMatch[1];
      card.relationName = relationMatch[2].trim();
    }

    // Extract House Number
    const houseMatch = section.match(/House Number\s*:\s*(\d+)/);
    if (houseMatch) {
      card.houseNumber = houseMatch[1];
    }

    // Extract Age
    const ageMatch = section.match(/Age\s*:\s*(\d+)/);
    if (ageMatch) {
      card.age = parseInt(ageMatch[1], 10);
    }

    // Extract Gender
    const genderMatch = section.match(/Gender\s*:\s*(Male|Female)/);
    if (genderMatch) {
      card.gender = genderMatch[1];
    }

    // Extract Voter ID (Usually starts with MML or RRN and is alphanumeric)
    const voterIDMatch = section.match(/\b(MML|RRN)\w+/);
    if (voterIDMatch) {
      card.voterID = voterIDMatch[0];
    }

    // Push only if the card contains valid data
    if (card.name || card.relationName || card.houseNumber || card.age || card.gender) {
      cardsData.push(card);
    }
  }
});

// Save the parsed data as JSON
fs.writeFileSync('parsedData.json', JSON.stringify(cardsData, null, 2));
console.log("Data extraction and parsing completed.");
