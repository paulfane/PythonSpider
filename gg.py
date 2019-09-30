def save_page(page):
    with open("page.txt", "w") as file_stream:
        file_stream.write(str(page))


save_page(2)