function addFile() {    
    var file_div = document.getElementById("file_list")
    var n_files = file_div.childNodes.length
    var new_file = document.createElement("input")
    new_file.setAttribute("type", "file")
    new_file.setAttribute("name", "file " + n_files)
    new_file.setAttribute("id", n_files)
    new_file.setAttribute("class", "form-control")
    file_div.appendChild(new_file)
}

function removeFile() {    
    var file_div = document.getElementById("file_list")
    var inputs = file_div.childNodes
    file_div.removeChild(inputs[inputs.length - 1])
}