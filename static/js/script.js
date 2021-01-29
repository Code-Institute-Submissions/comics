$(document).ready(function () {
    // Materialize functions
    $('.sidenav').sidenav();
    $(".datepicker").datepicker({
        format: "dd/mm/yyyy",
        yearRange: [1930, new Date().getFullYear()],
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    });
    M.updateTextFields();
    $('.modal').modal();
    $('.parallax').parallax();
});

// Sends data to app.py through ajax to add favourites.
function addFavourite(comic_name) {
    $.ajax({
        data: JSON.stringify({ "comic_name": comic_name }),
        contentType: "application/json",
        type: 'POST',
        url: '/add_favourite'
    })
        .done(function () {
            $(`button.favourite[id="${comic_name}"]`).addClass("hide");
            $(`button.unfavourite[id="${comic_name}"]`).removeClass("hide");
        })
}

// Sends data to app.py through ajax to delete favourites.
function deleteFavourite(comic_name) {
    $.ajax({
        data: JSON.stringify({ "comic_name": comic_name }),
        contentType: "application/json",
        type: 'POST',
        url: '/delete_favourite'
    })
        .done(function () {
            $(`button.unfavourite[id="${comic_name}"]`).addClass("hide");
            $(`button.favourite[id="${comic_name}"]`).removeClass("hide");
        })
}
