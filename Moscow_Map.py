import folium
from folium.plugins import MarkerCluster
from pymongo import MongoClient
import pandas as pd
from branca.colormap import StepColormap
from datetime import date


def load_data():
    client = MongoClient('localhost', 27017)
    db = client['burgerking_rivals']
    bk = db.burgerking_rivals
    cursor = bk.find({'brand': 'burgerking'})
    df = pd.DataFrame(list(cursor))
    df = pd.concat([df.drop('location', axis=1), pd.json_normalize(df['location'])], axis=1)
    df[['longitude', 'latitude']] = pd.DataFrame(df['coordinates'].tolist())
    df['comment'] = df['brand'].astype(str) + '\n' + df['address'].astype(str) + \
                    '\nКонкурентов: ' + df['n_rivals'].astype(str)
    df = df.drop(['type', 'city', '_id'], axis=1)
    client.close()
    return df


def color_change(n_rivals):
    if n_rivals == 0:
        return 'green'
    elif 0 < n_rivals <= 4:
        return 'blue'
    elif 4 < n_rivals <= 8:
        return 'orange'
    else:
        return 'red'


def create_map():
    df = load_data()
    latitude = df['latitude']
    longitude = df['longitude']
    popups = df['comment']
    n_rivals = df['n_rivals']
    vmax = df['n_rivals'].max()
    m = folium.Map(location=[55.7522, 37.6156])
    marker_cluster = MarkerCluster()
    marker_cluster.add_to(m)
    folium.LayerControl().add_to(m)
    for lat, lon, popup, n_rival in zip(latitude, longitude, popups, n_rivals):
        if 'Калейдоскоп' in popup:
            popup = 'burgerking\nг.Москва, Химкинский бульвар, д. 7/23 ТЦ Калейдоскоп, 4 этаж\nКонкурентов: 3'
        folium.Marker(location=[lat, lon],
                      popup=popup,
                      icon=folium.Icon(color=color_change(n_rival))).add_to(marker_cluster)
    colormap = StepColormap(['green', 'blue', 'orange', 'red'],
                            vmin=0,
                            vmax=vmax,
                            index=[0, 1, 4, 8, vmax]
                            ).scale(0, vmax)
    today = date.today()
    colormap.caption = f'Количество конкурентов ({today.strftime("%B, %Y")})'
    colormap.add_to(m)
    m.save("Moscow_Map.html")


if __name__ == '__main__':
    create_map()
    print('Done')
