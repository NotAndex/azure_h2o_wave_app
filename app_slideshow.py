# Image / Stream
# Display an image and continuously update it in real time.
# ---
import io
import contextlib
import time
import uuid

import cv2
from h2o_wave import app, Q, ui, main, site
import numpy as np
import concurrent.futures


def create_random_image(bgr):
    frame = np.zeros((256, 1280, 3), dtype=np.uint8)
    frame[0:-1, 0:-1] = bgr
    _, img = cv2.imencode('.jpg', frame)
    return io.BytesIO(img)
def color_gen():
    i = 0
    color = ['blue','green','red']
    while True:
        yield color[i]
        i += 1
        if i == 3:
            i = 0

def color_gen_1(i):
    color = ['blue','green','red']
    return color[i]

def event_gen():
    i = 0
    color = [0,1,2]
    while True:
        yield color[i]

        i += 1
        if i == 3:
            i = 0
        time.sleep(1)


@app('/demo', mode='broadcast')
async def serve(q: Q):

  
    q.page['header'] = ui.header_card(
    box='1 1 12 1',
    title='My app',
    subtitle='My app subtitle',
    icon='Heart',)

    # Display image
    stream_name = f'stream/demo/{uuid.uuid4()}.jpeg'
    endpoint = site.uplink(stream_name, 'image/jpeg', create_random_image([255, 0, 0]))
    q.page['qux'] = ui.form_card(
        box='1 3 12 3',
        title='Description',
        items=[ui.image('Image Stream', path=endpoint, width='1024')])

    q.page['test'] = ui.small_stat_card(
        box='1 2 1 1',
        title='Color',
        value= f'waiting...',
        )
    await q.page.save()

    event_g = event_gen()


    try:
        while True:

            i = event_g.__next__()
    
            print(i)

            #q.page['test'].value = f'{color_g.__next__()}'
            q.page['test'].value = f'{color_gen_1(i)}'
            await q.page.save()
            d = {
                0: [[255, 0, 0], 'Blue'], 
                1: [[0, 255, 0], 'Green'], 
                2: [[0, 0, 255], 'Red'], 
                }

            print(f'{i} -> {d[i][1]}')
            img = create_random_image(d[i][0])

            # Send image (use stream name as before).
            site.uplink(stream_name, 'image/jpeg', img)
            site.uplink(stream_name, 'image/jpeg', img)

            
            
            

    except:
        KeyboardInterrupt

    await q.site.unlink(stream_name)