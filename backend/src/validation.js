const { z } = require('zod');

const url = z.string().url().max(500).optional().nullable();
const pagination = z.object({ limit: z.coerce.number().int().min(1).max(100).default(20), cursor: z.coerce.bigint().positive().optional() });
const messageInput = z.object({ name: z.string().trim().min(2).max(120), email: z.string().trim().email().max(320), subject: z.string().trim().max(200).optional(), message: z.string().trim().min(10).max(10000) }).strict();
const projectInput = z.object({ title: z.string().trim().min(2).max(240), description: z.string().trim().min(10).max(20000), category: z.string().trim().min(2).max(80), techStack: z.array(z.string().trim().min(1).max(80)).max(30).default([]), imageUrl: url, projectUrl: url, githubUrl: url, featured: z.boolean().default(false) }).strict();
const blogInput = z.object({ title: z.string().trim().min(2).max(240), slug: z.string().trim().regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/).max(260), content: z.string().trim().min(20), excerpt: z.string().trim().max(500).optional().nullable(), tags: z.array(z.string().trim().min(1).max(50)).max(30).default([]), publishedAt: z.coerce.date().optional().nullable() }).strict();
const loginInput = z.object({ email: z.string().trim().email().max(320), password: z.string().min(8).max(200) }).strict();
const visitInput = z.object({ pageVisited: z.string().trim().min(1).max(500), referrer: z.string().trim().max(500).optional().nullable() }).strict();

function parse(schema, value) {
  const result = schema.safeParse(value);
  if (!result.success) { const error = new Error('Request validation failed.'); error.statusCode = 400; error.code = 'VALIDATION_ERROR'; error.details = result.error.flatten(); throw error; }
  return result.data;
}

module.exports = { pagination, messageInput, projectInput, blogInput, loginInput, visitInput, parse };
