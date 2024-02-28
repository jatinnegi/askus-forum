let totalRequests = 0;

fetch("/accounts/answers/requests/")
  .then((res) => res.json())
  .then((data) => {
    const requests = data;

    if (requests.length > 0) {
      document.getElementById("empty-list-text").style = "display:none";
      totalRequests = requests.length;
    }

    requests.forEach((request) => {
      const liTag = document.createElement("li");
      liTag.classList.add("list-group-item", "p-3");

      liTag.innerHTML = `
      <a href='/question/${
        request.question_id
      }/' style="font-weight:600; font-size: 1.1rem;" class="mb-0 text-primary">${
        request.content
      }</a>
      <p class="mt-2">answer requested by <a href='/accounts/@/${
        request.username
      }'>${request.username}</a> ${
        request.answered
          ? `<br /><small class="text-secondary">*You have answered this question before</small>`
          : ""
      }</p>
      <button onClick="deleteRequest(event, ${
        request.answer_request_id
      })" class='btn btn-danger btn-sm'>Cancel</button>
      `;

      document.getElementById("answer-request-list").appendChild(liTag);
    });
  })
  .catch((err) => console.log(err));

function deleteRequest(e, pk) {
  e.preventDefault();

  fetch(`/accounts/answer/request/${pk}/delete/`)
    .then((res) => {
      if (res.status === 200) {
        e.target.parentElement.style = "display:none;";

        totalRequests--;
        console.log(totalRequests);
        if (totalRequests === 0)
          document.getElementById("empty-list-text").style = "display: block";
      }
    })
    .catch((err) => console.log(err));
}
