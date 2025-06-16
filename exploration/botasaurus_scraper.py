#THIS ONE WORKS!!!

from botasaurus.browser import browser, Wait

@browser(headless=True)
def scrape_tunebat(driver, data):
    driver.google_get(data["url"], bypass_cloudflare=True)
    driver.wait_for_element("div.yIPfN", wait=Wait.LONG)

    result = {}

    # Title & Artist
    result["title"] = driver.get_text("h1.BSDxW")
    result["artist"] = driver.get_text("h3._6IzUR")

    # Main metric blocks
    for block in driver.select_all("div.yIPfN"):
        label_el = block.select("span")
        value_el = block.select("h3")
        if label_el and value_el:
            label = label_el.text.strip().lower()
            value = value_el.text.strip()
            result[label] = value

    # Fix: get correct labels for circular metrics
    for block in driver.select_all("div._1MCwQ"):
        value_el = block.select(".ant-progress-text")
        label_el = block.select(".fd89q")  # this class is used for the metric name
        if label_el and value_el:
            label = label_el.text.strip().lower()
            value = value_el.text.strip()
            result[label] = value

    # Metadata: release date, explicit, album
    for meta in driver.select_all("div._4aYzP span.ant-typography"):
        if ":" in meta.text:
            label, value = meta.text.split(":", 1)
            result[label.strip().lower()] = value.strip()

    return result
