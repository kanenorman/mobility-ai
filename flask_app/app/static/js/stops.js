stopLocations.forEach(function (stop) {
  L.marker([stop.latitude, stop.longitude]).addTo(map);
});
