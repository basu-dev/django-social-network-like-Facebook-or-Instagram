
  "use strict";
  let firstfriendId = "";
  let firstfriendidloaded = false;
const loadMoreProfileUser=(value)=> {
  let firstid;
let username=(/profile\/(.+)/.exec(location.hash)[1]) || (/profile\/(.+)\//.exec(location.hash));
  let lastId = value.split("f1*%$#1f")[0].split("n")[0];
  if (firstfriendidloaded === false) {
    firstfriendId = firstid = value.split("f1*%$#1f")[0].split("n")[1];
    firstfriendidloaded = true;
  } else {
    firstid = firstfriendId;
  }
  loading(true),
    $.ajax({
      type: "GET",
      url: `/profile/api/get_more_profile_stories/${username}/${lastId}/${firstid}`,
      success: function(response) {
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
        $(".userprofilestoriesappend").append(response);
      }
    });
}


 