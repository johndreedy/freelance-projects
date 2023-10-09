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
}

for (; FILE_ID < 1000; FILE_ID++) {
    createLogLinkElement();
}
