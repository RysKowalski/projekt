import { API } from "/api.js";

const canvasWrapper = document.getElementById("canvas-wrapper");

const mainCanvas = document.getElementById("main-canvas");
const mainCtx = mainCanvas.getContext("2d");

const backgroundCanvas = document.getElementById("background-canvas");
const backgroundCtx = backgroundCanvas.getContext("2d");

let drawing = false;
let lastX = 0;
let lastY = 0;

let fontWidth = 200;
let fontHeight = 200;

canvasWrapper.style.width = `${fontWidth * 3}px`;
canvasWrapper.style.aspectRatio = `${fontWidth} / ${fontHeight}`;

const rect = mainCanvas.getBoundingClientRect();
const dpr = window.devicePixelRatio || 1;

const displayWidth = rect.width;
const displayHeight = rect.height;

mainCanvas.width = rect.width * dpr;
mainCanvas.height = rect.height * dpr;

backgroundCanvas.width = rect.width * dpr;
backgroundCanvas.height = rect.height * dpr;

mainCtx.scale(mainCanvas.width / fontWidth, mainCanvas.height / fontHeight);
backgroundCtx.scale(backgroundCanvas.width / fontWidth, backgroundCanvas.height / fontHeight);

mainCtx.lineWidth = 10;
mainCtx.lineCap = "round";
mainCtx.lineJoin = "round";
mainCtx.strokeStyle = "#fafafa";

let fullBitMap = {};
let i = 0;
let charset = ['a', 'b', 'c'];
let currentCharacter = charset[i];

backgroundCtx.font = "180px Arial";
backgroundCtx.textAlign = "center";
backgroundCtx.textBaseline = "middle";
backgroundCtx.fillStyle = "#1a1a1d"

backgroundCtx.fillText(currentCharacter, fontWidth / 2, fontHeight / 2);

mainCanvas.addEventListener("mousedown", (e) => {
    drawing = true;

    const pos = getMousePos(e);

    lastX = pos.x;
    lastY = pos.y;
});

mainCanvas.addEventListener("mouseup", () => {
    drawing = false;
});

mainCanvas.addEventListener("mousemove", (e) => {
    if (!drawing) return;

    const pos = getMousePos(e);

    mainCtx.beginPath();

    mainCtx.moveTo(lastX, lastY);
    mainCtx.lineTo(pos.x, pos.y);

    mainCtx.stroke();

    lastX = pos.x;
    lastY = pos.y;
});

function getMousePos(e) {
    const rect = mainCanvas.getBoundingClientRect();

    return {
        x: (e.clientX - rect.left) * (fontWidth / rect.width), 
        y: (e.clientY - rect.top) * (fontHeight / rect.height)};
    }


//toolbox
const toolbox = document.getElementById("toolbox");
const sizeSlider = document.getElementById("slider");

sizeSlider.addEventListener("change", updateToolSize);
document.getElementById("eraseAll").addEventListener("click", eraseAll);

updateToolSize();

for(const child of toolbox.children) {
    if (child.className != "tool" || child.dataset.selectable == "false") {
        continue;
    }
    
    child.addEventListener("click", () => {
        toolSelect(child.dataset.toolName);
    });
}

function toolSelect(selectedTool) {
    for (const child of toolbox.children) {
        child.dataset.selected = "false";
    }

    for (const child of toolbox.children) {
        if (child.dataset.toolName == selectedTool) {
            child.dataset.selected = "true";
            updateToolProperties(selectedTool);
        }
    }
}

function updateToolProperties(selectedTool) {
    switch(selectedTool) {
        case "pencil":
            mainCtx.lineWidth = sizeSlider.value;
            mainCtx.globalCompositeOperation = "source-over";
            mainCtx.strokeStyle = "#fafafa";
            break;

        case "eraser":
            mainCtx.globalCompositeOperation = "destination-out";
            break;
    }
}

function updateToolSize() {
    const label = document.getElementById("slider-label");
    label.innerHTML = sizeSlider.value;
    mainCtx.lineWidth = sizeSlider.value;
}

function eraseAll() {
    mainCtx.clearRect(0, 0, fontWidth, fontHeight);
}


//other

const other = document.getElementById("other");

other.addEventListener("click", exportData);

function exportData() {
    const exportCanvas = document.createElement("canvas");
    const exportCtx = exportCanvas.getContext("2d");

    exportCanvas.width = fontWidth;
    exportCanvas.height = fontHeight;

    exportCtx.drawImage(mainCanvas, 0, 0, mainCanvas.width, mainCanvas.height, 0, 0, fontWidth, fontHeight);

    const pixels = exportCtx.getImageData(0, 0, fontWidth, fontHeight);

    const bitMap = [];

    for (let y = 0; y < fontHeight; y++) {
        const row = [];

        for (let x = 0; x < fontWidth; x++) {
            const i = (y * fontWidth + x) * 4;

            if (pixels.data[i + 3] > 127) {
                row.push(1);
            }
            else {
                row.push(0);
            }
        }

        bitMap.push(row);
    }

    const convertedBitMap = [];

    for (let y = 0; y < fontHeight; y++) {
        const row = bitMap[y];
        const convertedRow = [];

        let lastUniqueValue = null;
        let sameValueCombo = 0;
        for (let i = 0; i < row.length; i++) {

            if (lastUniqueValue == null) {
                lastUniqueValue = row[i];
                sameValueCombo = 1;
                continue;
            }

            if (lastUniqueValue == row[i]) {
                sameValueCombo++;
            }
            else {
                convertedRow.push([Boolean(lastUniqueValue), sameValueCombo]);
                lastUniqueValue = row[i];
                sameValueCombo = 1;
            }
        }
        convertedRow.push([Boolean(lastUniqueValue), sameValueCombo]);
        convertedBitMap.push(convertedRow);
    }

    fullBitMap[currentCharacter] = convertedBitMap;

    if (i + 1 < charset.length) {
        nextCharacter();
    }
    else {
        finish();
    }
}

function nextCharacter() {
    eraseAll();
    i++;
    currentCharacter = charset[i];
    backgroundCtx.clearRect(0, 0, fontWidth, fontHeight);
    backgroundCtx.fillText(currentCharacter, fontWidth / 2, fontHeight / 2);
}

async function finish() {
    const project = {bitmaps: fullBitMap, project_id: {id: 0}};

    const data = await API.put("/api/bitmaps", project);
    console.log(data);
}