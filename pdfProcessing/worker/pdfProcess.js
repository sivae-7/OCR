import { Worker }from "bullmq"
import Task from "../models/task.js" 
import Batch from "../models/batch.js" 
import processCreatedPDFs  from "../services/pdfService.js"
import {connection,pdfQueue} from "./queue.js"

const worker = new Worker('pdfQueue', async (job) => {
    try {
        console.log("pdfprocessing started......")
        const { pdfid, pdfPath } = job.data
        const imgfolderpath = await processCreatedPDFs(pdfPath);

        await Task.create({
            pdfid: pdfid,
            imgfolderpath: imgfolderpath,
            status: "created",
        });

        await Batch.update({ status: "processed" }, { where: { pdfid: pdfid } });
        console.log("pdf processing completed......")
       
    } catch (error) {
      console.error("Error fetching PDF paths from the database:", error);
    }
}, { connection });
       
worker.on("completed", (job) => {
  console.log(`Job ${job.id} completed successfully`);
});
worker.on("failed", (job, error) => {
  console.error(`Failed job with ID ${job.id}:`, error);
});

export default worker;
