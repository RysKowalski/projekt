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