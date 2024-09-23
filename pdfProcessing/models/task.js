const { Model, DataTypes } = require('sequelize');
const sequelize = require('../config/database');

class Task extends Model {}

Task.init({
    imgfolderid: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
        field: 'imgfolderid', 
    },
    pdfid: {
        type: DataTypes.INTEGER,
        references: {
          model: 'Batch',
          key: 'pdfid',
        },
    },
    imgfolderpath: {
        type: DataTypes.TEXT,
        allowNull: false,
        field: 'imgfolderpath', 
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
