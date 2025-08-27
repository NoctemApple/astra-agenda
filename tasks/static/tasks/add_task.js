document.addEventListener('DOMContentLoaded', () => {
    const depsContainer = document.getElementById('dependencies-container');
    const addDependencyBtn = document.getElementById('add-dependency-btn');

    // Read JSON of existing tasks
    let existingTasks = [];
    try {
        const el = document.getElementById('existing-tasks');
        if (el) existingTasks = JSON.parse(el.textContent || el.innerText);
    } catch (e) {
        console.warn("failed to parse existing tasks JSON", e);
    }

    function populateTaskOptions(select) {
        existingTasks.forEach(task => {
            const option = document.createElement('option');
            option.value = task.id;
            option.textContent = task.name;
            select.appendChild(option);
        });
    }

    function createDependencyRow() {
        const wrapper = document.createElement('div');
        wrapper.className = 'dependency-row d-flex gap-2 align-items-center mb-2';

        const select = document.createElement('select');
        select.name = 'dependencies';
        select.className = 'form-select';
        populateTaskOptions(select);

        const typeSelect = document.createElement('select');
        typeSelect.name = 'dependency_types';
        typeSelect.className = 'form-select';
        typeSelect.innerHTML = `
            <option value="ALL">Required (All)</option>
            <option value="ONE">Required (One-of)</option>
            <option value="OPT">Optional</option>
        `;

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.className = 'btn btn-outline-danger btn-sm';
        removeBtn.textContent = 'Remove';
        removeBtn.addEventListener('click', () => wrapper.remove());

        wrapper.appendChild(select);
        wrapper.appendChild(typeSelect);
        wrapper.appendChild(removeBtn);

        return wrapper;
    }

    addDependencyBtn && addDependencyBtn.addEventListener('click', () => {
        depsContainer.appendChild(createDependencyRow());
    });
});
