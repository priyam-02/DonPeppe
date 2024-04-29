window.addEventListener(('load'), () => {
  if (document.querySelector('#log') !== null) {
    window.sessionStorage.setItem('Logo', 'displayed');
  }
})

if (window.sessionStorage.getItem('Logo')) {
  document.querySelector('#log').classList.remove('anim')
}


