document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".complete-toggle").forEach(button => {
    button.addEventListener("click", () => {
      const taskId = button.dataset.taskId;
      fetch(`/tasks/${taskId}/complete/`, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": getCookie("csrftoken"),
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.completed) {
          button.innerText = "✅ Completed";
        } else {
          button.innerText = "❌ In Progress";
        }
      })
      .catch(err => console.error("Error:", err));
    });
  });
});

// Helper for CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
