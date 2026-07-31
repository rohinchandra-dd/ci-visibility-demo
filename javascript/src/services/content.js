const {
  add, subtract, multiply, divide, isPalindrome, fibonacci,
  flatten, chunkList, mergeDicts, clamp,
} = require('../utils');

function formatArticleTitle(title) {
  return title.trim().replace(/\s+/g, ' ');
}

function truncateBody(body, maxLength = 200) {
  if (body.length <= maxLength) return body;
  return `${body.slice(0, maxLength)}...`;
}

function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function calculateReadingTime(wordCount) {
  return Math.max(1, Math.ceil(wordCount / 200));
}

function mergeArticleMeta(article, meta) {
  return mergeDicts(article, meta);
}

function paginateItems(items, page, pageSize) {
  const start = multiply(subtract(page, 1), pageSize);
  return chunkList(items, pageSize)[Math.floor(start / pageSize)] || [];
}

module.exports = {
  add, subtract, multiply, divide, isPalindrome, fibonacci,
  flatten, chunkList, mergeDicts, clamp,
  formatArticleTitle,
  truncateBody,
  validateEmail,
  calculateReadingTime,
  mergeArticleMeta,
  paginateItems,
};
