// Add new dependency row (with nesting support)
function createDependencyRow() {
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

    // 🔑 Container for child dependencies
    const childContainer = document.createElement('div');
    childContainer.classList.add('child-dependencies');

    // 🔑 Button to add sub-dependencies
    const addChildBtn = document.createElement('button');
    addChildBtn.type = 'button';
    addChildBtn.textContent = '+ Add Sub-Dependency';
    addChildBtn.addEventListener('click', () => {
        const childRow = createDependencyRow();
        childRow.style.marginLeft = "20px"; // indent visually
        childContainer.appendChild(childRow);
    });

    div.appendChild(select);
    div.appendChild(typeSelect);
    div.appendChild(removeBtn);
    div.appendChild(addChildBtn);   // 🔑 add button for nesting
    div.appendChild(childContainer);

    return div;
}

// Hook top-level add button
document.getElementById('add-dependency-btn').addEventListener('click', () => {
    depsContainer.appendChild(createDependencyRow());
});
