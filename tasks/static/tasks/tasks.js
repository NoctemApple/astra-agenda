document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('dependencies-container');

    function createDependencyRow() {
        const div = document.createElement('div');
        div.classList.add('dependency-row', 'mb-2');

        // Task select
        const select = document.createElement('select');
        select.name = 'dependencies';
        select.classList.add('form-select', 'me-2');
        document.querySelectorAll('.task').forEach(t => {
            const option = document.createElement('option');
            option.value = t.id.replace('task-', '');
            option.textContent = t.textContent;
            select.appendChild(option);
        });

        // Type select
        const typeSelect = document.createElement('select');
        typeSelect.name = 'dependency_types';
        typeSelect.classList.add('form-select', 'me-2');
        typeSelect.innerHTML = `
            <option value="ALL">Required (All)</option>
            <option value="ONE">Required (One-of)</option>
            <option value="OPT">Optional</option>
        `;

        // Remove button
        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.classList.add('btn', 'btn-danger');
        removeBtn.textContent = 'x';
        removeBtn.addEventListener('click', () => div.remove());

        div.appendChild(select);
        div.appendChild(typeSelect);
        div.appendChild(removeBtn);
        container.appendChild(div);
    }

    document.getElementById('add-dependency-btn').addEventListener('click', createDependencyRow);
});
