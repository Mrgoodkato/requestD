import pychrome
from bs4 import BeautifulSoup

def chrome_handle(cedula: str):
    url = 'https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces'
    # Connect to the running Chrome instance
    browser = pychrome.Browser(url="http://127.0.0.1:9223")  # Default debug port

    tab = browser.new_tab()

    # For further logging uncomment these:
    """
    def request_will_be_sent(**kwargs):
        print('loading: %s'  % kwargs.get('request').get('url'))

    tab.set_listener('Network.requestWillBeSent', request_will_be_sent)
    """

    try:
        tab.start()
        tab.call_method('Network.enable')
        tab.call_method('Page.navigate', url=url, timeout=5)

        tab.wait(5)
        input_js = f"document.getElementById('vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit').value = '{cedula}'"
        tab.Runtime.evaluate(expression=input_js)
        print(f'Cedula proporcionada: {cedula}')

        button_js = "document.getElementById('vistaConsultaEstadoRUT:formConsultaEstadoRUT:btnBuscar').click()"
        tab.Runtime.evaluate(expression=button_js)
        print(f'Boton de busqueda activado en {url}')
        tab.wait(5)

        root = tab.call_method('DOM.getDocument')
        root_node_id = root['root']['nodeId']

        element_selector = '#vistaConsultaEstadoRUT\\:formConsultaEstadoRUT\\:formulario'
        element = tab.call_method('DOM.querySelector', nodeId=root_node_id, selector=element_selector)
        element_node_id = element['nodeId']

        outer_html = tab.call_method('DOM.getOuterHTML', nodeId=element_node_id)
        soup = BeautifulSoup(outer_html['outerHTML'], 'html.parser')

        with open(f'documents/{cedula}.html', 'w') as file:
            file.write(soup.prettify())

        print(f'Archivo {cedula}.html guardado en la carpeta -documents-')

    except Exception as e:
        print(e)
    finally:
        tab.stop()
        browser.close_tab(tab)
