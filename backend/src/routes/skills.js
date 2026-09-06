const router = require('express').Router();
const prisma = require('../db');
const { asyncHandler } = require('../middleware');

router.get('/', asyncHandler(async (req, res) => { const skills = await prisma.skill.findMany({ orderBy: [{ category: 'asc' }, { proficiencyLevel: 'desc' }, { id: 'asc' }] }); const grouped = skills.reduce((result, skill) => { const { category, ...item } = skill; (result[category] ||= []).push(item); return result; }, {}); res.json({ data: grouped }); }));
module.exports = router;
