/* Get logo element and make it so that when clicked, it will open or close the side menu */
let logo = document.getElementById("logo");
logo.addEventListener("click", function() {
    let sideMenu = document.getElementById("sidebar");
    console.log('clicked')
    if (sideMenu.classList.contains('opened')) {
        sideMenu.classList.remove('opened');
        sideMenu.classList.add('closed');
    } else {
        sideMenu.classList.add('opened');
        sideMenu.classList.remove('closed');
    }
});
