from h2o_wave import main, app, Q, ui

#if __name__ == "__main__":
@app('/')
async def serve(q: Q):
    # Modify the page
    q.page['qux'] = ui.markdown_card(
    box='1 1 2 2',
    title='Hello World',
    content='"The Internet? Is that thing still around?" - *Homer Simpson*',)

    # Save the page
    await q.page.save()

