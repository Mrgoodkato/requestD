from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep

# Set up Selenium with a regular browser
options = webdriver.ChromeOptions()
# Remove headless mode
# options.add_argument("--headless")  # Do not use headless mode
driver = webdriver.Chrome(options=options)

try:
    # Open the page
    driver.get("https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces")

    # Fill a form field
    input_field = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit")
    input_field.send_keys("1128275485")

    # Submit the form
    input_field.send_keys(Keys.RETURN)

    # Wait for the CAPTCHA to load and solve it manually
    sleep(10)  # Adjust sleep time if needed, or use `input()` to pause for manual CAPTCHA solving

    # After solving the CAPTCHA manually, continue with the process
    sleep(5)  # Wait for page to load after submitting the CAPTCHA

    # Get the page HTML
    result_html = driver.page_source
    soup = BeautifulSoup(result_html, 'html.parser')
    
    with open('test.html', 'w') as file:
        file.write(soup.prettify())

finally:
    driver.quit()
