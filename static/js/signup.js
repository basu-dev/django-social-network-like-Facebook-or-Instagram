confirm_password_touched = false;
username_valid = false;
password_valid = false;
confirm_password_valid = false;
fvalid = false;
lvalid = false;
function validateUsername(id) {
  $("#usrreq").css("display", "none");
  val = $(`#${id}`).val();
  $.ajax({
    type: "POST",
    url: "/username_validate/",
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      value: val
    },
    success: function(response) {
      $(".backend-u-err").css("display", "none");
      if (response.exist === true) {
        username_valid = false;
        $("#uservalmsg").css("display", "block");
        $("#invalidusername").css("display", "none");
        newusername = tryNewUsername(val);
        $("#suggestuser").html(`Try ${newusername}`);
      } else if (response.invalid === true) {
        username_valid = false;
        $("#invalidusername").css("display", "block");
        $("#uservalmsg").css("display", "none");
      } else {
        username_valid = true;
        showButton();
        $("#uservalmsg").css("display", "none");
        $("#invalidusername").css("display", "none");
      }
    }
  });
}
pvalue = "";
function validatePassword(value) {
  pvalue = value;
  errormsg = "Password Must Be At Least 6 Characters Long.";
  $(".backend-p-err").css("display", "none");
  if (pvalue.length < 6) {
    password_valid = false;
    displayErrorMsg("#pasvalmsg", errormsg);
    $("#cpvalmsg").css("display", "none");
  } else {
    $("#pasvalmsg").css("display", "none");
    password_valid = true;
    if (confirm_password_touched == true) {
      validateConfirmPassword("password2");
      showButton();
    }
  }
}
function validateConfirmPassword(id) {
  if (password_valid) {
    cvalue = $(`#${id}`).val();
    if (cvalue === pvalue) {
      confirm_password_valid = true;
      $("#cpvalmsg").css("display", "none");
    } else {
      $("#cpvalmsg").css("display", "block");
      confirm_password_valid = false;
    }
  } else {
    $("#cpvalmsg").css("display", "none");
  }
  showButton();
}
function showButton() {
  if (
    username_valid &&
    password_valid &&
    confirm_password_valid &&
    fvalid &&
    lvalid
  ) {
    $("button")[0].disabled = false;
  } else {
    $("button")[0].disabled = true;
  }
}
function tryNewUsername(val) {
  return (newusername = val.concat(
    Math.round(Math.random() * Math.random() * 876).toString()
  ));
}
function checkP(value) {
  if (value == "") {
    displayErrorMsg("#pasvalmsg", "Password Field Required");
  }
}
function checkU(value) {
  if (value == "") {
    confirm_password_valid = false;
    $("#usrreq").css("display", "block");
  }
}
function displayErrorMsg(selector, msg) {
  $(selector).css("display", "block");
  $(selector).text(msg);
}
function checkCP(value) {
  confirm_password_touched = true;
  if (value == "" && password_valid) {
    confirm_password_valid = false;
    $("#cpvalmsg").css("display", "block");
  }
}
function checkF(value, selector, n) {
  if (value == "") {
    if (n == "f") {
      fvalid = false;
    } else {
      lvalid = false;
    }
    $(selector).css("display", "block");
  } else {
    $(selector).css("display", "none");

    if (n == "f") {
      fvalid = true;
    } else {
      lvalid = true;
    }
  }
  showButton();
}
function showPassword(show, name) {
  if (show.attributes.clicked.value == "false") {
    show.children[0].style.border = "4px solid var(--show-eye-color)";
    show.attributes.clicked.value = "true";
    document.getElementsByName(name)[0].type = "text";
  } else {
    show.attributes.clicked.value = "false";
    show.children[0].style.border = "2px solid var(--show-eye-color)";
    document.getElementsByName(name)[0].type = "password";
  }
}
