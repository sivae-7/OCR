const sequelize = require('../config/database');
const { processCreatedPDFs } = require('../services/pdfService');

async function main() {
  try {
    await sequelize.authenticate();
    console.log('Connection has been established successfully.');

    await processCreatedPDFs();
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await sequelize.close();
  }
}

main();
