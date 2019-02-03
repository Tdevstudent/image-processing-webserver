import datetime

python_path = ["pipenv", "run", "python"]

scripts_folder = r"scripts/"
python_scripts = {"color": "color.py", "zero": "zero.py"}
matlab_scripts = {"flip image":"flip_img"}
scripts = {**python_scripts, **matlab_scripts}

input_folder = r"content/input/"
output_folder = r"content/output/"
preset_folder = r"static/images/presets/"

documentation_folder = r"static/"

filename_length = 16
keep_json = False

allowed_filetypes = ['.bmp', '.jpeg', '.jpg', '.pgm', '.png', '.tif']
max_upload_size = 50 * 10**6  # 50 MB

# Cleaner config

# storage threshold in bytes
# if storage exceeds this value the cleaner will start deleting files
# set to None for no threshold
input_size_threshold = 50 * 10**6  # 50 MB

# age threshold
# if file age exceeds this value the cleaner will start deleting files
# set to None for no threshold
input_age_threshold = datetime.timedelta(days=1, hours=0, minutes=0)
