window.addEventListener("load", function() {
  $("#search-input").on("keyup", debounce(onSearchInputChange, 300));
  $("#search-input").on("keyup", setHref);
  setHref();
})

window.addEventListener("click", function(e) {
  if(!$(e.target).closest("#search-area").length) {
    $("#search-result-instant").hide();
  }
})

function onSearchInputChange(e) {
  setHref();

  if(e.target.value.length < 3) {
    $("#search-result-instant").hide();
    return;
  }

  $.ajax({
    url: "/quick_search?query=" + encodeURIComponent(e.target.value),
    type: "GET",

    success: function(json) {
        console.log(json.data);
        fillInstant(json.data);
    },
    error: function(xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText);
    }
});
}

function fillInstant(data) {
  $("#search-result-instant").empty();

  if(!data.length) {
    $("#search-result-instant").show();
    $("#search-result-instant").append("<div>Ничего не найдено!</div>");
    return;
  }

  for(let item of data) {
    $("#search-result-instant").show();
    $("#search-result-instant").append(
      `<div class="instant-item-wrap">
        <div class="instant-item-pic">
          <img src="/static/choco/choco_pics/${item.choco_dir}/${item.choco_pic}"/>
        </div>
        <div class="instant-item-info">
          <div class="instant-item-title"><a href="/catalog/${item.id}/" target="_blank">${item.choco_name}</a></div>
          <div class="instant-item-desc">${item.description}</div>
        </div>
      </div>`
    )
  }
}

function setHref() {
  console.log($("#search-input"));
  $("#search-link").attr("href", "/search?query=" + $("#search-input")[0].value);
}

function debounce(f, ms) {

  let timer = null;

  return function (...args) {
    const onComplete = () => {
      f.apply(this, args);
      timer = null;
    }

    if (timer) {
      clearTimeout(timer);
    }

    timer = setTimeout(onComplete, ms);
  };
}