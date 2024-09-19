const { pdfToText } = require('text-from-pdf');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

async function getPageCount(pdfPath) {
  const data = fs.readFileSync(pdfPath);
  const pdfDoc = await PDFDocument.load(data);
  return pdfDoc.getPageCount();
}

function runPythonScript() {
  return new Promise((resolve, reject) => {
    console.log('Starting Python script...');

    const pythonProcess = spawn('python3', ['/home/shiva/Documents/OCR/textExtraction.py']);

    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python Output: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python script exited with code ${code}`);
        reject(`Python script exited with code ${code}`);
      } else {
        console.log('Python script finished successfully');
        resolve();
      }
    });
  });
}

function removeImagesInFolder(folderPath) {
  return new Promise((resolve, reject) => {
    fs.readdir(folderPath, (err, files) => {
      if (err) {
        console.error('Error reading the folder:', err);
        return reject(err);
      }

      const imageFiles = files.filter(file => ['.jpg', '.jpeg', '.png'].includes(path.extname(file).toLowerCase()));

      imageFiles.forEach(file => {
        const filePath = path.join(folderPath, file);
        fs.unlink(filePath, (err) => {
          if (err) {
            console.error(`Error deleting file ${file}:`, err);
          } else {
            console.log(`Successfully deleted file ${file}`);
          }
        });
      });

      resolve();
    });
  });
}

async function extractTextFromPDF(pdfPath) {
  try {
    const totalPages = await getPageCount(pdfPath);

    const options = {
      firstPageToConvert: 3,
      lastPageToConvert: totalPages - 2,
    };

    const text = await pdfToText(pdfPath, options);
    console.log(`Text extracted from ${pdfPath}:`);
    console.log(text);

  } catch (error) {
    console.error(`Error processing ${pdfPath}:`, error);
  }
}

async function processPDFFolder(folderPath) {
  try {
    const files = fs.readdirSync(folderPath);
    const pdfFiles = files.filter(file => path.extname(file).toLowerCase() === '.pdf');

    for (const pdfFile of pdfFiles) {
      const pdfPath = path.join(folderPath, pdfFile);

      await extractTextFromPDF(pdfPath);

      await runPythonScript();

      const imagesFolderPath = '/home/shiva/Documents/OCR/images';  
      await removeImagesInFolder(imagesFolderPath);
    }
  } catch (error) {
    console.error('Error processing folder:', error);
  }
}

const folderPath = '/home/shiva/Documents/OCR/utils/';
processPDFFolder(folderPath);
