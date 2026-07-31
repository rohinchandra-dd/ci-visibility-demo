const { test, expect } = require('@playwright/test');

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

test.describe('Pulse E2E flows', () => {
  test('homepage loads', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.brand')).toContainText('Pulse');
  });

  for (let i = 1; i <= 10; i += 1) {
    test(`navigation flow ${i}`, async ({ page }) => {
      await page.goto('/');
      await sleep(3000);
      await page.click('text=Login');
      await expect(page.locator('h1')).toContainText('Sign in');
      await sleep(2000);
    });
  }

  for (let i = 1; i <= 10; i += 1) {
    test(`feed render check ${i}`, async ({ page }) => {
      await page.goto('/');
      await sleep(3000);
      const feed = page.locator('.feed, .empty');
      await expect(feed.first()).toBeVisible();
      await sleep(2000);
    });
  }
});
