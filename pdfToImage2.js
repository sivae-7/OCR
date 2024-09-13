const { pdfToText } = require('text-from-pdf');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');

async function getPageCount(pdfPath) {
  const data = fs.readFileSync(pdfPath);
  const pdfDoc = await PDFDocument.load(data);
  return pdfDoc.getPageCount();
}

async function extractTextFromPDF(pdfPath) {
  try {
    const totalPages = await getPageCount(pdfPath);
    
    const options = {
      firstPageToConvert: 1,
      lastPageToConvert: totalPages, 
    };

    const text = await pdfToText(pdfPath, options);
    console.log(text);
  } catch (error) {
    console.error('Error processing PDF:', error);
  }
}

const pdfPath = '/home/shiva/Documents/OCR/utils/2024-FC-EROLLGEN-S22-175-FinalRoll-Revision2-ENG-185-WI.pdf';
extractTextFromPDF(pdfPath);
