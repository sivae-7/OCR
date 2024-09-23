const sequelize = require('../config/database');
const scheduleJobs = require('../worker/scheduler')

async function main() {
  try {
    await sequelize.authenticate();
    console.log('Connection has been established successfully.');

    await setInterval(scheduleJobs,10000)
  } catch (error) {
    console.error('job shedule Error:', error);
  } finally {
    await sequelize.close();
  }
}

main();
