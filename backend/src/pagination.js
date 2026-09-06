function readPagination(query) {
  const limit = Math.min(Math.max(Number(query.limit || 20), 1), 100);
  const cursor = query.cursor ? BigInt(query.cursor) : undefined;
  return { limit, cursor };
}

function page(items, limit) {
  const hasMore = items.length > limit;
  const data = hasMore ? items.slice(0, limit) : items;
  return { data, pagination: { limit, hasMore, nextCursor: hasMore ? String(data[data.length - 1].id) : null } };
}

module.exports = { readPagination, page };
