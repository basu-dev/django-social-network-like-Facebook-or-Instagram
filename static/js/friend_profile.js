firstId = "";
firstidloaded = false;
function loadMoreProfileUser(value) {
  lastId = value.split("f1*%$#1f")[0].split("n")[0];
  if (firstidloaded === false) {
    firstId = firstid = value.split("f1*%$#1f")[0].split("n")[1];
    firstidloaded = true;
  } else {
    firstid = firstId;
  }
  loading(true),
    $.ajax({
      type: "GET",
      url: `/profile/api/get_more_profile_stories/${username}/${lastId}/${firstid}`,
      success: function(response) {
        btn = document.getElementById(value);
        btn.remove();
        let result = response.split("antxi");
        for (i = 0; i < result.length; i++) {
          if (i % 2 != 0) {
            let div = document.getElementById(`antxi${result[i]}antxi`);
            if (div != null) {
              div.remove();
            }
          }
        }
        loading();
        $(".userprofilestoriesappend").append(response);
      }
    });
}
