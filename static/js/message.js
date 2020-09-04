function loadMoreMsg(value) {
  previousHeight = $("#scrollanimate")[0].scrollHeight;
  newvalue = value.split("ms*&*")[1];
  userid = newvalue.split("n")[0];
  lastid = newvalue.split("n")[1];
  btn = document.getElementById(value);
  btn.innerHTML = "<div style='height:32px'>Loading....</div>  ";
  $.ajax({
    type: "GET",
    url: `/messages/moremessages/${userid}/${lastid}`,
    success: function(response) {
      btn.remove();
      $(`.messagearea`).prepend(response);
      recentHeight = $("#scrollanimate")[0].scrollHeight;
      if (recentHeight - previousHeight != 0) {
        scroll(recentHeight - previousHeight);
      }
      arrangeElements();
    },
    error: function(err) {
      toastr(err);
    }
  });
}
function scroll(height) {
  let time = 0;
  obj = { height, time };
  obj = height
    ? { height: height, time: 0 }
    : { height: $("#scrollanimate")[0].scrollHeight, time: 5 };
  $("#scrollanimate")
    .stop()
    .animate({ scrollTop: obj.height }, obj.time);
}
function sendMessage(value) {
  var msg = $("#" + value).val();
  id = value.split("textarea")[1];
  if (msg.trim() == "") {
    document.getElementById(value).value = "";
    return false;
  } else {
    for (i = 0; i < msg.length; i++) {
      if (msg[i] == "\n") {
        if ((msg.length == 0) | (msg == "\n")) {
          return false;
        } else {
          document.getElementById(value).value = "";
          $.ajax({
            type: "POST",
            url: "/messages/api/" + id + "/",
            data: {
              csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
              message: msg
            },
            success: function(data) {
              play();
              var div = `<div class="mymsg">
<span>${data.message}</span>
</div>`;
              scroll();
              $(".messagearea").append(div);
              arrangeElements();
            },
            error: function(err) {
              toastr(err);
            }
          });
        }
      }
    }
  }
}
interval = -1;
function getMessage(id) {
  try {
    clearInterval(interval);
  } catch (e) {}
  interval = val = setInterval(function() {
    try {
      $.ajax({
        type: "GET",
        url: "/messages/api/" + id + "/",
        success: function(data) {
          if (data.data) {
            play();
            var div = `<div class="hismsg">
  <span>${data.message}</span>
  </div>`;
            scroll();
            $(".messagearea").append(div);
            arrangeElements();
          }
        },
        error: function(err) {
          // toastr(err)
        }
      });
    } catch (e) {}
  }, 1000);
}
function play() {
  audio = $("audio");
  audio[0].play();
}
function remove(abc) {
  loadMessanger();
  $("#addedmessagebox").remove();
  clearInterval(interval);
  $(".previous_messageareaa").css("display", "block");
}
function arrangeElements() {
  var leftClass = "hismsg";
  var rightClass = "mymsg";
  var parentClass = ".messagearea div";
  var reqBorderRadius = "20px";
  var normalBorderRadius = "3px";
  var children = $(parentClass);
  var len = children.length;
  lastElement = children[0];
  recentElement = null;
  for (var i = 0; i < len; i++) {
    recentElement = children[i];
    if (!(recentElement.className == lastElement.className)) {
      recentElement.firstElementChild.style.marginTop = "2px";
      if (lastElement.className == leftClass) {
        lastElement.firstElementChild.style.borderBottomLeftRadius = reqBorderRadius;

        recentElement.firstElementChild.style.borderTopRightRadius = reqBorderRadius;
      } else {
        lastElement.firstElementChild.style.borderBottomRightRadius = reqBorderRadius;
        recentElement.firstElementChild.style.borderTopLeftRadius = reqBorderRadius;
      }
    } else {
      if (lastElement.className == leftClass) {
        lastElement.firstElementChild.style.borderBottomLeftRadius = normalBorderRadius;
      } else {
        lastElement.firstElementChild.style.borderBottomRightRadius = normalBorderRadius;
      }
    }
    lastElement = recentElement;
  }
  if (children[len - 1].className == leftClass) {
    children[
      len - 1
    ].firstElementChild.style.borderBottomLeftRadius = reqBorderRadius;
  } else if (children[len - 1].className == rightClass) {
    children[
      len - 1
    ].firstElementChild.style.borderBottomRightRadius = reqBorderRadius;
  }
};
