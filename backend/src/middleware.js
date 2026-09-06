const jwt = require('jsonwebtoken');
const config = require('./config');

function asyncHandler(handler) {
  return (req, res, next) => Promise.resolve(handler(req, res, next)).catch(next);
}

function requireAuth(req, res, next) {
  const header = req.get('authorization');
  const token = header && header.startsWith('Bearer ') ? header.slice(7) : null;
  if (!token) return res.status(401).json({ error: { code: 'UNAUTHORIZED', message: 'Authentication required.' } });
  try {
    req.admin = jwt.verify(token, config.jwtSecret);
    return next();
  } catch {
    return res.status(401).json({ error: { code: 'INVALID_TOKEN', message: 'Invalid or expired token.' } });
  }
}

function notFound(req, res) {
  res.status(404).json({ error: { code: 'NOT_FOUND', message: `Route ${req.method} ${req.path} not found.` } });
}

function errorHandler(error, req, res, next) {
  req.log?.error({ err: error }, 'request failed');
  if (res.headersSent) return next(error);
  const status = error.statusCode || 500;
  res.status(status).json({ error: { code: error.code || 'INTERNAL_ERROR', message: status === 500 ? 'An unexpected error occurred.' : error.message } });
}

module.exports = { asyncHandler, requireAuth, notFound, errorHandler };
