Running the server:

for testing (ctrl-c to close server):
pipenv run python Server.py

for running the server even if you log out:
(nohup pipenv run python Server.py &)
logout

Configuration:

Do not store important files in content/input or content/output or risk them being removed by the cleaner.

Preset images are public domain: https://homepages.cae.wisc.edu/~ece533/images/

A lot of the configuration is documented in config.py.
 
If a different folder needs to contain data, configure it there.
Server memory configurations can also be found there.

When installing this in another virtual environment, make sure to install matlab engine for python as well as the dependencies in the pipfile.

Website:

Algorithm specific information can be added by modifying or adding web pages.
Lorem Ipsum example pages are present.
 
To modify pages on the website, edit the html templates in static/templates.
Adding a new %PAGE%.html requires a new template as well as a corresponding call in Server.py

@app.route('%PAGE%', methods=["GET"])
def api_%PAGE%():
    return render_template('%PAGE%.html')

To add support for new image algorithms in the interactive webpage, modify interactive.js and interactive.html. Feel free to rewrite code using promises for improved clarity.

Scripts:

To add a python or matlab script, make sure it creates an image at the output path (see example scripts) and put it in the /scripts/ folder. Then add an entry for it in the config.py dictionary for it to be usable by the server. Again, example entries are present here.
