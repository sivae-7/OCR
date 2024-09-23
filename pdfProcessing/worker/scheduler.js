import Batch from '../models/batch.js';
import { pdfQueue } from "./queue.js";

async function scheduleJobs() {
    try {
        console.log("Scheduling jobs......");
        const batches = await Batch.findAll({
            where: { status: 'created' },
        });

        for (const batch of batches) {
            await pdfQueue.add('processPdf', {
                pdfid: batch.pdfid,
                pdfPath: batch.pdfpath
            });

            await Batch.update({ status: 'processing' }, { where: { pdfid: batch.pdfid } });
            console.log("updated one batch .....")
        }
    } catch (error) {
        console.error('Error During scheduling jobs:', error);
    }
}

export default scheduleJobs;
