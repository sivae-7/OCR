
//   const Tesseract = require('tesseract.js');
  
//   Tesseract.recognize(
//     '/home/shiva/Documents/OCR/images/2024-FC-EROLLGEN-S22-175-FinalRoll-Revision2-ENG-185-WI (1)-03.png',
//     'eng',
//     {
//       logger: info => console.log(info) // Log progress
//     }
//   ).then(({ data: { text } }) => {
//     console.log(text); // The extracted text will be logged here
//   });









const fs = require('fs');
const path = require('path');
const Tesseract = require('tesseract.js');

const imagesDir = path.join(__dirname, './images'); 

const extractTextFromImage = (imagePath) => {
  return Tesseract.recognize(imagePath, 'eng', {
    logger: info => console.log(info) 
  }).then(({ data: { text } }) => {
    console.log(`Extracted text from ${path.basename(imagePath)}:\n${text}`);
  }).catch(err => {
    console.error(`Error processing ${path.basename(imagePath)}:`, err);
  });
};
33
const processImages = () => {
  fs.readdir(imagesDir, (err, files) => {
    if (err) {
      console.error('Error reading directory:', err);
      return;
    }

    files.forEach(file => {
      const filePath = path.join(imagesDir, file);
      const fileExt = path.extname(file).toLowerCase();

      if (fileExt === '.png' || fileExt === '.jpg' || fileExt === '.jpeg') {
        extractTextFromImage(filePath);
      }
    });
  });
};

processImages();








// const fs = require('fs');
// const path = require('path');
// const Tesseract = require('tesseract.js');
// const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// const imagesDir = path.join(__dirname, './images');
// const outputCsvFile = path.join(__dirname, 'extracted_data.csv');

// // Set up CSV writer
// const csvWriter = createCsvWriter({
//   path: outputCsvFile,
//   header: [
//     { id: 'name', title: 'Name' },
//     { id: 'husbandFatherName', title: 'Husband/Father Name' },
//     { id: 'houseNumber', title: 'House Number' },
//     { id: 'age', title: 'Age' },
//     { id: 'gender', title: 'Gender' }
//   ]
// });

// // Function to extract text from an image
// const extractTextFromImage = async (imagePath) => {
//   try {
//     const { data: { text } } = await Tesseract.recognize(imagePath, 'eng', {
//       logger: info => console.log(info)
//     });
//     return text;
//   } catch (err) {
//     console.error(`Error processing ${path.basename(imagePath)}:`, err);
//     return '';
//   }
// };

// // Function to parse and normalize text data
// const parseText = (text) => {
//   const lines = text.split('\n').filter(line => line.trim() !== '');
//   const peopleData = [];
//   let currentPerson = {};
  
//   for (let line of lines) {
//     line = line.trim();

//     // Skip lines that do not contain relevant data
//     if (line.match(/^\d+[-\s\w]+$/) || line.match(/Electoral roll updated on/)) continue;

//     // Extract and clean person data
//     const nameMatch = line.match(/Name\s*:\s*(.*)$/);
//     if (nameMatch) {
//       if (Object.keys(currentPerson).length) {
//         peopleData.push(currentPerson);
//       }
//       currentPerson = { name: nameMatch[1].trim() };
//       continue;
//     }

//     const husbandFatherMatch = line.match(/(Husband Name|Father Name)\s*:\s*(.*)$/);
//     if (husbandFatherMatch) {
//       currentPerson.husbandFatherName = husbandFatherMatch[2].trim();
//       continue;
//     }

//     const houseNumberMatch = line.match(/House Number\s*:\s*(.*)$/);
//     if (houseNumberMatch) {
//       currentPerson.houseNumber = houseNumberMatch[1].trim();
//       continue;
//     }

//     const ageGenderMatch = line.match(/Age\s*:\s*(\d+)\s*Gender\s*:\s*(.*)$/);
//     if (ageGenderMatch) {
//       currentPerson.age = ageGenderMatch[1].trim();
//       currentPerson.gender = ageGenderMatch[2].trim();
//       continue;
//     }

//     // If line does not match any pattern, it might be additional info or noise
//   }

//   // Push the last person object
//   if (Object.keys(currentPerson).length) {
//     peopleData.push(currentPerson);
//   }

//   return peopleData;
// };

// // Function to process images and write data to CSV
// const processImages = async () => {
//   fs.readdir(imagesDir, async (err, files) => {
//     if (err) {
//       console.error('Error reading directory:', err);
//       return;
//     }

//     let allPeopleData = [];
//     for (const file of files) {
//       const filePath = path.join(imagesDir, file);
//       const fileExt = path.extname(file).toLowerCase();

//       if (fileExt === '.png' || fileExt === '.jpg' || fileExt === '.jpeg') {
//         const text = await extractTextFromImage(filePath);
//         const peopleData = parseText(text);
//         allPeopleData = allPeopleData.concat(peopleData);
//       }
//     }

//     csvWriter.writeRecords(allPeopleData)
//       .then(() => console.log('CSV file was written successfully'))
//       .catch(err => console.error('Error writing CSV file:', err));
//   });
// };

// processImages();
