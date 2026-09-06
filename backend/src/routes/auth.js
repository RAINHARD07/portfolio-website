const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const router = require('express').Router();
const prisma = require('../db');
const config = require('../config');
const { asyncHandler } = require('../middleware');
const { loginInput, parse } = require('../validation');

router.post('/login', asyncHandler(async (req, res) => {
  const { email, password } = parse(loginInput, req.body);
  const admin = await prisma.adminUser.findUnique({ where: { email: email.toLowerCase() } });
  if (!admin || !(await bcrypt.compare(password, admin.passwordHash))) return res.status(401).json({ error: { code: 'INVALID_CREDENTIALS', message: 'Email or password is incorrect.' } });
  const token = jwt.sign({ sub: String(admin.id), email: admin.email }, config.jwtSecret, { expiresIn: config.jwtExpiresIn });
  res.json({ data: { token, expiresIn: config.jwtExpiresIn } });
}));

module.exports = router;
