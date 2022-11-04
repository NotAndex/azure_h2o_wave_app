# Image / Stream
# Display an image and continuously update it in real time.
# ---

import time
import uuid
import json

from h2o_wave import app, Q, ui, main


def read_json(path: str):
    with open(path) as json_file:
        return json.load(json_file)

def yield_image(path: str):
    with open(path, 'rb') as f:
        byte_img = f.read()
    return byte_img


@app('/demo', mode='broadcast')
async def serve(q: Q):

    q.page['header'] = ui.header_card(
        box='1 1 12 1',
        title='My app',
        subtitle='My app subtitle',
        icon='Heart',)

    # Display image
    stream_name = f'stream/demo/{uuid.uuid4()}.jpeg'
    img1_path = read_json('./data/meta_data/1.json')['img1']['path']
    endpoint = await q.site.uplink(stream_name, 'image/jpeg', yield_image(img1_path))
    q.page['img1'] = ui.form_card(
        box='1 3 12 3',
        title='Description',
        items=[ui.image('Image Stream', path=endpoint, width='1024')])

    stream_name_2 = f'stream/demo/{uuid.uuid4()}.jpeg'
    img2_path = read_json('./data/meta_data/1.json')['img2']['path']
    endpoint = await q.site.uplink(stream_name_2, 'image/jpeg', yield_image(img2_path))
    q.page['img2'] = ui.form_card(
        box='1 6 12 3',
        title='Description',
        items=[ui.image('Image Stream', path=endpoint, width='1024')])


    q.page['stat_1'] = ui.small_stat_card(
        box='1 2 1 1',
        title='Stat 1',
        value= f'waiting...',
        )
    await q.page.save()

    i = 0

    try:
        while True:
            time.sleep(5)

            
            event_list = [
                './data/meta_data/1.json',
                './data/meta_data/2.json']

            d = read_json(event_list[i])
            print(event_list[i])


            img1_path = d['img1']['path']
            img1_stat_1 = d['img1']['stats']['stat_1']
            img2_path = d['img2']['path']
            q.page['stat_1'].value = f'{img1_stat_1}'

            print(img1_path)
            print(img2_path)


            img = yield_image(img1_path)
            img2 = yield_image(img2_path)

            
            # Send image (use stream name as before).

            await q.site.uplink(stream_name, 'image/jpeg', img)
            await q.site.uplink(stream_name, 'image/jpeg', img)

            await q.site.uplink(stream_name_2, 'image/jpeg', img2)
            await q.site.uplink(stream_name_2, 'image/jpeg', img2)

            await q.page.save()
            # await q.page.save()
            
            i+=1

            if i == 2:
                i = 0
    except:
        KeyboardInterrupt

    await q.site.unlink(stream_name)