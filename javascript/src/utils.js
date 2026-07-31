function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) {
    throw new Error('Cannot divide by zero');
  }
  return a / b;
}

function isPalindrome(text) {
  const normalized = text.toLowerCase().replace(/\s/g, '');
  return normalized === normalized.split('').reverse().join('');
}

function fibonacci(n) {
  if (n < 0) {
    throw new Error('n must be non-negative');
  }
  if (n <= 1) {
    return n;
  }
  let a = 0;
  let b = 1;
  for (let i = 2; i <= n; i += 1) {
    const next = a + b;
    a = b;
    b = next;
  }
  return b;
}

function flatten(items) {
  return items.reduce((acc, item) => {
    if (Array.isArray(item)) {
      return acc.concat(flatten(item));
    }
    return acc.concat(item);
  }, []);
}

function chunkList(items, size) {
  if (size <= 0) {
    throw new Error('size must be positive');
  }
  const chunks = [];
  for (let i = 0; i < items.length; i += size) {
    chunks.push(items.slice(i, i + size));
  }
  return chunks;
}

function mergeDicts(...dicts) {
  return Object.assign({}, ...dicts);
}

function clamp(value, minimum, maximum) {
  return Math.max(minimum, Math.min(value, maximum));
}

module.exports = {
  add,
  subtract,
  multiply,
  divide,
  isPalindrome,
  fibonacci,
  flatten,
  chunkList,
  mergeDicts,
  clamp,
};
