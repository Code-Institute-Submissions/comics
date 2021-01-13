$(document).ready(function () {
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

function addFavourite(comicId) {
        $.ajax({
			data : JSON.stringify({"comic_id" : comicId}),
            contentType : "application/json",
			type : 'POST',
			url : '/add_favourite'
        })
        .done(function() {
            $(`button.favourite[id="${comicId}"]`).addClass("hide");
            $(`button.unfavourite[name="${comicId}"]`).removeClass("hide");
        })
}

function deleteFavourite(comicId) {
            $.ajax({
			data : JSON.stringify({"comic_id" : comicId}),
            contentType : "application/json",
			type : 'POST',
			url : '/delete_favourite'
        })
        .done(function() {
            $(`button.unfavourite[name="${comicId}"]`).addClass("hide");
            $(`button.favourite[id="${comicId}"]`).removeClass("hide");
        })
}