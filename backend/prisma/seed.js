const bcrypt = require('bcryptjs');
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  const email = process.env.SEED_ADMIN_EMAIL || 'admin@example.com';
  const password = process.env.SEED_ADMIN_PASSWORD || 'change-me-before-production';
  await prisma.adminUser.upsert({ where: { email }, update: {}, create: { email, passwordHash: await bcrypt.hash(password, 12) } });
  await prisma.skill.createMany({ data: [
    { name: 'LAN/WAN', category: 'Networking', proficiencyLevel: 85 }, { name: 'IP addressing', category: 'Networking', proficiencyLevel: 82 }, { name: 'IT troubleshooting', category: 'IT Support', proficiencyLevel: 90 }, { name: 'Windows/Linux', category: 'Systems Administration', proficiencyLevel: 78 }, { name: 'Threat monitoring', category: 'Cybersecurity', proficiencyLevel: 74 }, { name: 'AWS EC2', category: 'Cloud', proficiencyLevel: 68 }
  ], skipDuplicates: true });
  const projects = [
    { title: 'Password Strength Checker', category: 'Security', description: 'A local-first password feedback utility.', techStack: ['JavaScript', 'Security'], featured: true },
    { title: 'Phishing Email Analyzer', category: 'Security', description: 'A practical first-pass phishing triage tool.', techStack: ['JavaScript', 'Security'], featured: false },
    { title: 'AWS EC2 Personal Cloud Security Lab', category: 'Cloud', description: 'A repeatable EC2 hardening practice environment.', techStack: ['AWS', 'EC2', 'Cloud Security'], featured: false }
  ];
  for (const project of projects) await prisma.project.create({ data: project });
  const posts = Array.from({ length: 20 }, (_, index) => ({ title: `Systems note ${index + 1}`, slug: `systems-note-${index + 1}`, content: 'A short operational note about dependable IT systems.', excerpt: 'A practical note about dependable systems.', tags: ['systems', 'it-support'], publishedAt: new Date(Date.now() - index * 86400000) }));
  await prisma.blogPost.createMany({ data: posts, skipDuplicates: true });
  if (process.env.SEED_SCALE === 'true') {
    const messages = Array.from({ length: 5000 }, (_, index) => ({ name: `Test User ${index}`, email: `test-${index}@example.com`, subject: 'Pagination test', message: 'Seeded message for pagination and search testing.' }));
    for (let offset = 0; offset < messages.length; offset += 500) await prisma.message.createMany({ data: messages.slice(offset, offset + 500) });
    const visits = Array.from({ length: 10000 }, (_, index) => ({ pageVisited: index % 4 === 0 ? '/' : '/projects', ipHash: `${String(index % 1000).padStart(64, '0')}`, userAgent: 'seed', visitedAt: new Date(Date.now() - (index % 30) * 86400000) }));
    for (let offset = 0; offset < visits.length; offset += 500) await prisma.visit.createMany({ data: visits.slice(offset, offset + 500) });
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; }).finally(() => prisma.$disconnect());
