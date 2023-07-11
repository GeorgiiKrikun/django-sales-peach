all_options=[];

/*
Remove options from service selector that do not  correspond to company_left
If company_left is null, remove all options
*/

function selectFirstOption() {
    service_selector = document.getElementById("service_name");
    options = service_selector.children;
    if (options.length != 0) {
        options[0].selected = true;
    }
}

function removeServiceOptions( company_left ) {
    service_selector = document.getElementById("service_name");
    //get childer of option class
    options = service_selector.children;
    for (var i = options.length - 1 ; i >=0 ; i--) {
        if (options[i].getAttribute("additional") != company_left) {
            options[i].remove();
        }
    }
    selectFirstOption();
}

function resetServiceOptions() {
    removeServiceOptions(null);
    service_selector = document.getElementById("service_name");
    for (var i = 0; i < all_options.length; i++) {
        service_selector.appendChild(all_options[i]);
    }
    selectFirstOption();
}

function onCompanyChanged() {
    resetServiceOptions();      
    company_selector = document.getElementById("company_name");
    company_left = company_selector.value;
    resetServiceOptions();
    console.log(company_left);
    removeServiceOptions(company_left);
}

function on_load() {
    company_selector = document.getElementById("company_name");
    company_selector.addEventListener("change", onCompanyChanged);
    service_selector = document.getElementById("service_name");
    service_options = service_selector.children;
    all_options=[];
    for (var i  = 0; i < service_options.length; i++) {
        all_options.push(service_options[i]);
    }

    onCompanyChanged();
}

document.onload = on_load();