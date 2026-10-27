import datetime
from aiohttp import web

ads = {}
id_counter = 1


# POST метод должен создавать объявление
async def create_ads(request):
    global id_counter
    data = await request.json()

    # валидация обязательных полей при создании
    if not data.get('title') or not data.get('description') or not data.get('owner'):
        return web.json_response(
            {'error': 'Поля title, description и owner обязательны для заполнения'}, status=400
        )

    new_ad = {
        'id': id_counter,
        'title': data.get('title'),
        'description': data.get('description'),
        'created_at': datetime.datetime.now().isoformat(),
        'owner': data.get('owner')
    }
    ads[id_counter] = new_ad
    id_counter += 1
    return web.json_response(new_ad, status=201)


# GET - получать объявление
async def get_ad(request):
    ad_id = int(request.match_info['ad_id'])
    if ad_id not in ads:
        return web.json_response({'error': 'объявление не найдено'}, status=404)
    return web.json_response(ads[ad_id])


# PATCH - редактировать объявление
async def update_ad(request):
    ad_id = int(request.match_info['ad_id'])
    if ad_id not in ads:
        return web.json_response({'error': 'объявление не найдено'}, status=404)

    data = await request.json()
    ad = ads[ad_id]

    # редактирование полей
    ad['title'] = data.get('title', ad['title'])
    ad['description'] = data.get('description', ad['description'])
    ad['owner'] = data.get('owner', ad['owner'])

    return web.json_response(ad, status=200)


# DELETE - удалять объявление
async def delete_ad(request):
    ad_id = int(request.match_info['ad_id'])
    if ad_id not in ads:
        return web.json_response({'error': 'объявление не найдено'}, status=404)
    del ads[ad_id]
    return web.json_response({'result': 'объявление успешно удалено'}, status=200)

app = web.Application()

app.add_routes([
    web.post('/ads', create_ads),
    web.get(r'/ads/{ad_id:\d+}', get_ad),
    web.patch(r'/ads/{ad_id:\d+}', update_ad),
    web.delete(r'/ads/{ad_id:\d+}', delete_ad)
])


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8090)
