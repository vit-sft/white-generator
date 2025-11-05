const canvas = document.getElementById('slot');
const ctx = canvas.getContext('2d');

// --- CONFIG ---
const SYMBOL_SIZE = 35;
const REEL_GAP = 5;
const BASE_SPEED = 3;
const MAX_SPEED = 45;
const ACCEL_UP = 0.12;   // faster acceleration
const ACCEL_DOWN = 0.04; // slower deceleration
const DAMP = 0.995;      // slower glide when coasting
const HOLD_DELAY = 300;

// --- SETUP ---
const reelWidth = SYMBOL_SIZE;
const totalWidth = NUM_REELS * reelWidth + (NUM_REELS + 1) * REEL_GAP;
const totalHeight = 80;
canvas.width = totalWidth;
canvas.height = totalHeight;
const W = canvas.width;
const H = canvas.height;

// --- STATE ---
let reels = Array(NUM_REELS).fill(0).map(() => ({
  offset: Math.random() * SYMBOLS.length * SYMBOL_SIZE,
  speed: BASE_SPEED,
  targetSpeed: BASE_SPEED
}));
let holding = false;
let holdTimer = null;
let revertTimer = null;

function drawReel(x, reel) {
  const totalHeight = SYMBOLS.length * SYMBOL_SIZE;
  let offsetY = ((reel.offset % totalHeight) + totalHeight) % totalHeight;

  for (let y = -SYMBOL_SIZE; y < H + SYMBOL_SIZE; y += SYMBOL_SIZE) {
    const index = Math.floor((offsetY / SYMBOL_SIZE + y / SYMBOL_SIZE)) % SYMBOLS.length;
    const symbol = SYMBOLS[(index + SYMBOLS.length) % SYMBOLS.length];
    ctx.font = `${SYMBOL_SIZE * 0.75}px Segoe UI Emoji`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(symbol, x + SYMBOL_SIZE / 2, y + SYMBOL_SIZE / 2 - offsetY % SYMBOL_SIZE);
  }

  // Vertical fade
  const fade = ctx.createLinearGradient(0, 0, 0, H);
  fade.addColorStop(0, "rgba(0, 0, 0, 0.18)");
  fade.addColorStop(0.15, "transparent");
  fade.addColorStop(0.85, "transparent");
  fade.addColorStop(1, "rgba(0, 0, 0, 0.18)");
  ctx.fillStyle = fade;
  ctx.fillRect(x, 0, SYMBOL_SIZE, H);

  // Border
  ctx.lineWidth = 3;
  ctx.strokeStyle = "rgba(255,255,255,0.12)";
  ctx.strokeRect(x, 0, SYMBOL_SIZE, H);
}

function draw() {
  // Base background using CSS vars
  const rootStyle = getComputedStyle(document.documentElement);
  const background = rootStyle.getPropertyValue('--background').trim();
  const primary = rootStyle.getPropertyValue('--primary').trim();
  const secondary = rootStyle.getPropertyValue('--secondary').trim();

  const panelGradient = ctx.createLinearGradient(0, 0, W, 0);
  panelGradient.addColorStop(0, background);
  panelGradient.addColorStop(0.5, primary);
  panelGradient.addColorStop(1, secondary);

  ctx.fillStyle = panelGradient;
  ctx.fillRect(0, 0, W, H);

  // Reels
  for (let i = 0; i < NUM_REELS; i++) {
    const x = i * (SYMBOL_SIZE + REEL_GAP) + REEL_GAP;
    drawReel(x, reels[i]);
  }

  // Middle highlight
  ctx.fillStyle = "rgba(255,255,255,0.05)";
  ctx.fillRect(0, H / 2 - SYMBOL_SIZE / 2, W, SYMBOL_SIZE);
}

function update() {
  for (let reel of reels) {
    const accel = reel.speed < reel.targetSpeed ? ACCEL_UP : ACCEL_DOWN;
    reel.speed += (reel.targetSpeed - reel.speed) * accel;

    // smooth deceleration when returning to base speed
    if (!holding && reel.targetSpeed === BASE_SPEED && reel.speed > BASE_SPEED) {
      reel.speed *= DAMP;
      if (reel.speed < BASE_SPEED) reel.speed = BASE_SPEED;
    }

    reel.offset += reel.speed;
    if (reel.offset >= SYMBOLS.length * SYMBOL_SIZE) {
      reel.offset -= SYMBOLS.length * SYMBOL_SIZE;
    }
  }
}

function loop() {
  requestAnimationFrame(loop);
  update();
  draw();
}

// --- HELPER ---
function setTarget(base = false) {
  if (holding) {
    holding = false;
    for (const reel of reels) reel.targetSpeed = BASE_SPEED;
  } else if (!base) {
    // Accelerate quickly and cleanly
    for (const reel of reels) {
      reel.targetSpeed = Math.min(reel.targetSpeed + 10, MAX_SPEED);
      reel.speed = Math.min(reel.speed + 6, MAX_SPEED);
    }

    // Clear any pending revert
    if (revertTimer) clearTimeout(revertTimer);

    // Slowly return to base speed
    revertTimer = setTimeout(() => {
      for (const reel of reels) reel.targetSpeed = BASE_SPEED;
    }, 500);
  } else {
    for (const reel of reels) reel.targetSpeed = BASE_SPEED;
  }
}

// --- INPUT ---
canvas.addEventListener("touchstart", e => {
  e.preventDefault();
  canvas.dispatchEvent(new PointerEvent("pointerdown", e));
});
canvas.addEventListener("touchend", e => {
  e.preventDefault();
  canvas.dispatchEvent(new PointerEvent("pointerup", e));
});

canvas.addEventListener("pointerdown", () => {
  holdTimer = setTimeout(() => {
    holding = true;
    for (const reel of reels) reel.targetSpeed = 0;
  }, HOLD_DELAY);
});

canvas.addEventListener("pointerup", () => {
  if (holdTimer) clearTimeout(holdTimer);
  setTarget();
});

canvas.addEventListener("pointerleave", () => {
  if (holdTimer) clearTimeout(holdTimer);
  setTarget(true);
});

loop();
