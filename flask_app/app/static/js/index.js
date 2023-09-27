const bostonCoordinates = [42.3601, -71.0589];
const map = L.map("map").setView(bostonCoordinates, 12);
var CartoDB_Voyager = L.tileLayer(
  "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
  {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: "abcd",
    maxZoom: 20,
  },
);
CartoDB_Voyager.addTo(map);
