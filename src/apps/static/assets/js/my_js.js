function openPopup() {
    document.getElementById("popup").style.display = "block"; // Display the popup
    return "opened";
  }
  
  function closePopup() {
    document.getElementById("popup").style.display = "none"; // Hide the popup
    return "closed";
  }

function align_popups() {
    var popups = document.getElementsByClassName("overlay");
    var n_popups = popups.length;
    var offset = 0;
    for (let i = 0; i < n_popups; i++) {
        popups[i].style.top = offset+"px";
        offset += popups[i].offsetHeight + 2;
    }
 }

 function add_close_functionality() {
    var close_spans= document.getElementsByClassName("message_close");  
    var n_close_spans = close_spans.length;
    for (let i = 0; i < n_close_spans; i++) {
        close_spans[i].addEventListener("click", function() {
          this.parentElement.remove();
          align_popups();
        });
    }
 }


document.addEventListener('DOMContentLoaded', function() {
  // Your JavaScript code here
  align_popups();  
  add_close_functionality();
});