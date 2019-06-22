import json
import re
from collections import Counter


pattern_line = re.compile(r"^\{'points': \'?(?P<points>[^\'\,]+)\'?, "
                          r"'title': \'?[^\'\,]+\'?, "
                          r"'description': \"[^\"]+\", "
                          r"'taster_name': \'?(?P<taster_name>[^\'\,]+)\'?, "
                          r"'taster_twitter_handle': \'?[^\'\,]+\'?, "
                          r"'price': \'?(?P<price>[^\'\,]+)\'?, "
                          r"'designation': \'?[^\'\,]+\'?, "
                          r"'variety': \'?(?P<variety>[^\'\,]+)\'?, "
                          r"'region_1': \'?(?P<region_1>[^\'\,]+)\'?, "
                          r"'region_2': \'?(?P<region_2>[^\'\,]+)\'?, "
                          r"'province': \'?[^\'\,]+\'?, "
                          r"'country': \'?(?P<country>[^\'\,]+)\'?, "
                          r"'winery': \'?[^\,\']+\'?\}$")


def get_whole_data(data_1, data_2):
    with open(data_1) as d1, open(data_2) as d2:
        loading_data = json.load(d1)
        loading_data.extend(json.load(d2))

    unique_items_set = set()
    for dict_item in loading_data:
        unique_items_set.add(tuple(dict_item.items()))

    dumping_data = [dict(item) for item in unique_items_set]
    dumping_data.sort(key=lambda item: (0-(item['price'] or 0), item['variety'] or 'z'))

    full_winedata = 'winedata_full.json'
    with open(full_winedata, 'w') as d:
        json.dump(dumping_data, d, ensure_ascii=False, indent='\t')

    return full_winedata


def create_report_wine_dict(data):
    wine_dict = {}

    for item in data:
        if item["variety"] and item["variety"] != "None" and item["variety"] != 'None':
            if item["variety"] not in wine_dict:
                wine_dict[item["variety"]] = {'points': [],
                                              'price': [],
                                              'region': [],
                                              'country': []}
            if item["points"] is not None:
                wine_dict[item["variety"]]['points'].append(item["points"])
            if item["price"] is not None:
                wine_dict[item["variety"]]['price'].append(item["price"])
            if item["region_1"] is not None and item["region_1"] != "None" and item["region_1"] != 'None':
                wine_dict[item["variety"]]['region'].append(item["region_1"])
            if item["region_2"] is not None and item["region_2"] != "None" and item["region_2"] != 'None':
                wine_dict[item["variety"]]['region'].append(item["region_2"])
            if item["country"] is not None and item["country"] != "None" and item["country"] != 'None':
                wine_dict[item["variety"]]['country'].append(item["country"])

    return wine_dict


def create_report_country_dict(data):
    country_dict = {}

    for item in data:
        if item["country"] and item["country"] != "None" and item["country"] != 'None':
            if item["country"] not in country_dict:
                country_dict[item["country"]] = {'points': [],
                                                 'price': []}

            if item["points"] is not None:
                country_dict[item["country"]]['points'].append(item["points"])
            if item["price"] is not None:
                country_dict[item["country"]]['price'].append(item["price"])

    return country_dict


def get_wine_stat(data):
    dict_data = create_report_wine_dict(data)
    wine_stat_dict = {}
    wines = ['Gewürztraminer', 'Riesling', 'Merlot', 'Madera', 'Tempranillo', 'Red Blend']

    for wine in wines:
        if wine in dict_data:
            wine_stat_dict[wine] = \
                {'avarege_price': round((sum(dict_data[wine]['price'])/len(dict_data[wine]['price']) or 0), 2),
                 'min_price': sorted(dict_data[wine]['price'])[0],
                 'max_price': sorted(dict_data[wine]['price'])[-1],
                 'most_common_region': Counter(dict_data[wine]['region']).most_common(1)[0][0],
                 'most_common_country': Counter(dict_data[wine]['country']).most_common(1)[0][0],
                 'avarage_score': round((sum(dict_data[wine]['points'])/len(dict_data[wine]['points'])), 2)
                 }

    return wine_stat_dict


def get_country_stat(data):
    dict_data = create_report_country_dict(data)
    for item in dict_data:
        dict_data[item]['avg_price'] = (sum(dict_data[item]['price'])/len(dict_data[item]['price'])
                                        if len(dict_data[item]['price']) > 0 else 0)
        dict_data[item]['avg_score'] = sum(dict_data[item]['points']) / len(dict_data[item]['points'])

    avg_price_list = []
    avg_score_list = []

    for item in dict_data:
        avg_price_list.append([dict_data[item]['avg_price'], item])
        avg_score_list.append([dict_data[item]['avg_score'], item])

    avg_price_list.sort()
    avg_score_list.sort()

    most_expensive_country = [i[1] for i in avg_price_list if i[0] == avg_price_list[-1][0]]
    cheapest_country = [i[1] for i in avg_price_list if i[0] == avg_price_list[0][0]]
    most_rated_country = [i[1] for i in avg_score_list if i[0] == avg_score_list[-1][0]]
    underrated_country = [i[1] for i in avg_score_list if i[0] == avg_score_list[0][0]]

    country_stat_dict = \
        {'most_expensive_country': most_expensive_country,
         'cheapest_country': cheapest_country,
         'most_rated_country': most_rated_country,
         'underrated_country': underrated_country
         }

    return country_stat_dict


def parse_item(record):
    match_line = pattern_line.match(record)
    if match_line:
        try:
            points = int(match_line.groupdict()['points'].strip(''""))
        except ValueError:
            points = None
        taster_name = match_line.groupdict()['taster_name'].strip(''"")
        try:
            price = float(match_line.groupdict()['price'].strip(''""))
        except ValueError:
            price = None
        variety = match_line.groupdict()['variety'].strip(''"")
        region_1 = match_line.groupdict()['region_1'].strip(''"")
        region_2 = match_line.groupdict()['region_2'].strip(''"")
        country = match_line.groupdict()['country'].strip(''"")
        return points, taster_name, price, variety, region_1, region_2, country
    return


def read_data_file(file_name):
    with open(file_name) as f:
        for item in json.load(f):
            record_item = parse_item(str(item))
            if record_item:
                yield record_item


def get_statistics(data_file):
    stat_data = []
    records = read_data_file(data_file)
    for i in records:
        stat_data.append({"points": i[0], "taster_name": i[1], "price": i[2], "variety": i[3],
                          "region_1": i[4], "region_2": i[5], "country": i[6]})

    stat_data.sort(key=lambda item: item['price'] or 0, reverse=True)

    most_expensive_wine_set = set([x['variety'] for x in stat_data if x['price'] == stat_data[0]['price']])
    most_expensive_wine = [item for item in most_expensive_wine_set]

    data_without_null_price = list(filter(lambda item: item['price'], stat_data))

    cheapest_wine_set = set([x['variety'] for x in data_without_null_price
                             if x['price'] == data_without_null_price[-1]['price']])
    cheapest_wine = [item for item in cheapest_wine_set]

    stat_data.sort(key=lambda item: item['points'] or 0)

    highest_score_set = set([x['variety'] for x in stat_data if x['points'] == stat_data[-1]['points']])
    highest_score = [item for item in highest_score_set]

    data_without_null_score = list(filter(lambda item: item['points'], stat_data))

    lowest_score_set = set([x['variety'] for x in data_without_null_score if x['points'] == stat_data[0]['points']])
    lowest_score = [item for item in lowest_score_set]

    most_active_commentator = Counter(
        item['taster_name'] for item in stat_data
        if item['taster_name'] and item['taster_name'] != "None" and item['taster_name'] != 'None').most_common(1)[0][0]

    wine_stat_dict = get_wine_stat(stat_data)
    country_stat_dict = get_country_stat(stat_data)

    statictics = {"statistics": {
                    "wine": wine_stat_dict,
                    "most_expensive_wine": most_expensive_wine,
                    "cheapest_wine": cheapest_wine,
                    "highest_score": highest_score,
                    "lowest_score": lowest_score,
                    "most_expensive_country": country_stat_dict["most_expensive_country"],
                    "cheapest_country": country_stat_dict["cheapest_country"],
                    "most_rated_country": country_stat_dict["most_rated_country"],
                    "underrated_country": country_stat_dict["underrated_country"],
                    "most_active_commentator": most_active_commentator
                  }
    }

    return statictics


def render_report(data):
    with open('stats.json', 'w+') as sj:
        json.dump(data, sj, ensure_ascii=False, indent='\t')

    with open('stats.MD', 'w+') as md:
        md.write('## wine statistics: \n')
        md.write("```\n")
        json.dump(data, md, ensure_ascii=False, indent='\t')
        md.write('\n')
        md.write("```")


def main(winedata_1, winedata_2):
    wine_data = get_whole_data(winedata_1, winedata_2)
    wine_report = get_statistics(wine_data)
    render_report(wine_report)


if __name__ == '__main__':
    datafile_1 = 'winedata_1.json'
    datafile_2 = 'winedata_2.json'
    main(datafile_1, datafile_2)
