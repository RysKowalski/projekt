const canvas = document.getElementById("main-canvas");
const ctx = canvas.getContext("2d");

let drawing = false;
let lastX = 0;
let lastY = 0;

let fontWidth = 200;
let fontHeight = 200;

const rect = canvas.getBoundingClientRect();
const dpr = window.devicePixelRatio || 1;

const displayWidth = rect.width;
const displayHeight = rect.height;

canvas.width = rect.width * dpr;
canvas.height = rect.height * dpr;

ctx.scale(canvas.width / fontWidth, canvas.height / fontHeight);

canvas.style.aspectRatio = `${fontWidth} / ${fontHeight}`;

ctx.lineWidth = 10;
ctx.lineCap = "round";
ctx.lineJoin = "round";
ctx.strokeStyle = "#fafafa";


canvas.addEventListener("mousedown", (e) => {
    drawing = true;

    const pos = getMousePos(e);

    lastX = pos.x;
    lastY = pos.y;
});

canvas.addEventListener("mouseup", () => {
    drawing = false;
});

canvas.addEventListener("mousemove", (e) => {
    if (!drawing) return;

    const pos = getMousePos(e);

    ctx.beginPath();

    ctx.moveTo(lastX, lastY);
    ctx.lineTo(pos.x, pos.y);

    ctx.stroke();

    lastX = pos.x;
    lastY = pos.y;
});

function getMousePos(e) {
    const rect = canvas.getBoundingClientRect();

    return {
        x: (e.clientX - rect.left) * (fontWidth / rect.width), 
        y: (e.clientY - rect.top) * (fontHeight / rect.height)};
    }


//toolbox
const toolbox = document.getElementById("toolbox");
const sizeSlider = document.getElementById("slider");

sizeSlider.addEventListener("change", updateToolSize);

updateToolSize();

for(const child of toolbox.children) {
    if (child.className != "tool") {
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
            ctx.lineWidth = sizeSlider.value;
            ctx.globalCompositeOperation = "source-over";
            ctx.strokeStyle = "#fafafa";
            break;

        case "eraser":
            ctx.globalCompositeOperation = "destination-out";
            break;
    }
}

function updateToolSize() {
    const label = document.getElementById("slider-label");
    label.innerHTML = sizeSlider.value;
    ctx.lineWidth = sizeSlider.value;
}


//other

const other = document.getElementById("other");

other.addEventListener("click", exportData);

function exportData() {
    const exportCanvas = document.createElement("canvas");
    const exportCtx = exportCanvas.getContext("2d");

    exportCanvas.width = fontWidth;
    exportCanvas.height = fontHeight;

    exportCtx.drawImage(canvas, 0, 0, canvas.width, canvas.height, 0, 0, fontWidth, fontHeight);

    const pixels = exportCtx.getImageData(0, 0, fontWidth, fontHeight);

    const bitMap = [];

    for (let i = 0; i < pixels.data.length; i += 4) {
        if (pixels.data[i + 3] > 127) {
            bitMap.push(1);
        }
        else {
            bitMap.push(0);
        }
        
    }

    console.log(bitMap);
}