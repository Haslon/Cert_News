const HamBoton = document.querySelector('.nav__bar')
const Menu = document.querySelector('.Menu')
const close = document.querySelector('.close')

HamBoton.addEventListener('click', () => {
    Menu.style.marginLeft = '10px'
    document.querySelector('body').classList.add('bloquear')
} )

close.addEventListener('click', () => {
    Menu.style.marginLeft = '-2010px'
    document.querySelector('body').classList.remove('bloquear')
})