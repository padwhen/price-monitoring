import requests
from bs4 import BeautifulSoup
from pony import orm
from datetime import datetime

db = orm.Database()
db.bind(provider='sqlite', filename='products.db', create_db = True)

class Product(db.Entity):
    name = orm.Required(str)
    price = orm.Required(float)
    created_date = orm.Required(datetime)

db.generate_mapping(create_tables = True)

def zalando(session):
    url = "https://www.zalando.fi/dr-martens-jadon-tech-platform-nilkkurit-black-do211n0bf-q11.html"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = (
        "zalando",
        float(soup.select_one("span.sDq_FX._4sa1cA.dgII7d.Km7l2y").text.replace('€','').replace(',','.').strip()),
    )
    return data

def stockmann(session):
    url = "https://www.stockmann.com/dr.-martens-jadon-tech-platform--nahkamaiharit/15825684333-1.html"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = (
        "stockmann",
        float(soup.select_one("span.value").text.replace('€','').replace(',','.').strip()),
    )
    return data

def drmartens(session):
    url = "https://www.drmartens.com/eu/en_eu/jadon-tech-platform-boots-black/p/30985001"
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    data = (
        "drmartens",
        float(soup.select_one("p.bfx-price").text.replace('€','').strip()),
    )
    return data



def main():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76'
    })
    data = [
        zalando(session),
        stockmann(session),
        drmartens(session)
    ]
    print(data)
    with orm.db_session:
        for item in data:
            Product(name=item[0], price=item[1], created_date=datetime.now())


if __name__ == "__main__":
    main()