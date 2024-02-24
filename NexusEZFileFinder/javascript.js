const MOD_ID = 1;
let FILE_ID = 1;
let BACKUP_FILE_ID = FILE_ID;
let URL_LINK;
let searchingForMods = false;
let tabIndex = 0;
let modFound = false;

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
changeTabFindMods();

function clearAllTabs () {
    document.getElementById('find-mods').style.display = "none";
    document.getElementById('text-log').style.display = "none";
    document.getElementById('found-log').style.display = "none";
    document.getElementById('search-options').style.display = "none";
    document.getElementById('help-text').style.display = "none";
}

function changeTabFindMods() {
    clearAllTabs();
    document.getElementById('find-mods').style.display = "flex";
    document.getElementById('found-log').style.display = "flex";
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
    let linkHasNumber = /\d+$/.test(document.getElementById('url-text').value);
    if (linkHasNumber === true && !document.getElementById('url-text').value.includes("?")) {
        if (document.getElementById('url-text').value.includes("https://www.nexusmods.com/" && "/mods/")) {
            document.getElementById('enter-url-text').textContent = "Valid URL entered!";
            document.getElementById('enter-url-text').style.color = "green";
            return true;
        } else {
            document.getElementById('enter-url-text').textContent = "Invalid URL entered!";
            document.getElementById('enter-url-text').style.color = "red";
            return false;
        }
    } else {
        document.getElementById('enter-url-text').textContent = "Invalid URL entered!";
        document.getElementById('enter-url-text').style.color = "red";
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
    document.getElementById('text-log').scrollTop = document.getElementById('text-log').scrollHeight;
    URL_LINK = 'https://corsproxy.io/?' + encodeURIComponent(URL_LINK);
    getHTMLContent(URL_LINK);
    createFoundModLog(modFound);
    console.log(modFound);
  }


function createFoundModLog (modFound) {
    if (modFound === true) {
        URL_LINK = document.getElementById('url-text').value;
        URL_LINK = URL_LINK.concat(`?tab=files&file_id=${FILE_ID - 1}`)
        const a = document.createElement('a');
        const link = document.createTextNode(URL_LINK);
        a.appendChild(link);
        a.target= '_blank';
        a.title = URL_LINK;
        a.href = URL_LINK;
        document.getElementById('found-log').appendChild(a);
        document.getElementById('found-log').scrollTop = document.getElementById('text-log').scrollHeight;
    }
}

async function asyncCreateLogElement() {
    FILE_ID = BACKUP_FILE_ID;
    for (;; FILE_ID++) {
        if (searchingForMods === true) {
            await new Promise(resolve => setTimeout(resolve, 750));
            // throttling connection speed is necessary to prevent CORS rejection
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

// -------------------
// working fix from StackOverflow for minimum viable product
// -------------------

let session = new Map();
let queue = [];

async function fetchWithSession(url, session) {
    if (!session.has(url)) {
        session.set(url, fetch(url));
    }
    return session.get(url);
}

async function fetchHTML(url) {
    try {
        const response = await fetchWithSession(url, session);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.text();
    } catch (error) {
        console.error('Error fetching HTML:', error);
        return null;
    } finally {
        processQueue();
    }
}

function processQueue() {
    while (queue.length > 0) {
        const { url, resolve, reject } = queue.shift();
        fetchHTML(url).then(resolve).catch(reject);
    }
}

function addToQueue(url) {
    return new Promise((resolve, reject) => {
        queue.push({ url, resolve, reject });
        processQueue();
    });
}

function searchForLine(htmlContent) {
    const parser = new DOMParser();
    const htmlDoc = parser.parseFromString(htmlContent, 'text/html');
    const line = htmlDoc.querySelector('p.file-download-warning-text');
    return line ? line.textContent.trim() : null;
}

async function getHTMLContent(url) {
    let htmlContent = await addToQueue(url);
    if (htmlContent) {
        const line = searchForLine(htmlContent);
        if (line) {
            modFound = true;
        } else {
            modFound = false;
        }
    } else {
        modFound = false;
    }
}