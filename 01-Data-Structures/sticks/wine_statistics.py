import json
from collections import Counter


def get_whole_data(data_1, data_2):
    with open(data_1) as d1, open(data_2) as d2:
        loading_data = json.load(d1)
        loading_data.extend(json.load(d2))

    unique_items_set = set()
    for dict_item in loading_data:
        unique_items_set.add(tuple(dict_item.items()))

    dumping_data = [dict(item) for item in unique_items_set]
    dumping_data.sort(key=lambda item: (0-(item['price'] or 0), item['variety'] or 'z'))

    with open('winedata_full.json', 'w') as d:
        json.dump(dumping_data, d, ensure_ascii=False, indent='\t')

    return dumping_data


def parse_data(data):
    for item in data:
        points = item['points']
        price = item['price']
        variety = item['variety']
        region1 = item['region_1']
        region2 = item['region_2']
        country = item['country']
        yield points, price, variety, region1, region2, country


def create_report_wine_dict(dict_in, *args):
    points, price, variety, reg1, reg2, country = args

    if variety not in dict_in:
        dict_in[variety] = {'points': [],
                            'price': [],
                            'region': [],
                            'country': []}

    if points is not None:
        dict_in[variety]['points'].append(int(points))
    if price is not None:
        dict_in[variety]['price'].append(price)
    if reg1 is not None:
        dict_in[variety]['region'].append(reg1)
    if reg2 is not None:
        dict_in[variety]['region'].append(reg2)
    if country is not None:
        dict_in[variety]['country'].append(country)

    return dict_in


def create_report_country_dict(dict_in, points, price, country):
    if country not in dict_in:
        dict_in[country] = {'points': [],
                            'price': []}

    if points is not None:
        dict_in[country]['points'].append(int(points))
    if price is not None:
        dict_in[country]['price'].append(float(price))

    return dict_in


def get_wine_stat(dict_data):
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


def get_country_stat(dict_data):
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


def get_stat(data):
    report_wine_dict = {}
    report_country_dict = {}
    records = parse_data(data)
    for i in records:
        report_wine_dict = create_report_wine_dict(report_wine_dict, *i)
        report_country_dict = create_report_country_dict(report_country_dict, i[0], i[1], i[5])

    wine_stat = get_wine_stat(report_wine_dict)
    country_stat = get_country_stat(report_country_dict)
    return wine_stat, country_stat


def get_statistics(data):
    most_expensive_wine_set = set([x['variety'] for x in data if x['price'] == data[0]['price']])
    most_expensive_wine = [item for item in most_expensive_wine_set]

    data_without_null_price = list(filter(lambda item: item['price'], data))

    cheapest_wine_set = set([x['variety'] for x in data_without_null_price
                             if x['price'] == data_without_null_price[-1]['price']])
    cheapest_wine = [item for item in cheapest_wine_set]

    data.sort(key=lambda item: item['points'] or 0)

    highest_score_set = set([x['variety'] for x in data if x['points'] == data[-1]['points']])
    highest_score = [item for item in highest_score_set]

    lowest_score_set = set([x['variety'] for x in data if x['points'] == data[0]['points']])
    lowest_score = [item for item in lowest_score_set]

    most_active_commentator = Counter(
        item['taster_name'] for item in data if item['taster_name'] is not None).most_common(1)[0][0]

    wine_stat_dict = get_stat(data)[0]
    country_stat_dict = get_stat(data)[1]

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