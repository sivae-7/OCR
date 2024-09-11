const { pdfToText } = require ("text-from-pdf");
const options = {
    firstPageToConvert: 1,
    lastPageToConvert: 30,
  };
const text = pdfToText('./utils/2024-FC-EROLLGEN-S22-175-FinalRoll-Revision2-ENG-186-WI.pdf', options);
console.log(text)
