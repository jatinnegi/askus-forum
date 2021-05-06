const allUsersTab = document.getElementById("users");
const selectedUsersTab = document.getElementById("selected-users");
const activeBar = document.getElementById("active-bar");
let activeTab = allUsersTab;
const submitButton = document.getElementById("answer-request-submit-button");

function toggleTopmenu(event) {
  event.preventDefault();

  if (event.target.id === "all-users-list") {
    allUsersTab.classList.add("active");
    selectedUsersTab.classList.remove("active");
    activeBar.classList.add("left");
    activeBar.classList.remove("right");
    activeTab = allUsersTab;
  } else if (event.target.id === "selected-users-list") {
    selectedUsersTab.classList.add("active");
    allUsersTab.classList.remove("active");
    activeBar.classList.add("right");
    activeBar.classList.remove("left");
    activeTab = selectedUsersTab;
  } else {
  }
}

document.getElementById("box-container").addEventListener("click", (e) => {
  e.preventDefault();
  if (e.target.id === "box-container") {
    document.getElementById("box-container").classList.remove("active");
    document.querySelector("body").style = "overflowY: scroll;";
  }
});

fetch("/accounts/get_all_users/")
  .then((res) => res.json())
  .then((data) => {
    const users = data.users;

    users.forEach((user) => {
      const userElement = document.createElement("div");
      userElement.classList.add("user");
      userElement.dataset.username = user.username;
      userElement.innerHTML = `
        <div class='d-flex align-items-center ml-2'>
            <div class="img" style="background-image: url('${
              user.avatar
            }')"></div>
            <div class="ml-2">
                <strong>${user.username}</strong>
                <span>${user.answers} ${
        user.answers === 1 ? "answer" : "answers"
      }</span>
            </div>
        </div>
        <div style='pointer-events:none;'><img class='user-list-action' style="height:18px; width:18px;"/></div>
          `;

      userElement.addEventListener("click", (e) =>
        selectUser(e, user.username)
      );
      document.getElementById("users").appendChild(userElement);
    });
  })
  .catch((err) => console.log(err));

const selectedUsers = [];
const selectedUsersTotal = document.getElementById("selected-users-list-total");

function selectUser(e, username) {
  e.preventDefault();
  if (selectedUsers.includes(username)) {
    document.getElementById("users").appendChild(e.target);
    let index = selectedUsers.indexOf(username);
    selectedUsers.splice(index, 1);
    selectedUsersTotal.innerText = selectedUsers.length;

    if (selectedUsers.length === 0) {
      document.getElementById("no-selected-users").style =
        "display:block;text-align: center; padding: 20px 0;";
      selectedUsersTotal.classList.remove("show");
    }
  } else {
    if (selectedUsers.length === 0) {
      document.getElementById("no-selected-users").style = "display:none";
    }

    document.getElementById("selected-users").appendChild(e.target);
    selectedUsers.push(username);
    selectedUsersTotal.innerText = selectedUsers.length;
    selectedUsersTotal.classList.add("show");
  }

  if (selectedUsers.length === 0) {
    document.getElementById("answer-request-submit-button").style =
      "float:right; cursor: not-allowed";
    document.getElementById("answer-request-submit-button").disabled = true;
  } else {
    submitButton.style = "float:right; cursor: pointer";
    submitButton.disabled = false;
  }
}

const searchInput = document.getElementById("search");

searchInput.addEventListener("keyup", (e) => {
  if (activeTab === selectedUsersTab && selectedUsers.length === 0) return;
  Array.from(activeTab.children).forEach((user) => {
    if (
      user.dataset.username &&
      user.dataset.username.includes(e.target.value)
    ) {
      user.style.display = "flex";
    } else {
      user.style.display = "none";
    }
  });
});

document.getElementById("search").addEventListener("click", () => {
  document.getElementById("searchfield").focus();
});

submitButton.addEventListener("click", (e) => {
  e.preventDefault();

  fetch(`/question/${questionId}/requests/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFTOKEN": csrfToken,
    },
    body: JSON.stringify({
      users_list: selectedUsers,
    }),
  })
    .then((res) => {
      if (res.status === 201) {
        location.reload();
      }
    })
    .catch((err) => console.log(err));
});
