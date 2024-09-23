import {Queue} from 'bullmq'
import IORedis from 'ioredis';
const connection = new IORedis({
    maxRetriesPerRequest: null,
});
const pdfQueue = new Queue('pdfQueue', { connection });

export {pdfQueue,connection};