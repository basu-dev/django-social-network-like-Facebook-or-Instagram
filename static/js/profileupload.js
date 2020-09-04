let mydata;
let previousImageUrl = "";
let ppblob = null;
let storyblob = null;
let editblob = null;
let detin;
function showImagePreview(id, destination, showdiv, showcancelicon) {
  destin=destination;
  try {
    $(showcancelicon).css("z-index", "10");
  } catch (e) {}
  file = $("#" + id)[0].files[0];
  let fr = new FileReader();
  fr.readAsDataURL(file);
  fr.onloadend = function (e) {
    filetype = fr.result.split(":")[1].split(";")[0];
    if (
      filetype == "image/jpeg" ||
      filetype == "image/png" ||
      filetype == "image/svg+xml" ||
      filetype == "image/gif"
    ) {
      showPreview(showdiv, destination, e.target.result);
      let image = new Image();
      image.onload = function () {
        canvas = document.createElement("canvas");
        var context = canvas.getContext("2d");
        let ratio = image.width / image.height;
        function width() {
          if (image.width < 600) {
            return image.width;
          } else {
            return 550;
          }
        }
        function height() {
          return canvas.width / ratio;
        }
        canvas.width = width();
        canvas.height = height();
        context.drawImage(
          image,
          0,
          0,
          image.width,
          image.height,
          0,
          0,
          canvas.width,
          canvas.height
        );
        canvas.toBlob((x) => {
          switch (destin) {
            case ".pppreview":
              ppblob=x
              break;
            case ".storyfile":
              storyblob=x
            case "#editimage":
              editblob=x
          }
          
        }, `"${filetype}"`);
      };
      image.src = event.target.result;
    } else {
      $("#" + id)[0].value = "";
      toastr(
        "",
        "Invalid File Type",
        "Sorry!! This type of file cannot be uploaded"
      );
    }
  };
}
$("#ppform").submit(function (e) {
  e.preventDefault();
  data = new FormData(this);
  data.append("photo", ppblob, "ravenprofileimage.jpg" );
  ppblob=null;
  hideAndShow("#ppform", "#my_profile");
  previewimg = $(".pppreview").attr("src");
  $(".mypp").attr("src", previewimg);
  $(".profile_picture_loading").css("z-index", "5");
  $.ajax({
    type: "POST",
    url: "/update_pp/",
    data: data,
    contentType: false,
    processData: false,
    success: function (response) {
      toastr("","Profile Picture Updated Successfully !!!","",true,true)
      inputelem = $("#ppimg");
      inputelem[0].value = "";
      pp = response.picture;
      $(".profile_picture_loading").css("z-index", "-100");
      $(".profileimagestory").attr("src", "/storage/" + response.picture);
      $(".navpp").attr("src", "/storage/" + response.picture);
      story = getStoryWithImage(
        response,
        " added a profile picture.",
        `/storage/${pp}`
      );
      $(".profilestoriesappend").prepend(story);
    },
    error: function (err) {
      toastr(err);
    },
  });
});
$("#storyform").submit(function (e) {
  e.preventDefault();
  data = new FormData(this);
  if(storyblob!=null){
    data.append("images", storyblob, "ravenstory.jpg");
    storyblob=null;
  }
  loading(true);
  addStoryCancel();
  $.ajax({
    type: "POST",
    url: "/profile/my_profile/",
    contentType: false,
    processData: false,
    data: data,
    success: function (response) {
      toastr("","Story Added Successfully !!!","",true,true)
      inputelem = $("#storyinputfile");
      inputelem[0].value = "";
      loading();
      if (response.failed) {
        toastr(response, "Upload Failed", "Please Enter Valid Data");
      } else {
        pp = $(".pp").attr("src");
        story = getStoryWithImage(response, " added a story", pp);
        $(".profilestoriesappend").prepend(story);
      }
    },
    error: function (err) {
      toastr(err);
    },
  });
});
data = null;
$(".update_profile").submit(function (e) {
  e.preventDefault();
  data = new FormData(this);
  loading(true);
  $.ajax({
    type: "POST",
    url: "/profile/update_profile/",
    data: data,
    contentType: false,
    processData: false,
    success: function (response) {
      toastr("","Profile Updated Successfully !!!","",true,true)
      loading();
      ps = $(".profiledetail").children("b");
      ps[0].innerText = data.get("first_name");
      ps[1].innerText = data.get("last_name");
      ps[2].innerText = data.get("job");
      ps[3].innerText = data.get("address");
      ps[4].innerText = data.get("age");
      ps[5].innerText = data.get("contact_no");
      $(".mybio").html(data.get("bio"));
      showupdateProfile();
    },
    error: function (err) {
      toastr(err);
    },
  });
});
$("#update_story_form").submit(function (e) {
  e.preventDefault();
  data = new FormData(this);
  if(data.get('img').size!==0){
    if(editblob !=null) data.append('image',editblob,'ravenstory.jpg');
    editblob=null;
  }
  loading(true);
  $.ajax({
    method: "POST",
    url: "/updatestory",
    data: data,
    contentType: false,
    processData: false,
    success: function (response) {
      toastr("","Story Updated Successfully !!!","",true,true)
      loading();
      hideAndShow(".profile_edit", ".previous_messageareaa"),
        $(".editstorybody").html("");
      children = $(`.story${response.id}`).children();
      statusdiv = children[1];
      statusdiv.innerHTML = response.status;
      $("");
      if (response.picture) {
        try {
          $(`.storyimage${response.id}`).attr(
            "src",
            `/storage/${response.picture}`
          );
        } catch (e) {
          var imgfield = ` <div class="imagefield" id="likea${response.id}likea" ondblclick="like(this.id,1)">
          <img src="/storage/${response.picture}" class="storyimage storyimage${response.id}">
          </div>`;
          $(`#likea${response.id}likea`).replaceWith(imgfield);
        }
        $(`.imageurlhide${response.id}`).attr("id", response.imageid);
        $(`.imageurlhide${response.id}`).html(response.picture);
      }
      $(`#edittexthide${response.id}`).html(`b$890$${response.status}b$890$`);
    },
    error: function (err) {
      hideAndShow(".profile_edit", ".previous_messageareaa"), toastr(err);
    },
  });
});
resizeTextArea = (event) => {
  enterCount = 2;
  element = event.target;
  elementVal = element.value;
  var len = elementVal.length;
  if (elementVal.trim() != "") {
    for (var i = 0; i < len; i++) {
      if (elementVal[i] == "\n") {
        enterCount++;
      }
    }
    element.rows = enterCount;
  } else {
    element.value = "";
  }
};
function textareaFocused(element, focused) {
  var enterCount = 1;
  elementVal = element.value;
  len = elementVal.length;
  for (var i = 0; i < len; i++) {
    if (elementVal[i] == "\n") {
      enterCount++;
    }
  }
  if (focused) {
    element.rows = enterCount + 1;
  } else {
    element.rows = enterCount;
  }
}
function getStoryWithImage(response, storytype, pp) {
  if (response.picture) {
    var imgfield = ` <div class="imagefield" id="likea${response.id}likea" ondblclick="like(this.id,1)">
  <img src="/storage/${response.picture}" class="storyimage storyimage${response.id}">
  </div>`;
  } else {
    var imgfield = "";
  }
  story =
    `<div id="antxi${response.id}antxi">
<div class='card mb-2 pb-1 fordelete_${response.id}' id='${response.id}'>
 <div class='card-body story storyclick story${response.id}'id="${response.id}">
 <div class='card-title pb-2'>
 <div>
 <img class='pp mr-2 ml-2' height=30 width=30
 src='${pp}'>
 </div>
 <div><a class="mr-2" href='#'>${
   response.name
 }</a> ${storytype} on ${new Date()}.</div>
 </div>
 <pre class='card-text storybody text-justify'>${response.status}</pre>
 <span class="a" href="/storydetail/${
   response.id
 }/" onclick="route(this.attributes.href.value)">
 <div class="see_more_text">See Full Story</div>
 </span>
` +
    imgfield +
    `</div>
 <div class='ml-2'>
 <div class='ml-2 ${response.id}_likey'>0 Likes</div>
 <div class='like_show${response.id} ml-2'></div>
 </div>
 <div class="btn-group">
 <div type='submit' id='like${response.id}like' onclick="like(this.id,2)" class='like ml-3 mb-0'>Like</div>
 <button type='submit' id="delete${response.id}delete" onclick="deleteStory(this.id)"
 class='btn-sm delete ml-3 mb-0'>Delete</button>
 <div class="like ml-3" id=${response.id} onclick="editbtn(this)">
 Edit
 <div id="edittexthide${response.id}" style="display:none">b$890$${response.status}b$890$</div>
 <div style="display:none">
 <p id=${response.imageid} class='imageurlhide${response.id}'>>
 ${response.picture}
 </p>
 </div>
 </div>
 </div>
 <textarea onkeyup="commentt($(this))" placeholder="Comment..." id='comment${response.id}comment' name='comment'
 class='commentarea ' rows=1></textarea>
 <div style="overflow-y:scroll;max-height:30vh;">
 <div class="card commentupdate_${response.id}"></div>
 </div>
</div>
</div>
`;
  return story;
}
