const { Model, DataTypes } = require('sequelize');
const sequelize = require('../config/database');

class Batch extends Model {}

Batch.init({
    pdfid: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
        field: 'pdfid', 
    },
    pdfpath: {
        type: DataTypes.TEXT,
        allowNull: false,
        field: 'pdfpath', 
    },
    status: {
        type: DataTypes.STRING(50),
        allowNull: false,
        field: 'status', 
    },
}, {
    sequelize,
    modelName: 'Batch',
    tableName: 'batch', 
    timestamps: false, 
});

module.exports = Batch;
