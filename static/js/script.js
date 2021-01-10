  $(document).ready(function(){
    $('.sidenav').sidenav();
    $(".datepicker").datepicker({
        format: "dd mmmm, yyyy",
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