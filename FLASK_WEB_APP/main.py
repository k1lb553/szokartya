from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True) #debug ==> folytonosan updateli a python kóddal a websiteot
 