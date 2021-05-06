const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;

function answerVote(event, answerId, action) {
  event.preventDefault();

  fetch(`/answer/${answerId}/vote/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFTOKEN": csrfToken,
    },
    body: JSON.stringify({
      action,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById(`answer-upvote-total-${answerId}`).textContent =
        data.upvotes;
      document.getElementById(`answer-downvote-total-${answerId}`).textContent =
        data.downvotes;

      if (data.current_vote === "upvote") {
        document.querySelector(`#answer-upvote-${answerId} i`).classList =
          "fas fa-thumbs-up";
        document.querySelector(`#answer-downvote-${answerId} i`).classList =
          "far fa-thumbs-down";
      } else if (data.current_vote === "downvote") {
        document.querySelector(`#answer-downvote-${answerId} i`).classList =
          "fas fa-thumbs-down";
        document.querySelector(`#answer-upvote-${answerId} i`).classList =
          "far fa-thumbs-up";
      } else if (data.current_vote === "none") {
        document.querySelector(`#answer-upvote-${answerId} i`).classList =
          "far fa-thumbs-up";
        document.querySelector(`#answer-downvote-${answerId} i`).classList =
          "far fa-thumbs-down";
      } else {
      }
    })
    .catch((err) => console.log(err));
}

function commentVote(event, commentId, action) {
  event.preventDefault();

  fetch(`/comment/${commentId}/vote/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFTOKEN": csrfToken,
    },
    body: JSON.stringify({
      action,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById(`comment-upvote-total-${commentId}`).textContent =
        data.upvotes;
      document.getElementById(
        `comment-downvote-total-${commentId}`
      ).textContent = data.downvotes;

      if (data.current_vote === "upvote") {
        document.querySelector(`#comment-upvote-${commentId} i`).classList =
          "fas fa-thumbs-up";
        document.querySelector(`#comment-downvote-${commentId} i`).classList =
          "far fa-thumbs-down";
      } else if (data.current_vote === "downvote") {
        document.querySelector(`#comment-downvote-${commentId} i`).classList =
          "fas fa-thumbs-down";
        document.querySelector(`#comment-upvote-${commentId} i`).classList =
          "far fa-thumbs-up";
      } else if (data.current_vote === "none") {
        document.querySelector(`#comment-upvote-${commentId} i`).classList =
          "far fa-thumbs-up";
        document.querySelector(`#comment-downvote-${commentId} i`).classList =
          "far fa-thumbs-down";
      } else {
      }
    })
    .catch((err) => console.log(err));
}

function addComment(event, answerId) {
  event.preventDefault();
  const comment = document.getElementById(`comment-form-input-${answerId}`)
    .value;

  fetch(`/answer/${answerId}/comment/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFTOKEN": csrfToken,
    },
    body: JSON.stringify({
      comment,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      const section = document.createElement("section");

      section.id = `answer-comment-${data.id}`;

      section.innerHTML = `<div class="card p-2 mt-3">
                                <!-- comment header -->
                                <div class="d-flex">
                                    <div class="">
                                        <div id="home-questions-list-avatar"
                                            style="background-image: url('${data.user.avatar}')">
                                        </div>
                                    </div>
                                    <div class="flex-grow-1 pl-2">
                                        <a class="text-decoration-none text-capitalize h6 m-0"
                                            href="#">${data.user.username}</a>
                                        <p class="small m-0 text-muted">${data.uploaded_on}</p>
                                    </div>
                                    <div>
                                        <div class="dropdown">
                                            <a class="" href="#" role="button" id="dropdownMenuLink"
                                                data-toggle="dropdown" aria-haspopup="true"
                                                aria-expanded="false">
                                                <i class="fas fa-chevron-down"></i>
                                            </a>
  
                                            <div class="dropdown-menu"
                                                aria-labelledby="dropdownMenuLink">
                                                <a data-toggle="modal" href="#myModal"
                                                  class="dropdown-item text-primary"
                                                  onClick="deleteComment(event, ${data.id})">Delete</a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <!-- comment header -->
                                <!-- comment body -->
                                <div class="card-body p-0">
                                    <p class="card-text h7 mb-2">${data.content}</p>
                                    <a id="comment-upvote-${data.id}" class="card-link small"
                                        onClick="commentVote(event, ${data.id}, 'upvote')"
                                        href="#">
                                        <i
                                            class="far fa-thumbs-up"></i>
                                        <span
                                            id="comment-upvote-total-${data.id}">${data.upvotes}</span>
                                    </a>
                                    <a id="comment-downvote-${data.id}" class="card-link small"
                                        onClick="commentVote(event, ${data.id}, 'downvote')"
                                        href="#">
                                        <i
                                            class="far fa-thumbs-down"></i>
                                        <span
                                            id="comment-downvote-total-${data.id}">${data.downvotes}</span>
                                    </a>
                                </div>
                            </div>
                          </section>
                          </div>
                          <!-- comment card ends -->
  
                          </div>
                          </div>
                          <!-- collapsed comments ends -->
                          </footer>
                          <!-- post footer ends -->
                          </div>`;

      document
        .getElementById(`comments-container-${answerId}`)
        .prepend(section);

      document.getElementById(`comment-form-input-${answerId}`).value = "";

      document.getElementById(
        `comment-submit-button-${answerId}`
      ).disabled = true;
      document.getElementById(`comment-submit-button-${answerId}`).style =
        "cursor:not-allowed";
    })
    .catch((err) => console.log(err));
}

function commentInputChange(event, answerId) {
  if (event.target.value !== "") {
    document.getElementById(
      `comment-submit-button-${answerId}`
    ).disabled = false;
    document.getElementById(`comment-submit-button-${answerId}`).style =
      "cursor:pointer";
  } else {
    document.getElementById(
      `comment-submit-button-${answerId}`
    ).disabled = true;
    document.getElementById(`comment-submit-button-${answerId}`).style =
      "cursor:not-allowed";
  }
}

function deleteAnswer(event, answerId) {
  const modalActions = document.querySelectorAll(".modal-actions");
  const closeModal = document.getElementById("modal-close");

  modalActions.forEach((action) =>
    action.addEventListener("click", (e) => {
      if (e.target.dataset.action === "confirm") {
        fetch(`/answer/${answerId}/delete/`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFTOKEN": csrfToken,
          },
        }).then((res) => {
          if (res.status === 200) {
            location.reload();
          }
        });
      }
    })
  );
}

const homeAnswers = document.querySelectorAll(".home-answer");

homeAnswers.forEach((answer) => {
  if (answer.clientHeight === 300) {
    const aTag = document.createElement("a");
    aTag.innerHTML = `
      <a href="#" class="mt-2 d-block" onClick="displayFullAnswer(event, ${answer.dataset.answerid})">Read More</a>
    `;

    document
      .getElementById(`answer-container-${answer.dataset.answerid}`)
      .appendChild(aTag);

    document
      .getElementById(`home-answer-${answer.dataset.answerid}`)
      .classList.add("home-answer-overlay");
  }
});

function displayFullAnswer(event, answerId) {
  event.preventDefault();

  document.getElementById(`home-answer-${answerId}`).style =
    "max-height: inherit !important";
  document
    .getElementById(`home-answer-${answerId}`)
    .classList.remove("home-answer-overlay");

  event.target.style = "display: none !important";
}

function deleteComment(e, commentId) {
  e.preventDefault();

  const modalActions = document.querySelectorAll(".modal-actions");
  const closeModal = document.getElementById("modal-close");

  modalActions.forEach((action) =>
    action.addEventListener("click", (e) => {
      if (e.target.dataset.action === "confirm") {
        fetch(`/comment/${commentId}/delete/`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFTOKEN": csrfToken,
          },
        }).then((res) => {
          if (res.status === 200) {
            document.getElementById(`answer-comment-${commentId}`).style =
              "display:none;";

            const successAlert = document.createElement("div");

            successAlert.classList.add(
              "alert",
              "alert-success",
              "alert-dismissible",
              "fade",
              "show"
            );
            successAlert.innerHTML = `
                      Comment removed successfully!
                      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                      </button>`;

            document.getElementById("alerts-container").append(successAlert);
          }
        });
      }
    })
  );
}
