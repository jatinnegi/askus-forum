const username = JSON.parse(
  document.getElementById("user-username").textContent
);
const csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0]
  .value;

const bioInput = document.getElementById("profile-bio-input");
const firstNameInput = document.getElementById("profile-first-name-input");
const lastNameInput = document.getElementById("profile-last-name-input");

bioInput.setAttribute("size", bioInput.getAttribute("placeholder").length);
firstNameInput.setAttribute(
  "size",
  firstNameInput.getAttribute("placeholder").length
);
lastNameInput.setAttribute(
  "size",
  lastNameInput.getAttribute("placeholder").length
);

function inputDisplay(event, target) {
  event.preventDefault();
  let targetInput = null;

  if (target === "bio")
    targetInput = document.getElementById("profile-bio-input");
  if (target === "first_name")
    targetInput = document.getElementById("profile-first-name-input");
  if (target === "last_name")
    targetInput = document.getElementById("profile-last-name-input");

  if (event.target.classList.value === "fas fa-share-square fa-sm") {
    const inputValue = targetInput.value;
    let body = {};

    if (target === "bio") body.bio = inputValue;
    if (target === "first_name") body.first_name = inputValue;
    if (target === "last_name") body.last_name = inputValue;

    fetch(`/accounts/@/${username}/update/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFTOKEN": csrfmiddlewaretoken,
      },
      body: JSON.stringify(body),
    })
      .then((res) => res.json())
      .then((data) => {
        let placeholderText = "";

        if (target === "bio") placeholderText = "Enter your bio here";
        if (target === "first_name") placeholderText = "-";
        if (target === "last_name") placeholderText = "-";

        if (data[target] === "")
          targetInput.setAttribute("placeholder", placeholderText);
        else targetInput.setAttribute("placeholder", data[target]);

        targetInput.setAttribute(
          "size",
          targetInput.getAttribute("placeholder").length
        );
      })
      .catch((err) => console.log(err));

    targetInput.disabled = true;
    targetInput.classList.remove("input-active");
    event.target.classList.value = "fas fa-edit fa-sm";
  } else {
    targetInput.disabled = false;
    targetInput.focus();
    targetInput.selectionStart = targetInput.selectionEnd =
      targetInput.value.length;
    targetInput.setAttribute("placeholder", "");

    targetInput.classList.add("input-active");
    // bioLimit.style = "display:inline;";
    event.target.classList.value = "fas fa-share-square fa-sm";
  }
}

const avatarInput = document.querySelector('input[type="file"]');

avatarInput.addEventListener("change", (e) => {
  document.getElementById("avatar-update").click();
});

function displayAvatarFile(event) {
  event.preventDefault();
  avatarInput.click();
}

function showFullAnswer(event, answerId) {
  event.preventDefault();

  document.getElementById(`profile-answer-${answerId}`).style =
    "max-height:inherit";

  event.target.style = "display:none;";
}
