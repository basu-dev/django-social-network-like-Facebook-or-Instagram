
  "use strict"; 
function loadProfile() {
  loading(true),
    $.ajax({
      type: "GET",
      url: `/profile/api/get_profile_stories`,
      success: function (response) {
        loading();
        $(".profilestoriesappend").append(response);
      },
      error: function (err) {
        toastr(err);
      },
    });
}
let profileclicked = false;
function showEdit() {
  if (profileclicked) {
    $("#profile_picture").css("display", "none");
    profileclicked = !profileclicked;
  } else {
    previousImageUrl = $(".pp").attr("src");
    $("#profile_picture").css("display", "block");
    profileclicked = !profileclicked;
  }
}
function startStoryAdd(textarea) {
  let val = $("#" + textarea).val();
  let length = val.length;
  if (length > 0) {
    $(".addstorycancel").css("z-index", "10");
  } else {
    $(".addstorycancel").css("z-index", "-5");
  }
}
function addStoryCancel() {
  $(".storypreview").css("display", "none");
  $(".addstorycancel").css("z-index", "-5");
  $(".textarea_profile").val("");
  let inputelem = $("#storyinputfile");
  inputelem[0].value = "";
  storyblob=null;
}
function hidePPForm(className) {
  $("." + className).attr("src", previousImageUrl);
  hideAndShow("#ppform", "#my_profile");
  let inputelem = $("#ppimg");
  inputelem[0].value = "";
  ppblob=null;
}
function showPreview(showdiv, selector, src) {
  try {
    $(showdiv).css("display", "block");
  } catch (e) {}

  $(selector).attr("src", src);
}
function showupdateProfile(truth) {
  if (truth) {
    hideAndShow("#my_profile", "#update_profile");
    hideAndShow("#ppform", "");
  } else {
    hideAndShow("#update_profile", "#my_profile");
  }
}
let updatejsloaded = false;
function editbtn(div) {
  $(".profile_edit").css("display", "block");
  let inputelem = $("#editimageinput");
  inputelem[0].value = "";
  $("#addedmessagebox").remove();
  hideAndShow(".previous_messageareaa", ".editarea");
  let body = div.innerHTML;
  let storyId = div.id;
  let url = body.split("post-images/");
  let storybodyhtml = document.getElementById("edittexthide" + storyId).innerHTML;
  body = storybodyhtml.split("b$890$")[1];
  try {
    let imageId = $(".imageurlhide" + storyId).attr("id");
    url = url[1].split("</p>")[0];
    $("#editimage").attr("src", `/storage/post-images/${url}`);
    $("#imageId").attr("value", imageId);
  } catch (e) {
    console.log(e);
  }
  const textarea = $("#editstorybody");
  textarea[0].value = body;
  textarea[0].defaultValue = body;
  $("#storyId").attr("value", storyId);
}

function cancelEdit() {
  hideAndShow(".editarea", ".previous_messageareaa");
  let inputelem = $("#editimageinput");
  inputelem[0].value = "";
  $("#editimage").attr("src", "");
}

let firstidloaded = false;
let firstId = "";
function loadMoreProfile(value) {
  let lastId = value.split("#^&*")[1].split("n")[0];
  let firstid = value.split("#^&*")[1].split("n")[1];
  if (firstidloaded === false) {
    firstId = value.split("#^&*")[1].split("n")[1];
    firstidloaded = true;
  } else {
    firstid = firstId;
  }
  loading(true),
    $.ajax({
      type: "GET",
      url: `/profile/api/get_more_profile_stories/${lastId}/${firstid}`,
      success: function (response) {
        const btn = document.getElementById(value);
        btn.remove();
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
        $(".profilestoriesappend").append(response);
      },
    });
}
let selectedStoryId = "";
function deleteStory(value) {
  openModal(
    "Confirmation",
    "Do you really want to delete this story?",
    confirmDelete
  );
  selectedStoryId = value.split("delete")[1];
}
function confirmDelete() {
  $.ajax({
    url: "/profile/api/delete_story/" + selectedStoryId + "/",
    type: "POST",
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function (data) {

      if (data.success == "successful") {
        toastr("","Story Deleted Successfully !!!","",true,true)
        $(".fordelete_" + selectedStoryId).remove();
      }
    },
    error: function (err) {
      toastr(err);
    },
  });
}
