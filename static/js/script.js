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
function addFavourite(comicId) {
    $.ajax({
        data: JSON.stringify({ "comic_id": comicId }),
        contentType: "application/json",
        type: 'POST',
        url: '/add_favourite'
    })
        .done(function () {
            $(`button.favourite[id="${comicId}"]`).addClass("hide");
            $(`button.unfavourite[id="${comicId}"]`).removeClass("hide");
        })
}

// Sends data to app.py through ajax to delete favourites.
function deleteFavourite(comicId) {
    $.ajax({
        data: JSON.stringify({ "comic_id": comicId }),
        contentType: "application/json",
        type: 'POST',
        url: '/delete_favourite'
    })
        .done(function () {
            $(`button.unfavourite[id="${comicId}"]`).addClass("hide");
            $(`button.favourite[id="${comicId}"]`).removeClass("hide");
        })
}
