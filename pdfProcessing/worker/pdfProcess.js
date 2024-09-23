const { Worker } = require("bullmq");
const { Task } = require("../models/task"); 
const { Batch } = require("../models/batch");
const processCreatedPDF  = require("../services/pdfService.js")
const { connection , pdfQueue } = require("./queue.js");

const worker = new Worker(pdfQueue, async (job) => {
    try {
        const { pdfid, pdfPath } = pdfRecord
        const imgfolderpath = await processCreatedPDF(pdfPath);

        await Task.create({
            pdfid: pdfid,
            imgfolderpath: imgfolderpath,
            status: "created",
        });

        await Batch.update({ status: "processed" }, { where: { pdfid: pdfid } });
       
    } catch (error) {
      console.error("Error fetching PDF paths from the database:", error);
    }
}, { connection });
       
worker.on("completed", (job) => {
  // run the image to text here after the pdf to image is done.
  console.log(`Job ${job.id} completed successfully`);
});
worker.on("failed", (job, error) => {
  console.error(`Failed job with ID ${job.id}:`, error);
});

module.exports = processPdf;
