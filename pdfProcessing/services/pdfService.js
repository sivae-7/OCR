const { pdfToText } = require('text-from-pdf');
const { PDFDocument } = require('pdf-lib');
const fs = require('fs');
const path = require('path');


async function processCreatedPDFs(pdfPath) {
  try {
    await extractTextFromPDF(pdfPath);
    return await moveImagesBeforeNextPDF();
    
  } catch (error) {
    console.error('Error fetching PDF paths from the database:', error);
  }
}
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
      lastPageToConvert: totalPages - 2,
    };

    const text = await pdfToText(pdfPath, options); 
    console.log(text);
  } catch (error) {
    console.error('Error processing PDF:', error);
  }
}


function moveImagesAsync(sourceDir, targetDir) {
  return new Promise((resolve, reject) => {
      if (!fs.existsSync(sourceDir)) {
          return reject(`Source directory "${sourceDir}" does not exist.`);
      }

      if (!fs.existsSync(targetDir)) {
          fs.mkdirSync(targetDir, { recursive: true });
      }

      fs.readdir(sourceDir, (err, files) => {
          if (err) return reject(err);

          const movePromises = files.map(file => {
              return new Promise((resolve, reject) => {
                  const sourceFilePath = path.join(sourceDir, file);
                  const targetFilePath = path.join(targetDir, file);
                  
                  fs.rename(sourceFilePath, targetFilePath, (err) => {
                      if (err) return reject(err);
                      console.log(`Moved file: ${file}`);
                      resolve();
                  });
              });
          });

          Promise.all(movePromises)
              .then(() => resolve())
              .catch(reject);
      });
  });
}

function getTargetFolder(baseDir) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-'); 
  return path.join(baseDir, `${timestamp}`);
}

async function moveImagesBeforeNextPDF() {
  const sourceDir = './images'; 
  const baseTargetDir = '/home/shiva/Documents/OCR/imageProcessing/images';  

  const targetDir = getTargetFolder(baseTargetDir);

  try {
      await moveImagesAsync(sourceDir, targetDir);
      console.log('All images moved successfully!');
      return targetDir;
  } catch (error) {
      console.error('Error moving images:', error);
  }
}



module.exports = {
  processCreatedPDFs,
};
