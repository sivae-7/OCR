import sequelize from "../config/database.js";
import scheduleJobs from "../worker/scheduler.js";

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
    }, 12 * 10000); // Every 120 seconds (2 minutes)

    console.log('Job scheduler started.');

    process.on('SIGINT', async () => {
      console.log('Gracefully shutting down...');
      await sequelize.close(); 
      process.exit(0);
    });

  } catch (error) {
    console.error('Error establishing database connection:', error);
  }
}

main();
