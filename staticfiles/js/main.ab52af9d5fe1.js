"use strict";
let friendusername = "";
let friendprofieloaded = false;
let storydetailloaded = false;
function loading(truth) {
  if (truth) {
    $("#loading").css({ display: "block", opacity: "1" });
  } else {
    $("#loading").css({ opacity: "0", display: "none" });
  }
}
function hideAndShow(hide, show) {
  try {
    $(hide).css("display", "none");
  } catch (e) {}
  try {
    $(show).css("display", "block");
  } catch (e) {}
}
function generalToggle(button, target, closed) {
  if (closed) {
    $(target).css("display", "block");
    $(
      button
    )[0].attributes.onclick.value = `generalToggle('${button}','${target}')`;
  } else {
    $(target).css("display", "none");
    $(
      button
    )[0].attributes.onclick.value = `generalToggle('${button}','${target}',true)`;
  }
}

function loadFriends() {
  $.ajax({
    type: "GET",
    url: "/profile/api/fetch_friends",
    success: function (response) {
      $(".friendtop").css("opacity", "1");
      $(".friendlistt").html(response);
    },
    error: function (err) {
      toastr(err);
    },
  });
}

function loadMoreStories(value) {
  const lastId = value.split("n")[0];
  const firstid = value.split("n")[1];
  loading(true),
    $.ajax({
      type: "GET",
      url: `/stories/get_more_stories/${lastId}/${firstid}`,
      success: function (response) {
        $(`#${value}`).remove();
        let result = response.split("antxi");
        for (let i = 0; i < result.length; i++) {
          if (i % 2 != 0) {
            let div = document.getElementById(`antxi${result[i]}antxi`);
            if (div != null) {
              div.remove();
            }
          }
        }
        loading();
        $(".stories").append(response);
      },
      error: function (err) {
        toastr(err);
      },
    });
}
function storeProfile() {
  const fp = $(".others").html();
  if (friendprofieloaded) {
    sessionStorage.setItem("friendprofile", fp);
    friendprofieloaded = false;
  }
  if (storydetailloaded) {
    sessionStorage.setItem("storydetail", fp);
    storydetailloaded = false;
  }
}
let notification_clicked = false;
function loadNotifications() {
  if (!notification_clicked) {
    $(".dropdown-content").css("display", "block");
    $.ajax({
      type: "GET",
      url: "/api/get_notification",
      success: function (response) {
        $(".notification_div").html(response);
      },
      error: function (err) {
        toastr(err);
      },
    });
  } else {
    $(".dropdown_menu").css("display", "none");
  }
  notification_clicked = !notification_clicked;
}
function loadMessanger(nothing, respon) {
  if (respon) {
    $(".messageappend").html(respon);
    $(".messagetop").css("display", "block");
  } else {
    ajaxcall("GET", "/messanger", loadMessanger);
  }
}
function lauchMessage(id, frmprofile) {
  id = id ? id : frmprofile.split("msglaunch")[1];
  loading(true);
  $.ajax({
    type: "GET",
    url: "/messages/api/get/" + id + "/",
    success: function (response) {
      loading();
      $("#addedmessagebox").remove();
      $(".previous_messageareaa").css("display", "none");
      $(".messageareaa").prepend(response);
      scroll();
      getMessage(id);
      arrangeElements();
    },
    error: function (err) {
      toastr(err);
    },
  });
}

//storyline
$("#search").submit(function (e) {
  e.preventDefault();
  const data = $(".searchbox").val();
  if (data.trim() == "") {
    $(".searchbox").val("");
    return;
  }
  $(".searchresult").css("display", "block");
  $(".shadow").css("display", "block");
  $.ajax({
    type: "GET",
    url: `/search/?search_query=${data}`,
    data: data,
    success: function (response) {
      $(".searchresult").html(response);
    },
    error: function (err) {
      $(".searchresult").css("display", "none");
      $(".shadow").css("display", "none");
      toastr(err);
    },
  });
});
function closeSearch() {
  $(".searchresult").html("Searching...");
  $(".searchresult").css("display", "none");
  $(".shadow").css("display", "none");
  $("input[name=search_query]").val("");
}

let sidenavOpened = false;
function toggleSidenav() {
  if (sidenavOpened) {
    document.removeEventListener("click", toggleSidenav);
    $(".sidenav").css({ top: "-300px", opacity: "0" });
  } else {
    setTimeout(() => {
      document.addEventListener("click", toggleSidenav);
    });
    $(".sidenav").css({ top: "50px", opacity: "1" });
  }
  sidenavOpened = !sidenavOpened;
}
function getFriendSuggestions() {
  loading(true);
  $.ajax({
    type: "GET",
    url: "/profile/api/friend_suggestions",
    success: function (response) {
      loading();
      openSidebar("Friend Suggestions", response);
    },
    error: function (err) {
      toastr(err);
    },
  });
}
function openSidebar(title, response) {
  sidenavOpened = true;
  toggleSidenav();
  $(".sidebar").css({ right: "0" });
  $(".title").html(
    `<div class="notoggle">${title}<span class='cross ml-5' onclick="closeSidebar()">X</span></div>`
  );
  $(".sideitem").html(response);
}
function closeSidebar() {
  let sidebar = $(".sidebar");
  const width = sidebar[0].clientWidth;
  console.log(sidebar, width);
  sidebar[0].style.right = `-${width + 2}px`;
}
function getFriendRequests() {
  loading(true);
  $.ajax({
    type: "GET",
    url: "/profile/api/friend_requests",
    success: function (response) {
      loading();
      openSidebar("Friend Requests", response);
    },
    error: function (err) {
      toastr(err);
    },
  });
}
function getRequestSent() {
  loading(true);
  $.ajax({
    type: "GET",
    url: "/profile/api/sent_requests",
    success: function (response) {
      loading();
      openSidebar("Sent Requests", response);
    },
    error: function (err) {
      toastr(err);
    },
  });
}

function ajaxcall(method, url, cb, data, dataType) {
  $.ajax({
    type: method,
    url: url,
    data: data,
    dataType: dataType,
    success: function (response) {
      cb("", response);
    },
    error: function (err) {
      toastr(err);
    },
  });
}
let errortimer;
function toastr(err, title, message, notError, showAsItIs) {
  $(".toastr").toggleClass("toastr-success", notError);
  try {
    clearInterval(errortimer);
  } catch (e) {}
  errortimer = setTimeout(closeError, 3000);
  $(".loading").css("display", "none");
  if (err.status == 0) {
    $(".toastr-title").html("No Internet");
    $(".toastr-msg").html("Please Check Your Connection.");
  } else {
    $(".toastr-title").html(
      title ? title : showAsItIs ? "" : `${err.status}  Server Error`
    );
    $(".toastr-msg").html(
      message
        ? message
        : showAsItIs
        ? ""
        : `Some Error Occured We are fixing it.`
    );
  }
  $(".toastr").css({ right: "1rem", opacity: 1 });
}
function closeError() {
  clearInterval(errortimer);
  $(".toastr").css({ right: "-450px", opacity: 0 });
}

function logout() {
  e.preventDefault();
  sessionStorage.clear();
  // e.unbind();
}
$("#logout").click(function (e) {
  e.preventDefault();
  sessionStorage.clear();
  $("form[action='/logout/']").submit();
});

function makeDark() {
  $("#matrixa-theme")[0].disabled = true;
  $("#dark-theme")[0].disabled = false;
  saveTheme("dark");
}
function theme(themeColor) {
  localStorage.setItem("theme", themeColor);
  applyTheme();
}

function applyTheme() {
  let themeColor = localStorage.getItem("theme");
  if(!themeColor){
    theme('matrixa');
    return false;
  }
  $("#darker").removeClass("darker-active");
  $("#lighter").removeClass("lighter-active");
  $("#matrixa").removeClass("darker-active");
    switch (themeColor) {
      case "dark":
        $("#dark-theme")[0].disabled = false;
        $("#matrixa-theme")[0].disabled = true;
        $("#darker").addClass("darker-active");
        break;
      case "light":
        $("#matrixa-theme")[0].disabled = true;
        $("#dark-theme")[0].disabled = true;
        $("#lighter").addClass("lighter-active");
        break;
      case "matrixa":
        $("#matrixa-theme")[0].disabled = false;
        $("#dark-theme")[0].disabled = true;
        $("#matrixa").addClass("darker-active");
        break;
    }
  
}
const modal = document.querySelector(".confirmmodal");
const ms = modal.style;
let body = document.querySelector("body");
let mo = modal.attributes.opened.value;
function openModal(title, message, yesCb, noCb) {
  if (title.toString() != "[object MouseEvent]") {
    modal.children[0].innerHTML = title ? title : "Confirmation Modal";
  }
  if (message) {
    modal.children[1].innerHTML = message;
  }
  let btns = modal.children[2].children[0];
  btns.children[0].addEventListener("click", yesCb);
  if (mo == "false") {
    ms.transform = "scale(1) translate(-50%,-50%)";
    ms.opacity = 1;
    ms.zIndex = 5;
    mo = "true";
    setTimeout(() => {
      modal.addEventListener("click", openModal);
    }, 1000);
  } else {
    ms.transform = "scale(.5) translate(-50%,-50%)";
    ms.opacity = 0;
    setTimeout(() => {
      btns.children[0].removeEventListener("click", yesCb);
      ms.transform = "scale(1.2) translate(-50%,-50%)";
      ms.zIndex = -5;
    }, 600);
    mo = "false";
  }
}
function toggleNotification() {
  const toggler = document.querySelector("#navbarDropdown");
  const isShown = toggler.getAttribute("aria-expanded");
  const target = document.querySelector(".dropdown-notification");
  if (isShown == "false") {
    // target.style.display='block';
    console.log(target);
    setTimeout((_) => {});
    setTimeout(() => {
      $(".dropdown-notification").css("top", "50px");
      document.addEventListener("click", toggleNotification);
    });
    toggler.setAttribute("aria-expanded", "true");
  } else {
    document.removeEventListener("click", toggleNotification);
    // target.style.display='none';
    target.style.top = `-${target.clientHeight + 2}px`;
    toggler.setAttribute("aria-expanded", "false");
  }
}
document
  .querySelector("#navbarDropdown")
  .addEventListener("click", toggleNotification);
  
  document.addEventListener('DOMContentLoaded',()=>{
    document.querySelectorAll("[height='30']").forEach(x=>console.log(x));

})