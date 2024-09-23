import { Worker }from "bullmq"
import Task from "../models/task" 
import Batch from "../models/batch" 
import processCreatedPDF  from "../services/pdfService.js"
import {connection,pdfQueue} from "./queue.js"

const worker = new Worker(pdfQueue, processPdf, { connection });

async function processPdf() {
     try {
        console.log("processing pdf ......")
       const pdfRecords = await Batch.findAll({

         where: { status: "created" },
       });


       for (const pdfRecord of pdfRecords) {
         const { pdfid, pdfPath } = pdfRecord
         const imgfolderpath = await processCreatedPDF(pdfPath);

         await Task.create({
            pdfid: pdfid,
            imgfolderpath: imgfolderpath,
            status: "created",
         });
         console.log("one task created...")
       }
     } catch (error) {
       console.error("Error fetching PDF paths from the database:", error);
     }
}

worker.on("completed", (job) => {
  // run the image to text here after the pdf to image is done.
  console.log(`Job ${job.id} completed successfully`);
});
worker.on("failed", (job, error) => {
  console.error(`Failed job with ID ${job.id}:`, error);
});

module.exports = processPdf;
