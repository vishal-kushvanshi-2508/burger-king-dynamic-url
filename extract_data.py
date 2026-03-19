
import os

from lxml import html
import json
import requests

def read_html_content(file_name):
    current_working_dir = os.getcwd()
    file_path = f"{current_working_dir}/{file_name}"
    with open(file_path, "r", encoding='utf-8') as f :
        html_content = f.read()
    return html_content

#
def extract_data_from_html(html_content):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://stores.burgerking.in/location/haryana',
        'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        # 'cookie': '_gcl_au=1.1.1121010527.1773899531; _gid=GA1.2.362445554.1773899533; _ga=GA1.1.1502612679.1773408617; _fbp=fb.1.1773899532647.25529123894767585; moe_uuid=005a9800-88e6-414a-9244-ee3bf6b15efa; _ga_51NSXH673Q=GS2.1.s1773899532$o1$g0$t1773899534$j58$l0$h0; _ga_CRJBK2R8LM=GS2.1.s1773899532$o1$g0$t1773899534$j58$l0$h0; _ga_KQE6QVSPD1=GS2.1.s1773899540$o2$g1$t1773899821$j34$l0$h0',
    }


    tree = html.fromstring(html_content)
    ## list of HTML element objects which is matching with h1 tag.

    state_list = tree.xpath("//ul[@class='list-unstyled search-location']//select[@name='state']//option[@value!='']/text()")
        
    base_url = "https://stores.burgerking.in/location/"

    ## get all state name and website link .
    print("total states : ", len(state_list))
    state_info = []
    for state_name in state_list:
        state_dict_data = {}
        lower_state_name = state_name.lower().replace(" ", "-")
        
        state_dict_data["state_name"] = state_name
        state_dict_data["website_link"] = f"{base_url}{lower_state_name}#searchAdvance"
        state_info.append(state_dict_data)

    ## store state data in json file.
    with open("state_info.json", "w") as f:
        json.dump(state_info, f)

    ## get all state name, city name and website link .
    all_city_list = []
    for state in state_info:
        state_name = state.get("state_name").lower().replace(" ", "-")
        state_url = state.get("website_link")
        response = requests.get(state_url, headers=headers)

        city_tree = html.fromstring(response.text)
        city_list = city_tree.xpath("//ul[@class='list-unstyled search-location']//select[@name='city']//option[@value!='']/text()")

        for city_name in city_list:
            city_dict_data = {}
            lower_state_name = city_name.lower().replace(" ", "-")
            
            city_dict_data["state_name"] = state_name
            city_dict_data["city_name"] = city_name
            city_dict_data["website_link"] = f"{base_url}{state_name}/{lower_state_name}#searchAdvance"
            all_city_list.append(city_dict_data)

    ## store city data in json file.
    with open("city_info.json", "w") as f:
        json.dump(all_city_list, f)

    print("total city : ", len(all_city_list))


    # ## check all city url is right or not .
    # print("request done..")
    # url_headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    #     "Accept-Language": "en-US,en;q=0.9",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    #     "Referer": "https://www.google.com/",
    #     "Connection": "keep-alive"
    # }

    # not_right_url = []
    # for city in all_city_list:
    #     # state_name = state.get("state_name").lower().replace(" ", "-")
    #     city_url = city.get("website_link")
    #     # response = requests.get(state_url, headers=headers)

    #     response = requests.get(city_url, headers=url_headers)
    #     # print(response.status_code)
    #     if response.status_code != 200:
    #         print(response.status_code)
    #         not_right_url.append(city_url)
    #         print("yes requese done now .")
    # print(not_right_url)
    # print(len(not_right_url))



    return all_city_list
