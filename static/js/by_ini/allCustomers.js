let viewButton = document.querySelectorAll("button.view-button");

for (i = 0; i < viewButton.length; i++) {
  viewButton[i].addEventListener("click", function() {
    location.href = "dashboard__patient.html";
  });
}
