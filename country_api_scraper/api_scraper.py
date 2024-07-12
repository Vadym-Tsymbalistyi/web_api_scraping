import requests
from prettytable import PrettyTable
import json


class CountryData:
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()

    def get_table_data(self):
        data = self.fetch_data()
        table = PrettyTable()
        table.field_names = ["Country Name", "Capital Name", "Flag URL (PNG)"]

        table_data = []

        for country in data:
            country_name = country.get('name', {}).get('common', 'N/A')
            capital_name = country.get('capital', ['N/A'])[0]
            flag_url = country.get('flags', {}).get('png', 'N/A')
            table.add_row([country_name, capital_name, flag_url])
            table_data.append({
                "Country Name": country_name,
                "Capital Name": capital_name,
                "Flag URL (PNG)": flag_url
            })
        print(table)
        return table_data


if __name__ == "__main__":
    api_url = "https://restcountries.com/v3.1/all"
    country_data = CountryData(api_url)
    table_data = country_data.get_table_data()

    with open('table.json', 'w', encoding='utf-8') as f:
        json.dump(table_data, f, ensure_ascii=False, indent=4)
