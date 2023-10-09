const GAME_ID = "skyrimspecialedition";
const MOD_ID = 100562;
let FILE_ID = 1;
let URL_LINK = `https://www.nexusmods.com/${GAME_ID}/mods/${MOD_ID}?tab=files&file_id=${FILE_ID}`

function createLogLinkElement () {
    const a = document.createElement('a');
    const link = document.createTextNode(URL_LINK);
    a.appendChild(link);
    a.title = URL_LINK;
    a.href = URL_LINK;
    document.getElementById('text-log').appendChild(a);
    URL_LINK = `https://www.nexusmods.com/${GAME_ID}/mods/${MOD_ID}?tab=files&file_id=${FILE_ID + 1}`;
    console.log(URL_LINK)
}

async function asyncCreateLogLinkElement() {
    for (; FILE_ID < 1000; FILE_ID++) {
        await new Promise(resolve => setTimeout(resolve, 10));
        createLogLinkElement();
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

clearAllTabs();
document.getElementById('find-mods').style.display = "flex";

asyncCreateLogLinkElement();