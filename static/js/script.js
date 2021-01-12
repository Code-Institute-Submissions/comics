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
    $('.fixed-action-btn').floatingActionButton();
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
            $(this).addClass("hide");
            $(`button.unfavourite[name="${comicId}"]`).removeClass("hide")
        })
}