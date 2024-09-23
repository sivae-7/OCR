const {Queue,Worker} = require('bullmq')
import IORedis from 'ioredis';
const processPdf = require('./pdfProcess');

const connection = new IORedis();
const pdfQueue = new Queue('pdfQueue', { connection });
const worker = new Worker('pdfQueue', processPdf,{ connection });

module.exports = {pdfQueue};