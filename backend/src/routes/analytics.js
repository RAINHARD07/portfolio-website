const router = require('express').Router();
const prisma = require('../db');
const { asyncHandler, requireAuth } = require('../middleware');
const { visitInput, parse } = require('../validation');
const { enqueue, flush } = require('../analytics-buffer');

router.post('/visit', asyncHandler(async (req, res) => { const data = parse(visitInput, req.body); enqueue({ ...data, ip: req.ip, userAgent: req.get('user-agent') }); res.status(202).json({ data: { accepted: true } }); }));
router.get('/summary', requireAuth, asyncHandler(async (req, res) => { const days = Math.min(Math.max(Number(req.query.days || 30), 1), 365); await flush(); const since = new Date(Date.now() - days * 86400000); const [total, unique, topPages, daily] = await Promise.all([prisma.visit.count({ where: { visitedAt: { gte: since } } }), prisma.$queryRaw`SELECT count(DISTINCT ip_hash)::int AS count FROM analytics_visits WHERE visited_at >= ${since}`, prisma.visit.groupBy({ by: ['pageVisited'], where: { visitedAt: { gte: since } }, _count: { _all: true }, orderBy: { _count: { pageVisited: 'desc' } }, take: 10 }), prisma.$queryRaw`SELECT date_trunc('day', visited_at) AS day, count(*)::int AS visits, count(DISTINCT ip_hash)::int AS unique_visitors FROM analytics_visits WHERE visited_at >= ${since} GROUP BY 1 ORDER BY 1 ASC`]); res.json({ data: { days, totalVisits: total, uniqueVisitors: Number(unique[0]?.count || 0), topPages: topPages.map(row => ({ page: row.pageVisited, visits: row._count._all })), daily } }); }));
module.exports = router;
