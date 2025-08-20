document.addEventListener('DOMContentLoaded', () => {
    const depsContainer = document.getElementById('dependencies-container');
    const board = document.getElementById('task-board');

    // Draw existing dependencies on page load
    fetchConnections();

    // Populate dependency select options from existing tasks
    function populateTaskOptions(select) {
        document.querySelectorAll('.task').forEach(taskDiv => {
            const option = document.createElement('option');
            option.value = taskDiv.id.replace('task-', '');
            option.textContent = taskDiv.textContent;
            select.appendChild(option);
        });
    }

    // Add new dependency row
    document.getElementById('add-dependency-btn').addEventListener('click', () => {
        const div = document.createElement('div');
        div.classList.add('dependency-row');

        const select = document.createElement('select');
        select.name = "dependencies";
        populateTaskOptions(select);

        const typeSelect = document.createElement('select');
        typeSelect.name = "dependency_types";
        typeSelect.innerHTML = `
            <option value="ALL">Required (All)</option>
            <option value="ONE">Required (One-of)</option>
            <option value="OPT">Optional</option>
        `;

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.textContent = 'x';
        removeBtn.addEventListener('click', () => div.remove());

        div.appendChild(select);
        div.appendChild(typeSelect);
        div.appendChild(removeBtn);

        depsContainer.appendChild(div);
    });

    // Submit task form via AJAX
    document.getElementById('task-form').addEventListener('submit', e => {
        e.preventDefault();

        fetch('/add-task/', {
            method: 'POST',
            body: new FormData(e.target),
            headers: { 'X-CSRFToken': getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
            if (!data.error) {
                // Add task to board
                addTaskToBoard(data.id, data.name);

                // Clear form and dependencies
                e.target.reset();
                depsContainer.innerHTML = '';
            } else {
                console.error(data.messages);
            }
        });
    });

    function getCSRFToken() {
        return document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
    }

    function addTaskToBoard(id, name) {
        const div = document.createElement('div');
        div.classList.add('task');
        div.id = `task-${id}`;
        div.textContent = name;
        board.appendChild(div);
    }

    // Draw dependency lines
    function drawLine(fromId, toId) {
        const start = document.getElementById(`task-${fromId}`);
        const end = document.getElementById(`task-${toId}`);
        if (start && end) new LeaderLine(start, end);
    }

    function fetchConnections() {
        const deps = JSON.parse(document.getElementById('dependencies-data').textContent);
        deps.forEach(dep => drawLine(dep.prerequisite_task_id, dep.target_task_id));
    }
});
