export default function Block({ width, height, x, bottom, color, borderRadius, shadow }) {
  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        bottom,
        width,
        height,
        backgroundColor: color,
        borderRadius,
        boxShadow: shadow ? '0 4px 12px rgba(0,0,0,0.4)' : 'none',
      }}
    />
  );
}