function toggle_description(button_id) {
    let descriptor_id = button_id + "-description";
    button = document.getElementById(button_id)
    if (button == null) { return; }
    console.log(button);
    buttons = document.getElementsByClassName("vertical-list-button");
    for (let i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("selected");
    }
    button.classList.toggle("selected")
    descriptors= document.getElementsByClassName("vertical-description");
    for (let i = 0; i < descriptors.length; i++) {
        descriptors[i].style.display = "none";
    }
    descriptor = document.getElementById(descriptor_id);
    descriptor.style.display = "block";
}

function on_load() {
    selected_id = document.getElementById("selected").value;
    console.log(selected_id);
}

document.onload = on_load();