"use strict";
  let confirm_password_touched = false;
let username_valid = true;
let password_valid = false;
let confirm_password_valid = false;
let fvalid = false;
let lvalid = false;
function ajax({type,url,data,success,error}){
 let http= new XMLHttpRequest();
 let body=new FormData();
 Object.entries(data).forEach(x=>{
   body.append(x[0],x[1]);
 })
 http.open(type,url,true);
 http.onreadystatechange=function(ev){
   if(http.readyState==4 && http.status==200){
     success(JSON.parse(http.response))
   }
 }
 http.send(body);
}
function $(selector) {
  let elements = document.querySelector(selector);
  if (elements == undefined) {
    elements=null;
  }
  let self = {
    element: elements,
    html: function (body) {
      return self.element?(body ? (self.element.innerHTML = body) : self.element.innerHTML):null;
    },
    text: function (body) {
      return self.element?(body ? (self.element.innerText = body) : self.element.innerText):null;
    },
    val: function (value) {
      return self.element?(value ? (self.element.value = value) : self.element.value):null;
    },
    css: function (key, val) {
      return self.element?(self.element.style[key] = val):null;
    },
    disabled: function (val) {
      return self.element?(self.element.disabled = val):null;
    }

  };
  return self;
}
function validateUsername(id) {
  $("#usrreq").css("display", "none");
  const val = $(`#${id}`).val();
  ajax({
    type: "POST",
    url: "/username_validate/",
    data: {
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      value: val,
    },
    success: function (response) {
      $(".backend-u-err").css("display", "none");
      if (response.exist === true) {
        username_valid = false;
        $("#uservalmsg").css("display", "block");
        $("#invalidusername").css("display", "none");
        let newusername = tryNewUsername(val);
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
    },
  });
}
let pvalue = "";
function validatePassword(value) {
  pvalue = value;
  const errormsg = "Password Must Be At Least 6 Characters Long.";
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
    const cvalue = $(`#${id}`).val();
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
  // console.log($('button'))
  console.log(username_valid,password_valid,confirm_password_valid,fvalid,lvalid);
  if (
    username_valid &&
    password_valid &&
    confirm_password_valid &&
    fvalid &&
    lvalid
  ) {
    $("button").disabled(false);
  } else {
    $("button").disabled(true)
  }
}
function tryNewUsername(val) {
  return val.concat(Math.round(Math.random() * Math.random() * 876).toString());
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
show.children[0].style.border = "4px solid #c1bdbd";    
    show.attributes.clicked.value = "true";
    document.getElementsByName(name)[0].type = "text";
  } else {
    show.attributes.clicked.value = "false";
    show.children[0].style.border = "2px solid #c1bdbd";
    document.getElementsByName(name)[0].type = "password";
  }
}
