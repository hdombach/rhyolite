console.log("hello world")

fetch('./main.py.html')
  .then(response=> response.text())
  .then(text=> document.getElementById('root').innerHTML = text);
