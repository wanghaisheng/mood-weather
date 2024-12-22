import xml.etree.ElementTree as ET
import asyncio
from loguru import logger
from getbrowser import  setup_chrome

# Assuming the 'submit_radar_with_retry' and 'Recorder' are defined elsewhere in your code.
# Replace this with your actual method for submitting URLs to Radar.
from radar import submit_radar_with_retry  
from DataRecorder import Recorder  

def parse_sitemap(sitemap_file):
    """Parse the sitemap.xml and extract all URLs."""
    print('parsing====', sitemap_file)
    tree = ET.parse(sitemap_file)
    root = tree.getroot()
    
    # Handle namespaces if present
    namespace = {
        'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
    }

    urls = [url.text for url in root.findall('.//ns:url/ns:loc', namespace)]
    logger.info(f"Found {len(urls)} URLs in the sitemap.")
    return urls

async def submit_urls_to_radar(urls, outfile):
    """Submit URLs to Radar asynchronously."""
    for url in urls:
        try:
            logger.info(f"Submitting {url} to Radar...")
            # Replace this with your actual Radar submission method
            await submit_radar_with_retry(None, url, None, [], None, outfile)
        except Exception as e:
            logger.error(f"Failed to submit {url} to Radar: {e}")

def main():
    # Load the sitemap XML file
    sitemap_file = "sitemap.xml"  # This should match the filename or path downloaded

    # Parse the sitemap and extract URLs
    urls = parse_sitemap(sitemap_file)

    # Assuming 'Recorder' is your method for storing submission logs or tracking
    outfile = Recorder()  # Replace with your actual Recorder or similar object

    # Submit URLs to Radar
    browser=setup_chrome()
    asyncio.run(submit_urls_to_radar(browser,urls, outfile))

if __name__ == '__main__':
    main()
