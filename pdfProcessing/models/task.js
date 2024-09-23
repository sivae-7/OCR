const { Model, DataTypes } = require('sequelize');
const sequelize = require('../config/database');

class Task extends Model {}

Task.init({
    imgid: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
        field: 'pdfid', 
    },
    pdfid: {
        type: DataTypes.INTEGER,
        references: {
          model: 'Batch',
          key: 'pdfid',
        },
    },
    imgpath: {
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
    modelName: 'Task',
    tableName: 'task', 
    timestamps: false, 
});

module.exports = Task;
