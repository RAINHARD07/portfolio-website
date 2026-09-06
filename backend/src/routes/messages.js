const router = require('express').Router();
const rateLimit = require('express-rate-limit');
const prisma = require('../db');
const { asyncHandler, requireAuth } = require('../middleware');
const { messageInput, parse } = require('../validation');
const { readPagination, page } = require('../pagination');

const submitLimit = rateLimit({ windowMs: 15 * 60 * 1000, limit: 8, standardHeaders: 'draft-8', legacyHeaders: false, message: { error: { code: 'RATE_LIMITED', message: 'Too many messages. Try again later.' } } });
router.post('/', submitLimit, asyncHandler(async (req, res) => { const data = parse(messageInput, req.body); const message = await prisma.message.create({ data: { ...data, email: data.email.toLowerCase() } }); res.status(201).json({ data: { id: String(message.id), createdAt: message.createdAt } }); }));
router.get('/', requireAuth, asyncHandler(async (req, res) => { const { limit, cursor } = readPagination(req.query); const where = {}; if (req.query.isRead === 'true' || req.query.isRead === 'false') where.isRead = req.query.isRead === 'true'; if (req.query.q) { const q = String(req.query.q).trim().slice(0, 120); where.OR = [{ name: { contains: q, mode: 'insensitive' } }, { email: { contains: q, mode: 'insensitive' } }, { subject: { contains: q, mode: 'insensitive' } }]; } const items = await prisma.message.findMany({ where, take: limit + 1, ...(cursor ? { skip: 1, cursor: { id: cursor } } : {}), orderBy: [{ createdAt: 'desc' }, { id: 'desc' }] }); res.json(page(items, limit)); }));
module.exports = router;
