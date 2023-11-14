/************************************************************
                        TABS
 ************************************************************/

const tabButtons = document.querySelectorAll(".tabs li");
const tabContentBoxes = document.querySelectorAll(
  "#tab-content > div.schedule",
);

tabButtons.forEach((tabButton) => {
  tabButton.addEventListener("click", () => {
    tabButtons.forEach((button) => button.classList.remove("is-active"));
    tabButton.classList.add("is-active");
    const targetContentId = tabButton.dataset.target;

    tabContentBoxes.forEach((contentBox) => {
      if (contentBox.getAttribute("id") === targetContentId) {
        contentBox.classList.remove("is-hidden");
      } else {
        contentBox.classList.add("is-hidden");
      }
    });
  });
});

/************************************************************
                        ACCORDIANS
 ************************************************************/

let accordions = document.getElementsByClassName("accordion");

for (let accordion of accordions) {
  accordion.addEventListener("click", function () {
    this.classList.toggle("active");
    let panel = this.nextElementSibling;
    if (panel.style.maxHeight) {
      panel.style.maxHeight = null;
    } else {
      panel.style.maxHeight = panel.scrollHeight + "px";
    }
  });
}
