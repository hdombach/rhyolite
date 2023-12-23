var is_open = false 

function toggleNav() {
  if (is_open) {
    closeNav()
  } else {
    openNav()
  }
  is_open = !is_open
}

function openNav() {
  document.getElementById("sidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

function closeNav() {
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}
