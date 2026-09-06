const path = require('node:path');
const dotenv = require('dotenv');
dotenv.config({ path: path.resolve(__dirname, '..', '.env') });

function required(name) {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

module.exports = {
  nodeEnv: process.env.NODE_ENV || 'development',
  port: Number(process.env.PORT || 4000),
  databaseUrl: required('DATABASE_URL'),
  jwtSecret: required('JWT_SECRET'),
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '15m',
  corsOrigin: process.env.CORS_ORIGIN || '*',
  analyticsFlushMs: Number(process.env.ANALYTICS_FLUSH_MS || 1000),
  analyticsBatchSize: Number(process.env.ANALYTICS_BATCH_SIZE || 100),
};
