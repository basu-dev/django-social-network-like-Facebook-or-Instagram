"use strict";
$(document).ready(function () {
  let scripts=['main.js','message.js','likecomment.js','friendreq.js','friend_profile.js'];
  scripts=scripts.map(x=>`<script src="/static/js/${x}"></script>`);
  scripts.forEach(x=>$("body").append(x));
  applyTheme();
  setTimeout(()=>{
    loadFriends();
    loadMessanger();
    
  })
  if (location.hash) {
    hashchanged();
  } else {
    loadStories();
  }
  
});
let navppclicked = false;
let storiesloaded = false;
function loadStories() {
  if (!storiesloaded) {
    loading(true),
      $.ajax({
        type: "GET",
        url: `/stories/get_stories/`,
        success: function (response) {
          loading();
          $(".stories").html(response);
          storiesloaded = true;
          hideAndShow(".myprofile", ".stories");
        },
        error: function (err) {
          toastr(err);
        },
      });
  } else {
    hideAndShow(".myprofile", ".stories");
    $(".others").html("");
  }
}

function loadMyProfile(no, hardload) {
  if (!navppclicked) {
    loading(true);
    $.ajax({
      type: "GET",
      url: "/profile/my_profile/",
      data: navppclicked,
      success: function (response) {
        if (!no) {
          storeProfile();
        }
        navppclicked = true;
        $(".myprofile").html(response);
        loadProfile();
        hideAndShow(".stories", ".myprofile");
        hideAndShow(".others", "");
        $(".others").html("");
      },
      error: function (err) {
        toastr(err);
      },
    });
  } else {
    hideAndShow(".stories", ".myprofile");
    hideAndShow(".others", "");
    $(".others").html("");
  }
}
let friend_profile_script_loaded=false;
function loadUserProfile(div, username) {
  loading(true);
  let name = "";
  let url=""
  if (div != "") {
    url = div[0].attributes.href.value;
    name = url.split("/")[2];
  } else if (div === "" && username) {
    name = username;
    url = `/profile/${username}/`;
  }
  $.ajax({
    type: "GET",
    url: url,
    success: function (response) {
      loading();
      if (response.isuser) {
        location.hash = "my_profile";
      } else {
        $(".others").html("");
        $(".others").html(response);
        hideAndShow(".myprofile", ".others");
        hideAndShow(".stories", "");
        loadUserProfileStories(url);
        friend_profile_script_loaded=true;
      }
    },
    error: function (err) {
      toastr(err);
    },
  });
}
function loadUserProfileStories(url) {
  const username = url.split("/")[2];
  loading(true),
    $.ajax({
      type: "GET",
      url: `/profile/api/get_profile_stories/${username}`,
      success: function (response) {
        loading();

        $(".userprofilestoriesappend").append(response);
      },
      error: function (err) {
        toastr(err);
      },
    });
}
function getStoryDetail(div, response, id, fromback) {
  if (div == "" && response != "") {
    $(".others").html("");
    $(".others").html(response);
    hideAndShow(".stories", ".others");
    hideAndShow(".myprofile", "");
    loading();
  } else {
    loading(true);
    let url="";
    if (div == "" && id) {
      url = `/storydetail/${id}/`;
      ajaxcall("GET", url, getStoryDetail);
    } else if (div != null) {
      url = div[0].attributes.href.value;
      ajaxcall("GET", url, getStoryDetail);
    } else if (fromback) {
      ajaxcall("GET", fromback, getStoryDetail);
    }
  }
}
window.onhashchange = hashchanged;
function hashchanged() {
  let hashvalue = location.hash.replace("#", "");
  try {
    hashvalue = hashvalue.split("/")[0];
  } catch (e) {
    console.log(e);
  }
  switch (hashvalue) {
    case "":
      loadStories();
      break;
    case "my_profile":
      loadMyProfile();
      break;
    case "profile":
      let username = location.hash.split("/")[1];
      loadUserProfile("", username);
      break;
    case "storydetail":
      let id = location.hash.split("/")[1];
      let x = id.split("o673o");
      let recoveredid = x[0] / x[1];
      if (recoveredid) {
        getStoryDetail("", "", recoveredid);
      } else {
        toastr("", "404 ", "Story  With Id " + id + " Not Found");
      }
      break;
    default:
      loadStories();
  }
}
function route(link) {
  if (link[0] == "/") {
    link = link.slice("1");
  }
  if (link.includes("storydetail")) {
    let id = link.split("/")[1];
    let randomnumber = parseInt(Math.random() * 378078596);
    let newid = randomnumber * id;
    let requiredid = newid.toString() + "o673o" + randomnumber.toString();
    link = `storydetail/${requiredid}`;
  }
  location.hash = `#${link}`;
}
