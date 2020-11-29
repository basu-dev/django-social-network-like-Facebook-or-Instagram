function showButton() {
  if (
    document.getElementsByName("username")[0].validity.valid &&
    document.getElementsByName("password")[0].validity.valid
  ) {
    document.getElementsByTagName("button")[0].disabled = false;
  } else {
    
    document.getElementsByTagName("button")[0].disabled = true;
  }
}
function showPassword(show,name){
  if(show.attributes.clicked.value=='false'){
      show.children[0].style.border='4px solid #c1bdbd';
      show.attributes.clicked.value='true'
      document.getElementsByName(name)[0].type="text"
  }
  else{
      show.attributes.clicked.value='false'
      show.children[0].style.border='2px solid #c1bdbd';
      document.getElementsByName(name)[0].type="password"
  }
}
