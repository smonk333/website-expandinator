import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# URL of the page you want to expand elements on
URL = 'https://www.example.com' # replace with your desired URL

# initialize the webdriver
driver = webdriver.Chrome()
driver.get(URL)

# wait for the page to load
time.sleep(3)

# create a set to track clicked elements
clicked_elements = set()

try:
    # find all elements on the page
    all_elements = driver.find_elements(By.XPATH, "//*")

    # filter elements based on substrings in the class attribute
    collapsible_elements = [
        element for element in all_elements
        if "collap" in (element.get_attribute("class") or "").lower() or
           "expan" in (element.get_attribute("class") or "").lower()
    ]

    print(f"Found {len(collapsible_elements)} potentially collapsible elements.")

    # get the current domain
    current_domain = driver.current_url.split("//")[1].split("/")[0]

    # loop through filtered elements and try to expand them
    for element in collapsible_elements:
        try:
            # Get a unique identifier for the element
            element_id = element.get_attribute("outerHTML")  # Use outerHTML or another unique attribute

            # Check if the element has already been clicked
            if element_id in clicked_elements:
                print("Skipping already-clicked element.")
                continue

            # make sure the element won't take us to another part of the site
            tag_name = element.tag_name.lower()
            href = element.get_attribute("href")

            if tag_name == "a" and href:  # For <a> tags
                target_domain = href.split("//")[1].split("/")[0]
                if target_domain != current_domain:
                    print(f"Skipping external link: {href}")
                    continue

            # scroll to element
            ActionChains(driver).move_to_element(element).perform()

            # simulate click using js to prevent default navigation
            driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            print(f"Could not interact with element: {e}")

except Exception as e:
    print(f"No collapsible elements found: {e}")

print("Script completed.")
