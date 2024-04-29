window.addEventListener(('load'), () => {
  if (document.querySelector('#logo') !== null) {
    window.sessionStorage.setItem('Logo', 'displayed');
  }
})

if (window.sessionStorage.getItem('Logo')) {
  document.querySelector('#logo').classList.remove('animated')
}


window.addEventListener(('load'), () => {
  if (document.querySelector('#username') !== null) {
    window.sessionStorage.setItem('Logo', 'displayed');
  }
})

if (window.sessionStorage.getItem('Logo')) {
  document.querySelector('#username').classList.remove('animated1')
}