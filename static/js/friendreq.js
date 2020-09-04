function connect(value) {
  id = value.split("con&*&*")[1];
  $.ajax({
    type: "POST",
    url: `/profile/send_request/${id}/`,
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    },
    success: function(response) {
      if (response != false) {
        btn = document.getElementsByClassName(value);
        removeBtn(btn);
        $(`.messagebody${id}`).append(response);
      }
    },
    error: function(err) {
      toastr(err);
    }
  });
}
function cancelbtn(value) {
  id = value.split("can*&*")[1];
  $.ajax({
    type: "GET",
    url: `/profile/deny/${id}/`,
    success: function(response) {
      if (response != false) {
        btn = document.getElementsByClassName(value);
        removeBtn(btn);
        $(`.messagebody${id}`).append(response);
      }
    },
    error: function(err) {
      toastr(err, "Request Doesn't Exist", "Try Reloading The Page.");
    }
  });
}
function accept(value) {
  id = value.split("acc%&")[1];
  $.ajax({
    type: "POST",
    url: `/profile/accept/${id}/`,
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    },
    success: function(response) {
      console.log(response)
      result = response.split("&*&*&*&**ab");
      connectbtns=document.getElementsByClassName(`con&*&*${id}con&*&*`);
      removeBtn(connectbtns);
      btn = result[0];
      div = result[1];
      if (response != false) {
        $(`#frnreq${id}`).remove();
        $(`.req${id}`).remove();
        $(".messagebody" + id).append(btn);
        try {
          $(".friendss").prepend(div);
        } catch (e) {}
        try {
          $(".nofriends").remove();
        } catch (e) {}
      }
    },
    error: function(err) {
      toastr(err);
    }
  });
}
function deny(value) {
  id = value.split("den$%&")[1];
  $.ajax({
    type: "POST",
    url: `/profile/deny/${id}/`,
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    },
    success: function(response) {
      if (response != false) {
        $(`#frnreq${id}`).remove();
        $(`.req${id}`).remove();
        $(".messagebody" + id).append(response);
      }
    },
    error: function(err) {
      toastr(err);
    }
  });
}
selectedUserId = "";
function disconnect(value) {
  openModal(
    "Confirmation",
    "Are You Sure You Want To Disconnect?",
    disconnectConfirm
  );
  selectedUserId = value.split("dis*&*")[1];
}
function disconnectConfirm() {
  let id = selectedUserId;
  $.ajax({
    type: "POST",
    url: `/profile/unfriend/${id}/`,
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    },
    success: function(response) {
      if (response != false) {
       let className=`disconnectbtn dis*&*${id}dis*&*`
        btn = document.getElementsByClassName(className);
        // btn.forEach(b=>b.remove());
        removeBtn(btn);
        $(`.messagebody${id}`).append(response);
        $(`.${id}`).remove();
        try {
          $(`.msglaunch${id}msglaunch`).remove();
        } catch {}
      }
    },
    error: function(err) {
      toastr(err);
    }
  });
}
function removeBtn(btngrp) {
  console.log(btngrp)
  len = btngrp.length;
  for (i = 0; i < len; i++) {
    btngrp.item(0).remove();
  }
  console.log(btngrp)
}
