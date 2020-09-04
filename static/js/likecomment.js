function like(value, checkvalue) {
  if (checkvalue == 1) {
    id = value.split("likea")[1];
  } else if (checkvalue == 2) {
    id = value.split("like")[1];
  }
  $.ajax({
    url: "/api/like/" + id + "/",
    type: "POST",
    data: { csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val() },
    success: function(data) {
      if (data.truth == "True") {
        updated_count = data.count;
        $("." + id + "_likey").remove();
        $(".like_show" + id)
          .html(updated_count + " Likes")
          .show();
        $(`#like${id}like`).html(data.is_liked);
      } else if (data.truth == "False") {
        updated_count = data.count;
        $("." + id + "_likey").remove();
        $(".like_show" + id)
          .html(updated_count + " Likes")
          .show();
        $(`#like${id}like`).html(data.is_liked);
        $(`#like${id}like`).css("border");
      }
      try {
        $(".liketoggle").html(updated_count + " Like");
      } catch (e) {
        console.log(e);
      }
    },
    error: function(err) {
      toastr(err);
    }
  });
}
function getLike(value) {
  id = value.split("getlike")[1];
  $.ajax({
    type: "GET",
    url: "/api/like/getlike/" + id + "/",
    success: function(response) {
      $(".likediv").html(response);
    }
  });
}
function commentt(div) {
  idvalue = div[0].id;
  id = idvalue.split("comment")[1];
  var comment = div[0].value;
  if (comment.trim() == "") {
    div[0].value = "";
    return false;
  } else {
    for (i = 0; i <= comment.length; i++) {
      if (comment[i] == "\n") {
        div[0].value = "";
        $.ajax({
          type: "POST",
          url: "/api/stories/comment/" + id + "/",
          data: {
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            comment: comment
          },
          success: function(data) {
            var commentdiv = `<div class='media'>
<span class="a" href='${data.url}' onclick="route(this.attributes.href.value)">
<img class='mediaimg pp' src='${data.profile_picture}'>
</span>

<div class='cmt'><span onclick="route(this.attributes.href.value)" href="${data.url}"
class="a cmtuser">${data.user}</a>
${data.comment}</div>
</div>`;
            $(".commentupdate_" + id).prepend(commentdiv);
          },
          error: function(err) {
            toastr(err);
          }
        });
      }
    }
  }
}
