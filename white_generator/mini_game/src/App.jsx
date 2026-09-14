import { useEffect, useRef, useState } from "react";
import Block from "./components/Block";
import CurrencyIcon from "./components/CurrencyIcon";
import { loadConfig } from "./config/loadConfig";
import { BASE_BLOCK_HEIGHT, START_WIDTH, MIN_WIDTH, NARROW_STEP } from "./constants";

export default function App() {
  const [config, setConfig] = useState(null);
  const [stack, setStack] = useState([]);
  const [current, setCurrent] = useState(null);
  const [score, setScore] = useState(0);
  const [bestScore, setBestScore] = useState(() => {
    const saved = localStorage.getItem("towerBestScore");
    return saved ? Number(saved) : 0;
  });
  const [gameOver, setGameOver] = useState(false);
  const rafRef = useRef(null);
  const dirRef = useRef(1);

  useEffect(() => {
    loadConfig().then((cfg) => {
      setConfig(cfg);
      startGame(cfg, []);
    });
    return () => cancelAnimationFrame(rafRef.current);
  }, []);

  if (!config) return null;

  const { width: GAME_WIDTH, height: GAME_HEIGHT, footerHeight: FOOTER_HEIGHT, topMargin: TOP_MARGIN, moveSpeed: MOVE_SPEED } = config.game;

  const PLAYFIELD_HEIGHT = GAME_HEIGHT - TOP_MARGIN - FOOTER_HEIGHT;
  const TARGET_CURRENT_BOTTOM = FOOTER_HEIGHT + PLAYFIELD_HEIGHT / 2;

  function pickColor(cfg) {
    const colors = cfg.block.colors;
    return colors[Math.floor(Math.random() * colors.length)];
  }

  function startGame(cfg, existingStack) {
    const width = existingStack.length
      ? Math.max(MIN_WIDTH, existingStack[existingStack.length - 1].width - NARROW_STEP)
      : START_WIDTH;
    dirRef.current = 1;
    setCurrent({ x: 0, width, color: pickColor(cfg) });
    animate(cfg);
  }

  function animate(cfg) {
    cancelAnimationFrame(rafRef.current);
    const step = () => {
      setCurrent((prev) => {
        if (!prev) return prev;
        let nextX = prev.x + cfg.game.moveSpeed * dirRef.current;
        const maxX = cfg.game.width - prev.width;
        if (nextX <= 0) { nextX = 0; dirRef.current = 1; }
        if (nextX >= maxX) { nextX = maxX; dirRef.current = -1; }
        return { ...prev, x: nextX };
      });
      rafRef.current = requestAnimationFrame(step);
    };
    rafRef.current = requestAnimationFrame(step);
  }

  function handleTap() {
    if (gameOver || !current) return;

    const lastBlock = stack[stack.length - 1];
    let placedBlock;

    if (!lastBlock) {
      placedBlock = { x: current.x, width: current.width, color: current.color };
    } else {
      const overlapStart = Math.max(current.x, lastBlock.x);
      const overlapEnd = Math.min(current.x + current.width, lastBlock.x + lastBlock.width);
      const overlapWidth = overlapEnd - overlapStart;

      if (overlapWidth <= 4) {
        endGame();
        return;
      }
      placedBlock = { x: overlapStart, width: overlapWidth, color: current.color };
    }

    const newStack = [...stack, placedBlock];
    setStack(newStack);
    const newScore = score + 1;
    setScore(newScore);
    if (newScore > bestScore) {
      setBestScore(newScore);
      localStorage.setItem("towerBestScore", String(newScore));
    }
    startGame(config, newStack);
  }

  function endGame() {
    cancelAnimationFrame(rafRef.current);
    setGameOver(true);
  }

  function handleRetry() {
    setStack([]);
    setScore(0);
    setGameOver(false);
    startGame(config, []);
  }

  const currentWorldBottom = FOOTER_HEIGHT + stack.length * BASE_BLOCK_HEIGHT;
  const cameraOffset = Math.max(0, currentWorldBottom - TARGET_CURRENT_BOTTOM);

  return (
    <div
      onClick={handleTap}
      style={{
        width: GAME_WIDTH,
        height: GAME_HEIGHT,
        margin: "40px auto",
        position: "relative",
        overflow: "hidden",
        background: config.background.value,
        borderRadius: 16,
        cursor: "pointer",
        userSelect: "none",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 16,
          left: 16,
          right: 16,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 10,
          fontFamily: config.points.font,
          color: config.points.color,
        }}
      >
        <div style={{ fontSize: config.points.fontSize * 0.6 }}>
          {config.points.bestLabel}: {bestScore}
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 6, fontSize: config.points.fontSize, fontWeight: "bold" }}>
          <CurrencyIcon icon={config.points.currencyIcon} size={config.points.fontSize} />
          {score}
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translateY(${cameraOffset}px)`,
          transition: "transform 0.25s ease-out",
        }}
      >
        {stack.map((b, i) => (
          <Block
            key={i}
            x={b.x}
            width={b.width}
            height={BASE_BLOCK_HEIGHT}
            bottom={FOOTER_HEIGHT + i * BASE_BLOCK_HEIGHT}
            color={b.color}
            borderRadius={config.block.borderRadius}
            shadow={config.block.shadow}
          />
        ))}

        {current && !gameOver && (
          <Block
            x={current.x}
            width={current.width}
            height={BASE_BLOCK_HEIGHT}
            bottom={FOOTER_HEIGHT + stack.length * BASE_BLOCK_HEIGHT}
            color={current.color}
            borderRadius={config.block.borderRadius}
            shadow={config.block.shadow}
          />
        )}
      </div>

      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: FOOTER_HEIGHT,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          backgroundColor: config.footer.backgroundColor,
          borderTop: `${config.footer.borderWidth}px solid ${config.footer.borderColor}`,
        }}
      >
        {!gameOver && (
          <button
            onClick={handleRetry}
            style={{
              backgroundColor: config.button.backgroundColor,
              color: config.button.textColor,
              borderRadius: config.button.borderRadius,
              border: "none",
              padding: "12px 40px",
              fontSize: 18,
              fontWeight: "bold",
              cursor: "pointer",
            }}
          >
            {config.button.retryLabel}
          </button>
        )}
      </div>

      {gameOver && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            zIndex: 20,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            background: "rgba(0,0,0,0.55)",
          }}
        >
          <div style={{ color: "#fff", fontSize: 28, marginBottom: 20, fontFamily: config.points.font }}>
            {config.gameOverText}
          </div>
          <button
            onClick={(e) => { e.stopPropagation(); handleRetry(); }}
            style={{
              backgroundColor: config.button.backgroundColor,
              color: config.button.textColor,
              borderRadius: config.button.borderRadius,
              border: "none",
              padding: "12px 40px",
              fontSize: 18,
              fontWeight: "bold",
              cursor: "pointer",
            }}
          >
            {config.button.retryLabel}
          </button>
        </div>
      )}
    </div>
  );
}