const { pdfToText } = require('text-from-pdf');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

async function getPageCount(pdfPath) {
  const data = fs.readFileSync(pdfPath);
  const pdfDoc = await PDFDocument.load(data);
  return pdfDoc.getPageCount();
}

async function extractTextFromPDF(pdfPath) {
  try {
    const totalPages = await getPageCount(pdfPath);
    
    const options = {
      firstPageToConvert: 3,
      lastPageToConvert: totalPages-2, 
    };

    const text = await pdfToText(pdfPath, options);
    console.log(`Text extracted from ${pdfPath}:`);
    console.log(text);
  } catch (error) {
    console.error(`Error processing ${pdfPath}:`, error);
  }
}

function runPythonScript() {
  return new Promise((resolve, reject) => {
    exec('python3 /home/shiva/Documents/OCR/p8.py', (error, stdout, stderr) => {
      if (error) {
        console.error(`Error executing Python script: ${error}`);
        return reject(error);
      }
      if (stderr) {
        console.error(`Python script stderr: ${stderr}`);
        return reject(stderr);
      }
      console.log(`Python script output: ${stdout}`);
      resolve(stdout);
    });
  });
}

async function processPDFFolder(folderPath) {
  try {
    const files = fs.readdirSync(folderPath);

    const pdfFiles = files.filter(file => path.extname(file).toLowerCase() === '.pdf');

    for (const pdfFile of pdfFiles) {
      const pdfPath = path.join(folderPath, pdfFile);
      await extractTextFromPDF(pdfPath);
    }
  } catch (error) {
    console.error('Error processing folder:', error);
  }
}

const folderPath = '/home/shiva/Documents/OCR/utils';
processPDFFolder(folderPath);
