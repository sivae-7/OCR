const Tesseract = require('tesseract.js');
const fs = require('fs');

Tesseract.recognize(
  './images/2024-FC-EROLLGEN-S22-175-FinalRoll-Revision2-ENG-185-WI-15.png', // Use the path of your uploaded image
  'eng',
  {
    logger: (m) => console.log(m), 
  }
).then(({ data: { text } }) => {
  fs.writeFileSync('output.txt', text);
  console.log("OCR Completed");
});
