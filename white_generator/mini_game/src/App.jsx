import { useEffect, useRef, useState } from "react";
import Block from "./components/Block";
import CurrencyIcon from "./components/CurrencyIcon";
import Sky from "./components/Sky";
import { loadConfig } from "./config/loadConfig";
import { MIN_WIDTH_RATIO, NARROW_STEP_RATIO } from "./constants";
import LegalModal from "./components/LegalModal";
import StartScreen from "./components/StartScreen";
import CookieModal from "./components/CookieModal";
import MenuIcon from "./components/MenuIcon";

function getBlockSize() {
  const w = window.innerWidth;
  if (w >= 1024) return { block: 200, footer: 140 };
  if (w >= 600) return { block: 150, footer: 110 };
  return { block: 130, footer: 90 };
}

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
  const [sizes, setSizes] = useState(getBlockSize);
  const [gameWidth, setGameWidth] = useState(window.innerWidth);
  const [gamePhase, setGamePhase] = useState("start");
  const rafRef = useRef(null);
  const dirRef = useRef(1);
  const lastTextureRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    function onResize() {
      setSizes(getBlockSize());
      setGameWidth(window.innerWidth);
    }
    window.addEventListener("resize", onResize);
    window.addEventListener("orientationchange", onResize);
    return () => {
      window.removeEventListener("resize", onResize);
      window.removeEventListener("orientationchange", onResize);
    };
  }, []);

  useEffect(() => {
    loadConfig().then((cfg) => {
      setConfig(cfg);
    });
    return () => cancelAnimationFrame(rafRef.current);
  }, []);

  function handleStart() {
    setGamePhase("playing");
    startGame(config, []);
  }

  function handlePause() {
    cancelAnimationFrame(rafRef.current);
    setGamePhase("paused");
  }

  function handleResume() {
    setGamePhase("playing");
    animate(config);
  }

  if (!config) return null;

  const START_WIDTH = sizes.block;
  const BASE_BLOCK_HEIGHT = sizes.block;
  const FOOTER_HEIGHT = sizes.footer;
  const MIN_WIDTH = START_WIDTH * MIN_WIDTH_RATIO;
  const NARROW_STEP = START_WIDTH * NARROW_STEP_RATIO;

  function pickBlockStyle(cfg) {
    const textures = cfg.block.textures;
    if (textures && textures.length > 0) {
      let pool = textures;
      if (textures.length > 1 && lastTextureRef.current) {
        pool = textures.filter((t) => t !== lastTextureRef.current);
      }
      const texture = pool[Math.floor(Math.random() * pool.length)];
      lastTextureRef.current = texture;
      return { texture, color: null };
    }
    const colors = cfg.block.colors;
    return {
      texture: null,
      color: colors[Math.floor(Math.random() * colors.length)],
    };
  }

  function startGame(cfg, existingStack) {
    const width = existingStack.length
      ? Math.max(
          MIN_WIDTH,
          existingStack[existingStack.length - 1].width - NARROW_STEP,
        )
      : START_WIDTH;
    dirRef.current = 1;
    const style = pickBlockStyle(cfg);
    setCurrent({ x: 0, width, ...style });
    animate(cfg);
  }

  function animate(cfg) {
    cancelAnimationFrame(rafRef.current);
    const step = () => {
      setCurrent((prev) => {
        if (!prev) return prev;
        let nextX = prev.x + cfg.game.moveSpeed * dirRef.current;
        const maxX = gameWidth - prev.width;
        if (nextX <= 0) {
          nextX = 0;
          dirRef.current = 1;
        }
        if (nextX >= maxX) {
          nextX = maxX;
          dirRef.current = -1;
        }
        return { ...prev, x: nextX };
      });
      rafRef.current = requestAnimationFrame(step);
    };
    rafRef.current = requestAnimationFrame(step);
  }

  function handleTap() {
    if (gameOver || !current || gamePhase !== "playing") return;
    if (gameOver || !current) return;

    const lastBlock = stack[stack.length - 1];
    let placedBlock;

    if (!lastBlock) {
      placedBlock = {
        x: current.x,
        width: current.width,
        color: current.color,
        texture: current.texture,
      };
    } else {
      const overlapStart = Math.max(current.x, lastBlock.x);
      const overlapEnd = Math.min(
        current.x + current.width,
        lastBlock.x + lastBlock.width,
      );
      const overlapWidth = overlapEnd - overlapStart;

      if (overlapWidth <= 4) {
        endGame();
        return;
      }
      placedBlock = {
        x: overlapStart,
        width: overlapWidth,
        color: current.color,
        texture: current.texture,
      };
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
    setGamePhase("playing");
    startGame(config, []);
  }

  const containerHeight =
    containerRef.current?.clientHeight || window.innerHeight;
  const playfieldHeight = containerHeight - FOOTER_HEIGHT;
  const targetCurrentBottom = FOOTER_HEIGHT + playfieldHeight * 0.5;
  const currentWorldBottom = FOOTER_HEIGHT + stack.length * BASE_BLOCK_HEIGHT;
  const cameraOffset = Math.max(0, currentWorldBottom - targetCurrentBottom);

  const skyScrollOffset = Math.min(
    stack.length * config.background.scrollPixelsPerBlock,
    config.background.maxScroll,
  );

  return (
    <div ref={containerRef} className="game-container" onClick={handleTap}>
      <Sky
        image={config.background.image}
        fallbackColor={config.background.fallbackColor}
        scrollOffset={skyScrollOffset}
      />

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
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {gamePhase === "playing" && !gameOver && (
            <MenuIcon onClick={handlePause} />
          )}
          <div style={{ fontSize: config.points.fontSize * 0.6 }}>
            {config.points.bestLabel}: {bestScore}
          </div>
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 6,
            fontSize: config.points.fontSize,
            fontWeight: "bold",
          }}
        >
          <CurrencyIcon
            icon={config.points.currencyIcon}
            size={config.points.fontSize}
          />
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
            texture={b.texture}
            maxWidth={START_WIDTH}
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
            texture={current.texture}
            maxWidth={START_WIDTH}
            borderRadius={config.block.borderRadius}
            shadow={config.block.shadow}
          />
        )}
      </div>

      <div
        className="game-footer"
        onClick={(e) => e.stopPropagation()}
        style={{
          height: FOOTER_HEIGHT,
          backgroundColor: config.footer.backgroundColor,
          borderTop: `${config.footer.borderWidth}px solid ${config.footer.borderColor}`,
        }}
      >
        {!gameOver && (
          <button
            className="retry-button"
            onClick={handleRetry}
            style={{
              "--button-gradient-start": config.button.gradientStart,
              "--button-gradient-end": config.button.gradientEnd,
              "--button-border-color": config.button.borderColor,
              color: config.button.textColor,
              borderRadius: config.button.borderRadius,
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
          <div
            style={{
              color: "#fff",
              fontSize: 28,
              marginBottom: 20,
              fontFamily: config.points.font,
            }}
          >
            {config.gameOverText}
          </div>
          <button
            className="retry-button"
            onClick={(e) => {
              e.stopPropagation();
              handleRetry();
            }}
            style={{
              "--button-gradient-start": config.button.gradientStart,
              "--button-gradient-end": config.button.gradientEnd,
              "--button-border-color": config.button.borderColor,
              color: config.button.textColor,
              borderRadius: config.button.borderRadius,
            }}
          >
            {config.button.retryLabel}
          </button>
        </div>
      )}
      <CookieModal
        cookies={config.legal.cookies}
        font={config.points.font}
        buttonConfig={config.button}
      />

      {gamePhase === "start" && (
        <StartScreen
          legal={config.legal}
          font={config.points.font}
          onStart={handleStart}
          buttonConfig={config.button}
        />
      )}

      {gamePhase === "paused" && (
        <LegalModal
          legal={config.legal}
          font={config.points.font}
          onClose={handleResume}
          showResume={true}
          onResume={handleResume}
          buttonConfig={config.button}
        />
      )}
    </div>
  );
}
