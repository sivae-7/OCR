const fs = require('fs');
const path = require('path');

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
    const sourceDir = '/home/shiva/Documents/OCR/pdfProcessing/images'; 
    const baseTargetDir = '/home/shiva/Documents/OCR/imageProcessing/images';  

    const targetDir = getTargetFolder(baseTargetDir);

    try {
        await moveImagesAsync(sourceDir, targetDir);
        console.log('All images moved successfully!');
    } catch (error) {
        console.error('Error moving images:', error);
    }
}


moveImagesBeforeNextPDF();
