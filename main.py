
from extract_data import *

import time

from store_data_database import *
import requests

file_name = "Burger King Locator _ Ahmedabad _ Fast Food Restaurant.html"

def main():
    create_table()
    print("table and db create")
    html_content = read_html_content(file_name)
    burger_list = extract_data_from_html(html_content)
    insert_data_in_table(list_data=burger_list)
    

if __name__ == "__main__":
    start = time.time()
    main()

    end = time.time()
    print("time different  : ", end - start)





