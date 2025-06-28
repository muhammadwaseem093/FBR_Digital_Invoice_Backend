import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_item_details(page, item_link):
    await page.goto(item_link)
    await page.wait_for_load_state('networkidle')
    await page.wait_for_timeout(3000)  # Allow content to render

    details = await page.evaluate("""
        () => {
            const name = document.querySelector('h1')?.innerText || 'Unknown';
            const description = document.querySelector('.ant-descriptions')?.innerText || '';
            
            const data = { name, description, tables: [] };

            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                const rows = table.querySelectorAll('tr');
                const tableData = [];
                rows.forEach(row => {
                    const cells = row.querySelectorAll('td, th');
                    const rowData = Array.from(cells).map(cell => cell.innerText.trim());
                    tableData.push(rowData);
                });
                data.tables.push(tableData);
            });

            return data;
        }
    """)

    return details

async def scrape_items():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        url = "https://flyffipedia.com/items"
        print(f"🌐 Navigating to {url}...")
        await page.goto(url)
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(5000)

        print("✅ Page loaded, extracting items...")

        await page.wait_for_selector('tbody tr', timeout=30000)
        items = await page.evaluate("""
            () => {
                const rows = document.querySelectorAll('tbody tr');
                const data = [];
                rows.forEach(row => {
                    const cols = row.querySelectorAll('td');
                    if (cols.length >= 2) {
                        const name = cols[1].innerText.trim();
                        const link = cols[1].querySelector('a')?.href || '';
                        data.push({ name, link });
                    }
                });
                return data;
            }
        """)

        print(f"✅ Found {len(items)} items. Extracting first 10 with full details...")

        detailed_items = []
        detail_page = await browser.new_page()

        for idx, item in enumerate(items[:10]):
            print(f"🔍 Extracting details for item {idx+1}: {item['name']}")
            details = await scrape_item_details(detail_page, item['link'])
            detailed_items.append(details)

        await browser.close()

        with open("items_detailed.json", "w", encoding="utf-8") as f:
            json.dump(detailed_items, f, ensure_ascii=False, indent=2)

        print(f"🎉 Extraction complete. Saved {len(detailed_items)} items to items_detailed.json")

asyncio.run(scrape_items())
