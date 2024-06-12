import aiohttp
from database.main_db import sql_get_coordinates_shores
from config import BOT_TOKEN, YANDEX_MAPS_API


async def get_photo_url(file_key):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile"
    params = {"file_id": file_key}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                file_path = data["result"]["file_path"]
                photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                return photo_url
            else:
                return None


async def start_map():
    coordinates_with_descriptions_photos = await sql_get_coordinates_shores()
    js_points = ""
    for (
        coord,
        description,
        file_key,
        destruction,
        activated,
    ) in coordinates_with_descriptions_photos:
        latitude, longitude = coord.split(", ")
        if activated == 0:
            continue
        photo_url = await get_photo_url(file_key)
        if photo_url:
            js_points += f"{{coordinates: [{latitude}, {longitude}], description: \
                '{description}', photo: '{photo_url}', destruction: {destruction}}},\n"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <title>Yandex Maps Integration</title>
        <script src="https://api-maps.yandex.ru/2.1/?apikey={YANDEX_MAPS_API}&lang=ru_RU" type="text/javascript"></script>
        <style>
            #map {{
                width: 100%;
                height: 600px;
                margin: 0 auto;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>

        <script>
            document.addEventListener("DOMContentLoaded", function () {{
                ymaps.ready(initMap);
            }});

            function initMap() {{
                var myMap = new ymaps.Map("map", {{
                    center: [47.222078, 39.720358],
                    zoom: 10
                }});

                var points = [
                    {js_points}
                ];

                points.forEach(function (point) {{
                    var marker = new ymaps.Placemark(point.coordinates, {{
                        balloonContent: '<div><img src="' + point.photo + '" style="width: 200px;\
                            height: auto;"><br>' + point.description + '<br>Разрушенность: ' + point.destruction + '%</div>'
                    }});
                    myMap.geoObjects.add(marker);
                }});
            }}
        </script>
    </body>
    </html>
    """

    with open("map_with_points.html", "w", encoding="utf-8") as f:
        f.write(html_content)
