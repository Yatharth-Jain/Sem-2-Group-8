let weather = {
  apiKey: "786e2f50610360abd3176cf6027ce23e",
  fetchWeather: function (city) {
    fetch(
      "https://api.openweathermap.org/data/2.5/weather?q=" +
        city +
        "&units=metric&appid=" +
        this.apiKey
    )
      .then((res) => res.json())
      .then((data) => this.displayWeather(data))
      .catch((e) => console.log(e));
  },
  displayWeather: function (data) {
    const { name } = data;
    const { temp } = data.main;
    const { description } = data.weather[0];
    document.querySelector(".cityName").innerText = name;
    document.querySelector(".temperature").innerHTML =
      Math.round(temp) + `<sup>C</sup>`;
    document.querySelector(".desc").innerText = description;
  },
};

window.onload = weather.fetchWeather("Lucknow");
