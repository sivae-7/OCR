const {Queue} = require('bullmq')
import IORedis from 'ioredis';
const connection = new IORedis();
const pdfQueue = new Queue('pdfQueue', { connection });

module.exports = {pdfQueue};