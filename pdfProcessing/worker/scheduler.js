const {pdfQueue} = require('./queue')
import Batch from '../models/batch'

async function scheduleJobs(){
    try{
        const batches = await Batch.findAll({
            where: { status: 'created' },
          });
        for ( const batch of batches ){
            await pdfQueue.add('processPdf',{
                pdfid : batch.pdfid,
                pdfPath : batch.pdfpath
            })

            await Batch.update({status : 'processing'});
        }
    }
    catch(error){
        console.error('Error During scheduling jobs:', error);
    }
}

module.exports = scheduleJobs;