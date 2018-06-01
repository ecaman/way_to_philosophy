$(document).ready(function(){
  $('.radio-btn').click(function() {
    $(".radio_block").each(isChecked)
  })

  function isChecked() {
    var checked = $(this).find(".radio-btn").is(":checked")
    $(this).toggleClass("hvr", checked)
  }});
