const canvas = document.getElementById('wheel');
const ctx = canvas.getContext('2d');
const r = canvas.width / 2;

const BASE_SPEED = 0.03;
const MAX_SPEED = 0.5;
const HOLD_DELAY = 200;
const ACCELERATION = 0.03;

let angle = 0;
let speed = BASE_SPEED;
let targetSpeed = BASE_SPEED;
let holding = false;
let holdTimer = null;
let revertTimer = null;

function drawWheel() {
  ctx.save();
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.translate(r, r);
  ctx.rotate(angle);

  const slice = (2 * Math.PI) / colors.length;
  colors.forEach((c, i) => {
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.fillStyle = c;
    ctx.arc(0, 0, r - 4, i * slice, (i + 1) * slice);
    ctx.fill();
  });

  // Border ring
  ctx.beginPath();
  const grad = ctx.createRadialGradient(0, 0, r * 0.7, 0, 0, r);
  grad.addColorStop(0, "rgba(255,255,255,0.25)");
  grad.addColorStop(1, "rgba(255,255,255,0.05)");
  ctx.strokeStyle = grad;
  ctx.lineWidth = 4;
  ctx.arc(0, 0, r - 2, 0, Math.PI * 2);
  ctx.stroke();

  ctx.restore();
}

function animate() {
  requestAnimationFrame(animate);
  speed += (targetSpeed - speed) * ACCELERATION;

  if (!holding && targetSpeed === BASE_SPEED && speed > BASE_SPEED) {
    speed *= 0.995;
    if (speed < BASE_SPEED) speed = BASE_SPEED;
  }

  angle += speed;
  drawWheel();
}

function setTarget(base = false) {
  if (holding) {
    holding = false;
    targetSpeed = BASE_SPEED;
  } else if (!base) {
    // Accelerate instantly
    targetSpeed = Math.min(targetSpeed + 0.15, MAX_SPEED);
    speed = Math.min(speed + 0.1, MAX_SPEED);

    // Clear previous revert timer
    if (revertTimer) clearTimeout(revertTimer);

    // Slowly return to base speed after some time
    revertTimer = setTimeout(() => {
      targetSpeed = BASE_SPEED;
    }, 500);
  } else {
    targetSpeed = BASE_SPEED;
  }
}

// --- Touch handling ---
canvas.addEventListener("touchstart", e => {
  canvas.dispatchEvent(new PointerEvent("pointerdown", e));
});
canvas.addEventListener("touchend", e => {
  canvas.dispatchEvent(new PointerEvent("pointerup", e));
});

// --- Pointer events ---
canvas.addEventListener("pointerdown", () => {
  holdTimer = setTimeout(() => {
    holding = true;
    targetSpeed = 0;
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

animate();
