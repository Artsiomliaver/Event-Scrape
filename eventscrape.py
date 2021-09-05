import json
import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import xlsxwriter
import time


def get_leaves(item, key=None):
    if isinstance(item, dict):
        leaves = []
        for i in item.keys():
            leaves.extend(get_leaves(item[i], i))
        return leaves
    elif isinstance(item, list):
        leaves = []
        for i in item:
            leaves.extend(get_leaves(i, key))
        return leaves
    else:
        return [(key, item)]


def main():
    event_id = input("Please event ID : ")
    s = requests.Session()

    HEADER = {
        "accept": "application/json, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        # "referer": "https://www.trisignup.com/Race/Results/24568"
        "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    params = dict(
        resultSetId= 263364,
        page= 1,
        num= 5000,
        search=""
    )
    event_url = "https://www.trisignup.com/Race/Results/" + event_id
    r = s.get(event_url, headers=HEADER, params=params)

    if r.status_code == 200:
        result = r.json()
        event_json = result["resultSet"]["results"]
        headings = result["headings"]
        # df = pd.DataFrame(event_json)
        # df.to_excel(excel_writer="output.xlsx")
        excel_file = time.strftime("%Y%m%d%H%M%S") + ".xlsx"
        row = 0
        workbook = xlsxwriter.Workbook(excel_file)
        worksheet = workbook.add_worksheet()
        header_format = workbook.add_format({
            'bold': True,
            'fg_color': '#FE9423',
            'border': 1})
        for col_num, value in enumerate(headings):
            worksheet.write(0, col_num, value["name"], header_format)

        for col, data in enumerate(event_json):
            worksheet.write_row(col + 1, row, data)

        workbook.close()
        print("done!")
    else:
        print("get error eventID")


if __name__ == "__main__":
    main()
