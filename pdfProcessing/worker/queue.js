import {Queue} from 'bullmq'
import IORedis from 'ioredis';
const connection = new IORedis();
const pdfQueue = new Queue('pdfQueue', { connection });

export {pdfQueue,connection};