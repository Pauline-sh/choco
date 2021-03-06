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

  if(e.key == "Enter") {
    window.location.href = ("/search?query=" + $("#search-input")[0].value);
  }

  if(!e.target.value.length) {
    $("#search-result-instant").hide();
    return;
  }

  $.ajax({
    url: "/quick_search?query=" + encodeURIComponent(e.target.value),
    type: "GET",

    success: function(json) {
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
    let img = item.choco_pic;

    if(img.indexOf('tn') !== -1 && location.href.indexOf('memento') === -1) {
      img = 'new_' + img;
    }

    $("#search-result-instant").show();
    $("#search-result-instant").append(
      `<div class="instant-item-wrap">
        <div class="instant-item-pic">
          <img src="/static/choco/choco_pics/${item.choco_dir}/${img}"/>
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
  if(!$("#search-input")[0].value.length) {
    $("#search-link").attr("href", "#");
    return;
  }

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