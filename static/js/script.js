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
            $(`button[id="${comic_name}"]`).children("i").addClass("fas").removeClass("far");
            $(`button[id="${comic_name}"]`).attr("onclick", "deleteFavourite(this.id);").addClass("unfavourite").removeClass("favourite");
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
            $(`button[id="${comic_name}"]`).children("i").addClass("far").removeClass("fas");
            $(`button[id="${comic_name}"]`).attr("onclick", "addFavourite(this.id);").addClass("favourite").removeClass("unfavourite");
        })
}