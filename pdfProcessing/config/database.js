const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('pdftextdb', 'postgres', 'root', {
  host: 'localhost',
  dialect: 'postgres',
});

module.exports = sequelize;
