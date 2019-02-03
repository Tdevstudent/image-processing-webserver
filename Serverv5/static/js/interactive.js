/* Not my proudest work ever. */
/* Could be improved greatly by refactoring using promises */

function onImageInputSelect(type) {
    // uncheck other box
    if(type == "own") {
        document.getElementById("presetSelect").checked = false;
        document.getElementById("ownSelect").checked = true;
    }
    if(type == "preset") {
        document.getElementById("ownSelect").checked = false;
        document.getElementById("presetSelect").checked = true;
    }
}

function readInputImage(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("input_image").setAttribute('src', e.target.result);
            document.getElementById("input_image").setAttribute("width", "45%");
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function loadPresets() {
    var request = new XMLHttpRequest();
    var url = '/api/preset_names/';
    request.open('GET', url);
    request.send();
    request.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            preset_images = JSON.parse(request.responseText);
            var htmlstr = '';
            for (index in preset_images) {
                htmlstr += "<option value =\"" + preset_images[index]+ "\">" + preset_images[index] + "</option>";
            }
            document.getElementById("presets").innerHTML = htmlstr;

            document.getElementById("input_image").setAttribute("src", "../images/presets/" + document.getElementById("presets").value);
            document.getElementById("input_image").setAttribute("width", "45%");
            loadScripts();
        }
    }
}

function loadScripts() {
    var request = new XMLHttpRequest();
    var url = '/api/script_names/';
    request.open('GET', url);
    request.send();
    request.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            scripts = JSON.parse(request.responseText);
            var htmlstr = "";
            for (index in scripts) {
                htmlstr += "<option value =\"" + scripts[index]+ "\">" + scripts[index] + "</option>";
            }
            document.getElementById("scripts").innerHTML = htmlstr;
            loadArguments();
        }
    }
}

function loadArguments() {
    onScriptSelectionChange();
    onSubmit();
}

function onPresetSelectionChange() {
    document.getElementById("input_image").setAttribute('src', "../images/presets/" + document.getElementById("presets").value);
    document.getElementById("input_image").setAttribute("width", "45%");
}

function onScriptSelectionChange() {
    script = document.getElementById("scripts").value;
    htmlstr = "";
    if(script == "color"){
        htmlstr += "color: <select id=\"color\">";
        htmlstr += "<option value=\"r\">red</option>";
        htmlstr += "<option value=\"b\">blue</option>";
        htmlstr += "<option value=\"g\">green</option>";
        htmlstr += "</select>"

    } else {
        htmlstr += "JSON arguments: <input type=\"file\" name=\"json\" id=\"jsonpicker\" accept=\".json\">";
    }
    document.getElementById("args").innerHTML = htmlstr;
}

function sendRequest(script, image, preset, data) {
    var request = new XMLHttpRequest();
    var url = '/api/';
    var payload = {script:script, image:image, preset:preset};
    for (i in data) {
        payload[i] = data[i];
    }
    request.open('POST', url);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(json=JSON.stringify(payload));
    request.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("output_image").setAttribute('src', request.responseText);
        }
    }
}

async function onSubmit(){
    script = document.getElementById("scripts").value;
    if(document.getElementById("presetSelect").checked){
        preset = "true";
        image = document.getElementById("presets").value;
    }

    if(document.getElementById("ownSelect").checked){
        preset = "false";
        image = await uploadImage();
    }

    if(script == "color"){
        color = document.getElementById("color").value;
        args = {"color": color};
        sendRequest(script, image, preset, args);
    } else {
        json = document.getElementById("jsonpicker");

        if (json.files && json.files[0]) {
            var reader = new FileReader();
            reader.readAsText(json.files[0], 'UTF-8');
            reader.onload = function (e) {
                args = JSON.parse(e.target.result);
                sendRequest(script, image, preset, args);
            };
        }
    }
}

async function uploadImage() {
    return new Promise(function(resolve, reject) {
        var request = new XMLHttpRequest();
        var url = '/api/upload_image/';
        var formData = new FormData();
        formData.append("image", document.getElementById("filepicker").files[0]);
        request.open('POST', url);
        request.setRequestHeader("Accept", "multipart/form-data");
        request.send(formData);
        request.onreadystatechange = function(){
            if (this.readyState == 4 && this.status == 200) {
                resolve(request.responseText);
            }
        }
    });

}
loadPresets();
