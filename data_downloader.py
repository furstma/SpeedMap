import argparse
import os
import requests
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser()
parser.add_argument("--eventID", default="20210613H21", type=str, help="Event ID from https://www.gpsseuranta.net/")


def main(args):
    event_folder_path = "Data\{}".format(args.eventID)
    if not os.path.exists(event_folder_path):
        os.makedirs(event_folder_path)

    print("----- Download started ------")

    URL = 'http://www.tulospalvelu.fi/gps/gpx/?eventID={}'.format(args.eventID)
    page = requests.get(URL)

    soap = BeautifulSoup(page.content, 'html.parser')

    runners = soap.find_all('li')

    for runner in runners:
        name = runner.text.strip()
        if name[0:6] == "vakant":
            continue
        link = runner.find('a')['href']
        link = "http://www.tulospalvelu.fi/gps/gpx/{}".format(link)
        gpx = requests.get(link, allow_redirects=True)
        with open(event_folder_path + '/{}.gpx'.format(name), 'wb') as f:
            f.write(gpx.content)

    map_url = "https://www.tulospalvelu.fi/gps/{}/map".format(args.eventID)
    map = requests.get(map_url, allow_redirects=True)
    with open(event_folder_path + '/map.bmp', 'wb') as f:
        f.write(map.content)

    print("----- Event {} (map and {} runners) successfully downloaded ------".format(args.eventID, len(runners)))


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)