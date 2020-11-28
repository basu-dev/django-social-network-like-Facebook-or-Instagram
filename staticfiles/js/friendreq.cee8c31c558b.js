"use strict";
function connect(value) {
  let id = value.split("con&*&*")[1];
  $.ajax({
    type: "POST",
    url: `/profile/send_request/${id}/`,
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    },
    success: function(response) {
      if (response != false) {
        const btn = document.getElementsByClassName(value);
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
  let id = value.split("can*&*")[1];
  $.ajax({
    type: "GET",
    url: `/profile/deny/${id}/`,
    success: function(response) {
      if (response != false) {
        const btn = document.getElementsByClassName(value);
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
  let id = value.split("acc%&")[1];
  $.ajax({
    type: "POST",
    url: `/profile/accept/${id}/`,
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
    },
    success: function(response) {
      let result = response.split("&*&*&*&**ab");
      const connectbtns=document.getElementsByClassName(`con&*&*${id}con&*&*`);
      removeBtn(connectbtns);
     let  btn = result[0];
     let  div = result[1];
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
  const id = value.split("den$%&")[1];
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
var selectedUserId = "";
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
       const btn = document.getElementsByClassName(className);
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
  const len = btngrp.length;
  for (let i = 0; i < len; i++) {
    btngrp.item(0).remove();
  }
}
