$(document).ready(function() {
  
  if($(".description").length) {
    $(".article").html($(".description").html().slice($(".description").html().indexOf("Артикул")));
    $(".description").html($(".description").html().slice(0, $(".description").html().indexOf("Артикул")));
  }
})