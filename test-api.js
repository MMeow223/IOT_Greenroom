console.log("Hello World!");
const axios = require("axios");
const fs = require("fs");

const image = fs.readFileSync(
  "C:/Users/Asus/Documents/Arduino/greenroom_unit/Raspberry/WIN_20231018_16_21_30_Pro.jpg",
  {
    encoding: "base64",
  }
);

axios({
  method: "POST",
  url: "https://detect.roboflow.com/plant-size-zrqp4/2",
  params: {
    api_key: "9TwZaDpIJ3gnWQ0inEaH",
  },
  data: image,
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
  },
})
  .then(function (response) {
    console.log(response.data);
  })
  .catch(function (error) {
    console.log(error.message);
  });
