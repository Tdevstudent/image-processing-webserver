import json
import os
import subprocess

from imghdr import what
from flask import abort, send_from_directory

import config
import input_handler

import matlab.engine

# documentation


def documentation(app):
    """
    returns the documentation zip file
    """
    app.logger.debug("documentation requested")
    return send_from_directory(config.documentation_folder, "Documentation.7z")


# names

def preset_names(app):
    """
    returns a list of preset names
    """
    app.logger.debug("preset names requested")
    return json.dumps(os.listdir(config.preset_folder))


def script_names(app):
    """
    returns a list of script names
    """
    app.logger.debug("preset names requested")
    return json.dumps(list(config.scripts.keys()))

# images


def preset_image(app, filename):
    app.logger.debug("preset image requested: " + filename)
    """
    returns a requested preset image
    """
    return send_from_directory(config.preset_folder, filename)


def output_image(app, filename):
    app.logger.debug("output image requested: " + filename)
    """
    returns a requested output image
    """
    return send_from_directory(config.output_folder, filename)


def upload_image(app, request):
    """
    stores an image in the input folder
    """
    app.logger.debug("Received files: " + str(request.files))
    if 'image' not in request.files:
        # 400: Bad request
        abort(400, "Image not found")

    file = request.files['image']
    ext = "." + what(file)
    if ext in config.allowed_filetypes:
        file_name = input_handler.filename_get_random() + ext
        file.save(config.input_folder + file_name)
        return file_name
    else:
        # 415 Unsupported Media Type
        abort(415, "Unsupported image format")


def remove_image(app, request):
    """
    removes a specified image from the input folder
    """
    # load json
    valid_json, args, errors = input_handler.json_load_from_request(request)

    if not valid_json:
        # 400: Bad request
        abort(400, errors[0])

    # see if data is present and valid
    has_fields, errors = input_handler.json_has_fields(args, ["image"])
    if not has_fields:
        # 400: Bad request
        abort(400, errors[0])
    image_name = args['image']

    # invalid filename
    valid, error = input_handler.filename_is_valid(image_name)
    if(not valid):
        # 400: Bad request
        abort(400, error)

    # remove image
    path = config.input_folder + image_name
    if(os.path.exists(path)):
        os.remove(path)
    return "image removed"


def api(app, request, engine):
    """
    processes a specified image with a specified script and returns the resulting image
    """
    # load json
    valid_json, args, errors = input_handler.json_load_from_request(request)

    if not valid_json:
        # 400: Bad request
        abort(400, errors[0])

    # see if data is present and valid
    has_fields, errors = input_handler.json_has_fields(args, ["script", "image", "preset"])
    if not has_fields:
        # 400: Bad request
        abort(400, errors[0])

    if(args["script"] not in config.scripts):
        # 400: Bad request
        abort(400, "Invalid script")

    if(not isinstance(args["preset"], str) or str.lower(args["preset"]) not in ["true", "false"]):
        # 400: Bad request
        abort(400, "Preset should be either true or false")

    if not isinstance(args["image"], str):
        # 400: Bad request
        abort(400, "Image should be a string")
    image_name = args["image"]

    if str.lower(args["preset"]) == "true":
        if image_name not in os.listdir(config.preset_folder):
            # 400: Bad request
            abort(400, "preset image not found")
    else:
        valid_name, error = input_handler.filename_is_valid(image_name)
        if not valid_name:
            # 400: Bad request
            abort(400, error)

    script_path = config.scripts_folder + config.scripts[args["script"]]

    # generate json path name
    id = input_handler.filename_get_random()
    json_name = id + ".json"
    input_json_path_abs = os.path.abspath(config.input_folder + json_name)

    # save json arguments
    file = open(input_json_path_abs, 'w')
    file.write(json.dumps(args))
    file.close()

    # set image input and output paths using image name
    if str.lower(args["preset"]) == "true":
        input_image_path_abs = os.path.abspath(config.preset_folder + image_name)
    else:
        input_image_path_abs = os.path.abspath(config.input_folder + image_name)
    output_image_path_abs = os.path.abspath(config.output_folder + image_name)
    
    # call algorithm with paths and retrieve output image
    try:
        if(args["script"] in config.python_scripts):
            algorithm_args = config.python_path + [script_path,
                                                  input_image_path_abs,
                                                  input_json_path_abs,
                                                  output_image_path_abs]
            app.logger.debug("Calling algorithm color: " + str(algorithm_args))
            subprocess.call(algorithm_args)
        elif args["script"] in config.matlab_scripts:
            getattr(engine, config.scripts[args["script"]])(input_image_path_abs, input_json_path_abs, output_image_path_abs, nargout=0)

        # rename output image (to keep having same name as input image is bad)
        image_name = id + "." + what(output_image_path_abs)
        os.rename(output_image_path_abs, config.output_folder + image_name)
    except Exception as e:
        # 400: Bad request
        app.logger.debug(str(e))
        abort(400, "execution failed")

    # remove json input file
    if(not config.keep_json):
        os.remove(config.input_folder + json_name)

    # return processed image
    app.logger.debug("sending file location: " + "/images/output/" + image_name)
    return "/images/output/" + image_name
