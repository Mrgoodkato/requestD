import pychrome
from bs4 import BeautifulSoup

# Connect to the running Chrome instance
browser = pychrome.Browser(url="http://127.0.0.1:9223")  # Default debug port

tab = browser.new_tab()

def request_will_be_sent(**kwargs):
    print('loading: %s'  % kwargs.get('request').get('url'))

tab.set_listener('Network.requestWillBeSent', request_will_be_sent)

try:
    tab.start()
    tab.call_method('Network.enable')
    tab.call_method('Page.navigate', url='https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces', timeout=5)

    tab.wait(5)
    input_js = "document.getElementById('vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit').value = '1128275485'"
    tab.Runtime.evaluate(expression=input_js)
    button_js = "document.getElementById('vistaConsultaEstadoRUT:formConsultaEstadoRUT:btnBuscar').click()"
    tab.Runtime.evaluate(expression=button_js)
    tab.wait(5)

    root = tab.call_method('DOM.getDocument')
    root_node_id = root['root']['nodeId']

    element_selector = '#vistaConsultaEstadoRUT\\:formConsultaEstadoRUT\\:formulario'
    element = tab.call_method('DOM.querySelector', nodeId=root_node_id, selector=element_selector)
    element_node_id = element['nodeId']

    outer_html = tab.call_method('DOM.getOuterHTML', nodeId=element_node_id)
    soup = BeautifulSoup(outer_html['outerHTML'], 'html.parser')

    with open('grabbedHTML.html', 'w') as file:
        file.write(soup.prettify())

    print('Element HTML', outer_html['outerHTML'])

except Exception as e:
    print(e)
finally:
    tab.stop()
    browser.close_tab(tab)
