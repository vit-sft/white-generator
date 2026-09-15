export default function Sky({ image, fallbackColor, scrollOffset }) {
  if (!image) {
    return (
      <div
        style={{ position: "absolute", inset: 0, background: fallbackColor }}
      />
    );
  }

  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden" }}>
      <img
        src={image}
        alt=""
        className="game-sky"
        style={{
          transform: `translateY(${scrollOffset}px)`,
          transition: "transform 0.6s ease-out",
        }}
      />
    </div>
  );
}
