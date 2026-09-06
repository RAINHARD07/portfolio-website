const router = require('express').Router();
const prisma = require('../db');
const { asyncHandler, requireAuth } = require('../middleware');
const { projectInput, parse } = require('../validation');
const { readPagination, page } = require('../pagination');

router.get('/', asyncHandler(async (req, res) => { const { limit, cursor } = readPagination(req.query); const where = req.query.category ? { category: String(req.query.category).slice(0, 80) } : {}; const items = await prisma.project.findMany({ where, take: limit + 1, ...(cursor ? { skip: 1, cursor: { id: cursor } } : {}), orderBy: [{ featured: 'desc' }, { createdAt: 'desc' }, { id: 'desc' }] }); res.json(page(items, limit)); }));
router.post('/', requireAuth, asyncHandler(async (req, res) => { const data = parse(projectInput, req.body); const project = await prisma.project.create({ data }); res.status(201).json({ data: project }); }));
router.put('/:id', requireAuth, asyncHandler(async (req, res) => { const id = BigInt(req.params.id); const data = parse(projectInput.partial(), req.body); const project = await prisma.project.update({ where: { id }, data }); res.json({ data: project }); }));
router.delete('/:id', requireAuth, asyncHandler(async (req, res) => { await prisma.project.delete({ where: { id: BigInt(req.params.id) } }); res.status(204).end(); }));
module.exports = router;
