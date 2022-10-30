from h2o_wave import site, ui


def main():
# Grab a reference to the page at route '/hello'
    page = site['/']

    # Add a markdown card to the page.
    page['quote'] = ui.markdown_card(
        box='1 1 2 2',
        title='Hello World',
        content='"The Internet? Is that thing still around?" - *Homer Simpson* a',
    )

    # Finally, save the page.
    page.save()

if __name__ == "__main__":
    main()
