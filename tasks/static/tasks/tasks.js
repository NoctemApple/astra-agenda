document.addEventListener('DOMContentLoaded', function () {
    // Draw all existing connections on load
    fetchConnections();

    // Handle adding a new task
    document.getElementById('task-form').addEventListener('submit', function (e) {
        e.preventDefault();
        fetch('/add-task/', {
            method: 'POST',
            body: new FormData(this),
            headers: { 'X-CSRFToken': getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
            if (!data.error) {
                // Add task to board
                const taskDiv = document.createElement('div');
                taskDiv.classList.add('task');
                taskDiv.id = `task-${data.id}`;
                taskDiv.innerHTML = `<strong>${data.name}</strong>`;
                document.getElementById('task-board').appendChild(taskDiv);

                // Add task to selects
                addTaskToSelects(data.id, data.name);

                // Reset form
                this.reset();
            }
        });
    });

    // Handle adding a dependency
    document.getElementById('dependency-form').addEventListener('submit', function (e) {
        e.preventDefault();
        fetch('/add-dependency/', {
            method: 'POST',
            body: new FormData(this),
            headers: { 'X-CSRFToken': getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
            if (!data.error) {
                // Immediately draw new line
                const start = document.getElementById(`task-${data.prerequisite}`);
                const end = document.getElementById(`task-${data.target}`);
                if (start && end) {
                    new LeaderLine(start, end);
                } else {
                    console.warn("Tasks not found in DOM for dependency:", data);
                }
                this.reset();
            }
        });
    });
});

// Helper: Draw a line between tasks
function drawLine(fromId, toId) {
    const start = document.getElementById(`task-${fromId}`);
    const end = document.getElementById(`task-${toId}`);
    if (start && end) {
        new LeaderLine(start, end);
    }
}

// Helper: Add a task to both dependency form selects
function addTaskToSelects(id, name) {
    const targetSelect = document.getElementById('target_task');
    const prereqSelect = document.getElementById('prerequisite_task');

    const option1 = document.createElement('option');
    option1.value = id;
    option1.textContent = name;
    targetSelect.appendChild(option1);

    const option2 = document.createElement('option');
    option2.value = id;
    option2.textContent = name;
    prereqSelect.appendChild(option2);
}

// Fetch all dependencies from template and draw them
function fetchConnections() {
    const deps = JSON.parse(document.getElementById('dependencies-data').textContent);
    deps.forEach(dep => drawLine(dep.prerequisite_task_id, dep.target_task_id));
}

// CSRF helper
function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
}
