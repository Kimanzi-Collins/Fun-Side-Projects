# Image Scraper Walkthrough

## What Was Accomplished
We created a robust Python scraper to download all images from the 596 articles on the Ramco Group news page. The script relies on the WordPress JSON REST API, making it much more reliable than parsing raw HTML.

### Key Features Implemented:
*   **WebP Conversion**: All images are automatically converted to the `.webp` format for better compression and consistent formatting.
*   **Folder Naming**: Folder and file names are heavily sanitized to be completely lowercase with no spaces, hyphens, or punctuation (e.g. `backtoschoolshoppingwithofficemartandtrcillah`), as requested.
*   **High-Resolution Images**: The scraper intelligently bypasses hotlink protection (using `Referer` headers) and extracts the full-resolution images instead of the thumbnails usually embedded in the text.
*   **Resumability**: If the script is stopped or interrupted, it checks for existing files and skips them, allowing it to pick up exactly where it left off.

## Validation Results
*   **Test Run**: We ran a small test limited to the first 5 articles. The scraper successfully bypassed the hotlink protection and downloaded the high-resolution images into appropriately named folders.
*   *(Note: You noticed an article from 2024 was missing during the test. This was completely expected because the test was artificially restricted to stop after processing exactly 5 articles to save time!)*
*   **Full Run**: The full scrape of all ~600 articles is currently running in the background.

## Tracking Progress
The full scraper is currently running. You can track the live progress by either:
1. Monitoring the `Scraper Images` folder to see the years and article folders being populated.
2. Checking the background task log generated in your IDE.
