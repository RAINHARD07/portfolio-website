const router = require('express').Router();
const prisma = require('../db');
const { asyncHandler, requireAuth } = require('../middleware');
const { blogInput, parse } = require('../validation');
const { readPagination, page } = require('../pagination');

router.get('/', asyncHandler(async (req, res) => { const { limit, cursor } = readPagination(req.query); const items = await prisma.blogPost.findMany({ where: { publishedAt: { not: null, lte: new Date() } }, select: { id: true, title: true, slug: true, excerpt: true, tags: true, publishedAt: true, viewsCount: true }, take: limit + 1, ...(cursor ? { skip: 1, cursor: { id: cursor } } : {}), orderBy: [{ publishedAt: 'desc' }, { id: 'desc' }] }); res.json(page(items, limit)); }));
router.post('/', requireAuth, asyncHandler(async (req, res) => { const data = parse(blogInput, req.body); const post = await prisma.blogPost.create({ data }); res.status(201).json({ data: post }); }));
router.put('/:id', requireAuth, asyncHandler(async (req, res) => { const data = parse(blogInput.partial(), req.body); const post = await prisma.blogPost.update({ where: { id: BigInt(req.params.id) }, data }); res.json({ data: post }); }));
router.delete('/:id', requireAuth, asyncHandler(async (req, res) => { await prisma.blogPost.delete({ where: { id: BigInt(req.params.id) } }); res.status(204).end(); }));
module.exports = router;
