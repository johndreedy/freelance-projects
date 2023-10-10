const GAME_ID = "skyrimspecialedition";
const MOD_ID = 100562;
let FILE_ID = 1;
let BACKUP_FILE_ID = FILE_ID;
let URL_LINK = `https://www.nexusmods.com/${GAME_ID}/mods/${MOD_ID}?tab=files&file_id=${FILE_ID}`
let searchingForMods = false;

function createLogElement () {
    const a = document.createElement('a');
    const link = document.createTextNode(URL_LINK);
    a.appendChild(link);
    a.title = URL_LINK;
    a.href = URL_LINK;
    document.getElementById('text-log').appendChild(a);
    URL_LINK = `https://www.nexusmods.com/${GAME_ID}/mods/${MOD_ID}?tab=files&file_id=${FILE_ID + 1}`;
    console.log(URL_LINK)
    document.getElementById('text-log').scrollTop = document.getElementById('text-log').scrollHeight;
}

async function asyncCreateLogElement() {
    FILE_ID = BACKUP_FILE_ID;
    for (; FILE_ID < 1000; FILE_ID++) {
        if (searchingForMods === true) {
            await new Promise(resolve => setTimeout(resolve, 10));
            createLogElement();
        } else {
            break;
        }
    }
}

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

function clearAllTabs () {
    document.getElementById('find-mods').style.display = "none";
    document.getElementById('text-log').style.display = "none";
    document.getElementById('search-options').style.display = "none";
    document.getElementById('help-text').style.display = "none";
}

function changeTabFindMods() {
    clearAllTabs();
    document.getElementById('find-mods').style.display = "flex";
}

function changeTabLog() {
    clearAllTabs();
    document.getElementById('text-log').style.display = "flex";
}

function changeTabSearchOptions() {
    clearAllTabs();
    document.getElementById('search-options').style.display = "flex";
}

function changeTabHelp () {
    clearAllTabs();
    document.getElementById('help-text').style.display = "flex";
}

function startModSearch() {
    if (searchingForMods === false) {
        document.getElementById('find-deleted-mods-button').innerHTML = "Stop Searching";
        searchingForMods = true;
        asyncCreateLogElement();
        
    } else {
        searchingForMods = false;
        document.getElementById('find-deleted-mods-button').innerHTML = "Find Deleted Mods";
    }
}

clearAllTabs();
document.getElementById('find-mods').style.display = "flex";

const TEXT_AREA = document.getElementById("find-mods");
TEXT_AREA.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
    }
});