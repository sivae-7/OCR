import sequelize from "../config/database.js";
import scheduleJobs from "../worker/scheduler.js";
import "../worker/pdfProcess.js"

async function main() {
  try {
    await sequelize.authenticate();
    console.log('Connection has been established successfully.');


    setInterval(async () => {
      try {
        await scheduleJobs();
      } catch (error) {
        console.error('Error during job scheduling:', error);
      }
    }, 2*60000);
    console.log('Job scheduler started.'); 
  } catch (error) {
    console.error('Error establishing database connection:', error);
  }
}

main();
