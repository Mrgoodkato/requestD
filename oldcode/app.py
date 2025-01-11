import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver (Ensure `chromedriver` is installed)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    # Navigate to the Turnstile-protected page
    driver.get("https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces")

    # Wait for the Turnstile iframe to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    )
    print("Turnstile loaded. Please complete the CAPTCHA.")

    # Wait for user to solve the Turnstile CAPTCHA
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.NAME, "cf-turnstile-response"))
    )

    # Extract the Turnstile response
    turnstile_response = driver.find_element(By.NAME, "cf-turnstile-response").get_attribute("value")
    print("cf-turnstile-response:", turnstile_response)

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()

# URL of the endpoint
url = "https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces"

# Headers (add all headers from your example)
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "text/html;charset=ISO-8859-1",
    "Host": "muisca.dian.gov.co",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

# Send the POST request
response = requests.get(url, headers=headers)
yoink = {
    'jsessionToken': '',
    'hddllavePublica': ''
}

if response.status_code == 200:
    print('Success! - ', response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    yoink["jsessionToken"] = re.findall(r'(?<=jsessionid=).+?(?=")', response.text)
    yoink["hddllavePublica"] = re.findall(r'(?<=hddllavePublica" value=").+?(?=")', response.text)
    print(yoink)
    with open('textOutput.txt', 'w') as txtfile:
        txtfile.write(response.text)
    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

    print('HTML Saved!')
else:
    print('Failed')





# Payload (add the payload from your example)
payload = {
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:modoPresentacionSeleccionBO": "pantalla",
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:siguienteURL": "",
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:modoPresentacionFormBO": "pantalla",
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:modoOperacionFormBO": "",
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:mantenerCriterios": "",
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:hddToken": "YOUR_TOKEN_HERE",
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:hddllavePublica": "0x4AAAAAAAg1YFKr1lxPdUIL",
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit": "1128275485",
    "cf-turnstile-response": "YOUR_CF_RESPONSE_HERE",
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:btnBuscar.x": "0",
    "vistaConsultaEstadoRUT:formConsultaEstadoRUT:btnBuscar.y": "0",
    "com.sun.faces.VIEW": "H4sIAAAAAAAAA...",
}

# Encode the payload as form data
encoded_payload = "&".join(f"{key}={value}" for key, value in payload.items())