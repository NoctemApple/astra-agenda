document.addEventListener('DOMContentLoaded', () => {
    const depsContainer = document.getElementById('dependencies-container');
    const board = document.getElementById('task-board');

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

        fetch('add/', {
            method: 'POST',
            body: new FormData(e.target),
            headers: { 'X-CSRFToken': getCSRFToken() }
        })
        .then(res => res.json())
        .then(data => {
            if (!data.error) {
                addTaskToBoard(data.id, data.name);

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
});
