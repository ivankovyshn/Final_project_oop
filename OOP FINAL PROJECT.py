import requests
from bs4 import BeautifulSoup
import json

class CurrencyConverter:
    def __init__(self):
        self.url = "https://minfin.com.ua/currency/"
        self.data = None

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            currency_elements = soup.find_all(
                "script",
                {
                    'data-react-helmet': 'true',
                    'type': "application/ld+json"
                }
            )
            data = currency_elements[1].text

            data = data.replace("'", '"')


            data = json.loads(data)
            self.data = data['itemListElement']

    def convert_currency(self, currency_code):
        if self.data is None:
            print("Дані не було завантажено. Спробуйте ще раз.")
            return

        found_currency = False

        for d in self.data:
            if d['name'] == 'Курс НБУ' and d['currency'] == currency_code:
                print(f"1 {currency_code} ≈ {d['currentExchangeRate']['price']} {d['currentExchangeRate']['priceCurrency']}")
                found_currency = True
                break



    def run(self):
        self.fetch_data()

        while True:
            currency_code = input("Введіть курс валюти, який би ви хотіли переглянути (PLN, USD, EUR): ").strip().upper()
            self.convert_currency(currency_code)
            choice = input("Бажаєте продовжити (Y/N)? ").strip().upper()
            if choice == "N":
                break

converter = CurrencyConverter()
converter.run()
