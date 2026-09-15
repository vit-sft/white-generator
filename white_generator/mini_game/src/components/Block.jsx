export default function Block({
  width,
  height,
  x,
  bottom,
  color,
  texture,
  maxWidth,
  borderRadius,
  shadow,
}) {
  const baseStyle = {
    position: "absolute",
    left: x,
    bottom,
    width,
    height,
    borderRadius,
    boxShadow: shadow ? "0 4px 12px rgba(0,0,0,0.4)" : "none",
    overflow: "hidden",
  };

  return (
    <div style={baseStyle}>
      {texture && (
        <div
          className="block-texture"
          style={{
            width: "100%",
            height: "100%",
            backgroundImage: `url(${texture})`,
            backgroundRepeat: "no-repeat",
            backgroundSize: `${maxWidth}px ${height}px`,
            backgroundPosition: "left center",
          }}
        />
      )}
      <div
        className={texture ? "block-fallback" : ""}
        style={{
          width: "100%",
          height: "100%",
          backgroundColor: color || "#8b5a2b",
          display: texture ? undefined : "block",
        }}
      />
    </div>
  );
}
