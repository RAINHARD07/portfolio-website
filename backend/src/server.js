const app = require('./app');
const config = require('./config');
const prisma = require('./db');

const server = app.listen(config.port, () => console.log(`Portfolio API listening on http://localhost:${config.port}`));

async function shutdown(signal) { console.log(`${signal}: shutting down`); server.close(async () => { await prisma.$disconnect(); process.exit(0); }); }
process.on('SIGTERM', () => shutdown('SIGTERM'));
process.on('SIGINT', () => shutdown('SIGINT'));
