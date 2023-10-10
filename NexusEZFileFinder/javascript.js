const MOD_ID = 1;
let FILE_ID = 1;
let BACKUP_FILE_ID = FILE_ID;
let URL_LINK;
let searchingForMods = false;
let tabIndex = 0;

const FIND_MODS_BUTTON = document.getElementById('find-mods-button');
FIND_MODS_BUTTON.addEventListener("click", changeTabFindMods);

const LOG_BUTTON = document.getElementById('log-button');
LOG_BUTTON.addEventListener("click", changeTabLog);

const SEARCH_OPTIONS_BUTTON = document.getElementById('search-options-button');
SEARCH_OPTIONS_BUTTON.addEventListener("click", changeTabSearchOptions);

const HELP_BUTTON = document.getElementById('help-button');
HELP_BUTTON.addEventListener("click", changeTabHelp);

const FIND_DELETED_MODS_BUTTON = document.getElementById('find-deleted-mods-button');
FIND_DELETED_MODS_BUTTON.addEventListener("click", startModSearch);

const TEXT_AREA = document.getElementById("find-mods");
TEXT_AREA.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        if (tabIndex == 0) {
            startModSearch();
        }
    }
});

clearAllTabs();
document.getElementById('find-mods').style.display = "flex";

function clearAllTabs () {
    document.getElementById('find-mods').style.display = "none";
    document.getElementById('text-log').style.display = "none";
    document.getElementById('search-options').style.display = "none";
    document.getElementById('help-text').style.display = "none";
}

function changeTabFindMods() {
    clearAllTabs();
    document.getElementById('find-mods').style.display = "flex";
    tabIndex = 0;
}

function changeTabLog() {
    clearAllTabs();
    document.getElementById('text-log').style.display = "flex";
    document.getElementById('text-log').scrollTop = document.getElementById('text-log').scrollHeight;
    tabIndex = 1;
}

function changeTabSearchOptions() {
    clearAllTabs();
    document.getElementById('search-options').style.display = "flex";
    tabIndex = 2;
}

function changeTabHelp () {
    clearAllTabs();
    document.getElementById('help-text').style.display = "flex";
    tabIndex = 3;
}

function validateURL () {
    if (document.getElementById('url-text').value.includes("https://www.nexusmods.com/" && "/mods/")) {
        document.getElementById('enter-url-text').textContent = "Valid URL entered!";
        return true;
    } else {
        document.getElementById('enter-url-text').textContent = "Invalid URL entered!";
        return false;
    }
}

function createLogElement () {
    URL_LINK = document.getElementById('url-text').value;
    URL_LINK = URL_LINK.concat(`?tab=files&file_id=${FILE_ID}`)
    const a = document.createElement('a');
    const link = document.createTextNode(URL_LINK);
    a.appendChild(link);
    a.target= '_blank';
    a.title = URL_LINK;
    a.href = URL_LINK;
    document.getElementById('text-log').appendChild(a);
    console.log(URL_LINK)
    document.getElementById('text-log').scrollTop = document.getElementById('text-log').scrollHeight;
    FILE_ID += 1;
}

async function asyncCreateLogElement() {
    FILE_ID = BACKUP_FILE_ID;
    for (;; FILE_ID++) {
        if (searchingForMods === true) {
            await new Promise(resolve => setTimeout(resolve, 10));
            createLogElement();
        } else {
            break;
        }
    }
}

function startModSearch() {
    if (validateURL()===true) {
        if (searchingForMods === false) {
            document.getElementById('find-deleted-mods-button').innerHTML = "Stop Searching";
            document.getElementById('url-text').disabled = true;
            searchingForMods = true;
            asyncCreateLogElement();
            
        } else {
            document.getElementById('find-deleted-mods-button').innerHTML = "Find Deleted Mods";
            document.getElementById('url-text').disabled = false;
            searchingForMods = false;
        }
    } else {
        return;
    }
}