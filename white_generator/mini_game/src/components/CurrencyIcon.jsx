export default function CurrencyIcon({ icon, size = 20 }) {
  const isImageUrl =
    typeof icon === "string" &&
    (icon.startsWith("http") || icon.startsWith("/") || icon.startsWith("./"));

    return (
      <img
        src={icon}
        alt=""
        style={{ width: size, height: size, verticalAlign: "middle" }}
      />
    );
}
