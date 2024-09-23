import { Sequelize } from 'sequelize';
const sequelize = new Sequelize('pdftextdb', 'postgres', 'root', {
  host: 'localhost',
  dialect: 'postgres',
});
export default sequelize;
