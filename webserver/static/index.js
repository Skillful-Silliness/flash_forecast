function buildQueryString(args) {
  if (!args) return ""

  const pairs = Object.keys(args).map(key => (key + "=" + args[key]))

  if (!pairs.length) return ""

  return '?' + pairs.join("&")
}

function apiRequest(command, args) {
  const query = buildQueryString(args)

  return fetch('/' + command + query)
    .then(response => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

function handleButtonClick(e, command, callback) {
  e.target.classList.add('loading')

  apiRequest(command)
    .then((res) => {
      console.log(res)
      e.target.classList.remove('loading')
      if(callback) callback(res)
    })
    .catch(() => e.target.classList.remove('loading'))
}

function setBrightnessDisplay(res) {
  const displayBrightness = Math.round(res.brightness * 100)

  document.querySelector(".brightness-display").innerHTML = displayBrightness
}

function initState() {
  apiRequest("status")
    .then((res) => {
      console.log({res})
      setBrightnessDisplay(res)
    })
    .catch((err) => console.error(err))
}

document.addEventListener("DOMContentLoaded", function() {
  document.querySelector(".on").addEventListener("click", (e) => handleButtonClick(e, "on"))
  document.querySelector(".off").addEventListener("click", (e) => handleButtonClick(e, "off"))
  document.querySelector(".brighter").addEventListener("click", (e) => handleButtonClick(e, "brighter", setBrightnessDisplay))
  document.querySelector(".darker").addEventListener("click", (e) => handleButtonClick(e, "darker", setBrightnessDisplay))

  initState()

  setInterval(initState, 1000)
})
