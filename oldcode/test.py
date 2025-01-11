from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Selenium
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Run browser in headless mode
driver = webdriver.Chrome(options=options)

try:
    # Open the page
    driver.get("https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces")
    
    # Fill a form field
    input_field = driver.find_element(By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit")
    input_field.send_keys("1128275485")

    # Submit the form
    input_field.send_keys(Keys.RETURN)

    # Wait for a specific element to load after submitting the form
    # Adjust the condition as needed based on the page content that signals it is ready
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vistaConsultaEstadoRUT:formConsultaEstadoRUT:dv")))

    # After the page has loaded, get the HTML
    result_html = driver.page_source
    soup = BeautifulSoup(result_html, 'html.parser')
    
    with open('test.html', 'w') as file:
        file.write(soup.prettify())

finally:
    driver.quit()
