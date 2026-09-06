const crypto = require('node:crypto');
const prisma = require('./db');
const config = require('./config');

const queue = [];
let flushing = false;

function hashIp(ip) { return crypto.createHash('sha256').update(`${ip}:${config.jwtSecret}`).digest('hex'); }

function enqueue({ pageVisited, ip, userAgent, referrer }) {
  queue.push({ pageVisited, ipHash: hashIp(ip), userAgent: userAgent?.slice(0, 500), referrer: referrer?.slice(0, 500) });
  if (queue.length >= config.analyticsBatchSize) flush().catch(() => {});
}

async function flush() {
  if (flushing || queue.length === 0) return;
  flushing = true;
  const batch = queue.splice(0, config.analyticsBatchSize);
  try { await prisma.visit.createMany({ data: batch }); } catch (error) { queue.unshift(...batch); throw error; } finally { flushing = false; }
}

const timer = setInterval(() => flush().catch(() => {}), config.analyticsFlushMs);
timer.unref();

module.exports = { enqueue, flush };
