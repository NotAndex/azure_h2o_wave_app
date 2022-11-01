# from h2o_wave import main, app, Q, ui

# #if __name__ == "__main__":
# @app('/')
# async def serve(q: Q):
#     # Modify the page
#     q.page['qux'] = ui.markdown_card(
#     box='1 1 2 2',
#     title='Hello World',
#     content='"The Internet? Is that thing still around?" - *Homer Simpson* test',)

#     # Save the page
#     await q.page.save()

# Image / Stream
# Display an image and continuously update it in real time.
# ---
import io
import time
import uuid

import cv2
from h2o_wave import app, Q, ui, main
import numpy as np


def create_random_image(bgr):
    frame = np.zeros((512, 512, 3), dtype=np.uint8)
    frame[0:-1, 0:-1] = bgr
    _, img = cv2.imencode('.jpg', frame)
    return io.BytesIO(img)

@app('/demo')
async def serve(q: Q):
    # Mint a unique name for our image stream
    stream_name = f'stream/demo/{uuid.uuid4()}.jpeg'

    # Send image
    endpoint = await q.site.uplink(stream_name, 'image/jpeg', create_random_image([255, 0, 0]))

    # Display image
    q.page['qux'] = ui.form_card(box='1 1 4 7', items=[ui.image('Image Stream', path=endpoint)])
    await q.page.save()

    i = 0

    try:
        while True:
            time.sleep(5)

            d = {
                0: [[255, 0, 0], 'Blue'], 
                1: [[0, 255, 0], 'Green'], 
                2: [[0, 0, 255], 'Red'], 
                }

            print(f'{i} -> {d[i][1]}')

            # Send image (use stream name as before).
            await q.site.uplink(stream_name, 'image/jpeg', create_random_image(d[i][0]))
            #await q.site.uplink(stream_name, 'image/jpeg', create_random_image(d[i][0]))

            i+=1
            if i == 3:
                i = 0
    except:
        KeyboardInterrupt

    await q.site.unlink(stream_name)