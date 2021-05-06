const questionId = JSON.parse(
  document.getElementById("question-id").textContent
);
const answerSubmitButton = document.getElementById("answer-submit-button");
const answersContainer = document.getElementById("answers-container");

const csrfmiddlewaretoken = document.getElementsByName("csrfmiddlewaretoken")[0]
  .value;

answerSubmitButton.addEventListener("click", (e) => {
  console.log("inside here");
  e.preventDefault();
  const content = CKEDITOR.instances["ckeditor_content"].getData();
  const anonymous = document.getElementById("answer-form-anonymous").checked;

  fetch(`/answer/${questionId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFTOKEN": csrfmiddlewaretoken,
    },
    body: JSON.stringify({
      csrfmiddlewaretoken,
      content,
      anonymous,
    }),
  })
    .then((res) => {
      if (res.status === 201) {
        location.reload();
      }
    })
    .catch((err) => console.log(err));
});

setTimeout(() => {
  CKEDITOR.instances["ckeditor_content"].on("change", (e) => {
    if (CKEDITOR.instances["ckeditor_content"].getData() === "") {
      answerSubmitButton.disabled = true;
      answerSubmitButton.style = "cursor: not-allowed";
    } else {
      answerSubmitButton.disabled = false;
      answerSubmitButton.style = "cursor: pointer";
    }
  });
}, 2000);

function questionVote(event, action) {
  event.preventDefault();

  fetch(`/question/${questionId}/vote/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFTOKEN": csrfmiddlewaretoken,
    },
    body: JSON.stringify({
      action,
    }),
  })
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("question-upvote-total").textContent =
        data.upvotes;
      document.getElementById("question-downvote-total").textContent =
        data.downvotes;

      if (data.current_vote === "upvote") {
        document.querySelector("#question-upvote i").classList =
          "fas fa-thumbs-up";
        document.querySelector("#question-downvote i").classList =
          "far fa-thumbs-down";
      } else if (data.current_vote === "downvote") {
        document.querySelector("#question-downvote i").classList =
          "fas fa-thumbs-down";
        document.querySelector("#question-upvote i").classList =
          "far fa-thumbs-up";
      } else if (data.current_vote === "none") {
        document.querySelector("#question-upvote i").classList =
          "far fa-thumbs-up";
        document.querySelector("#question-downvote i").classList =
          "far fa-thumbs-down";
      } else {
      }
    })
    .catch((err) => console.log(err));
}

function deleteQuestion(event, questionId) {
  const modalActions = document.querySelectorAll(".modal-actions");
  const closeModal = document.getElementById("modal-close");

  modalActions.forEach((action) =>
    action.addEventListener("click", (e) => {
      if (e.target.dataset.action === "confirm") {
        fetch(`/question/${questionId}/delete/`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFTOKEN": csrfToken,
          },
        }).then((res) => {
          if (res.status === 200) {
            window.location = "/";
          }
        });
      }
    })
  );
}
