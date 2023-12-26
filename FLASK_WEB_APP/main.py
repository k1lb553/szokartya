#mivel a website-on belül van __init__.py, ezért a benne lévő fájlok funkcióit egyből lehet importálni
from website import create_app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)  # debug ==> folytonosan updateli a python kóddal a websiteot
