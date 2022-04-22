// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();
  $('#dataTable2').DataTable();

  $('.custom-accordion').on('click', function (e) {
    if ($(".collapse").hasClass("show")) {
      $('.collapse').removeClass("show");;
    };
  })
});
