# import brotli
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
if __name__ == "__main__":
    session = requests.session()

    web = session.get("https://www.cwa.gov.tw/V8/C/D/MOD/UVIHistory/202308_N.html?ID=213")
    cont = "{}{}{}".format("<table>", web.text, "</table>")
    with open("web2.html", 'w', encoding=web.encoding) as f:
        f.write(cont)

    table = bs(cont, features='lxml').find('table')

    print(table)
    df = pd.read_html(str(table))
    print(df)