(function () {
  const form = document.getElementById("task-form");
  const depsContainer = document.getElementById("dependencies-container");
  const hiddenTree = document.getElementById("dependency_tree");
  const addBtn = document.getElementById("add-dependency-btn");

  // Read safe JSON injected by template
  let existingTasks = [];
  try {
    existingTasks = JSON.parse(document.getElementById("existing-tasks").textContent || "[]");
  } catch (_) {
    existingTasks = [];
  }

  function taskSelect() {
    const sel = document.createElement("select");
    sel.className = "form-select form-select-sm me-2 dep-task";
    // no name attribute -> we’ll serialize manually
    existingTasks.forEach(t => {
      const opt = document.createElement("option");
      opt.value = String(t.id);
      opt.textContent = t.name;
      sel.appendChild(opt);
    });
    return sel;
  }

  function typeSelect() {
    const sel = document.createElement("select");
    sel.className = "form-select form-select-sm me-2 dep-type";
    [["ALL","Required (All)"],["ONE","Required (One-of)"],["OPT","Optional"]]
      .forEach(([val,label]) => {
        const opt = document.createElement("option");
        opt.value = val;
        opt.textContent = label;
        sel.appendChild(opt);
      });
    return sel;
  }

  function createDependencyRow(indentPx = 0) {
    const row = document.createElement("div");
    row.className = "d-flex align-items-start mb-2 dependency-row";
    row.style.marginLeft = indentPx + "px";

    const left = document.createElement("div");
    left.className = "d-flex align-items-center flex-wrap gap-2";

    const selTask = taskSelect();
    const selType = typeSelect();

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "btn btn-sm btn-outline-danger";
    removeBtn.textContent = "Remove";
    removeBtn.addEventListener("click", () => row.remove());

    const addChildBtn = document.createElement("button");
    addChildBtn.type = "button";
    addChildBtn.className = "btn btn-sm btn-outline-secondary";
    addChildBtn.textContent = "+ Add Sub-Dependency";

    const childWrap = document.createElement("div");
    childWrap.className = "child-dependencies w-100 mt-2";

    addChildBtn.addEventListener("click", () => {
      childWrap.appendChild(createDependencyRow(indentPx + 20));
    });

    left.appendChild(selTask);
    left.appendChild(selType);
    left.appendChild(addChildBtn);
    left.appendChild(removeBtn);

    row.appendChild(left);
    row.appendChild(childWrap);
    return row;
  }

  function addTopLevelDependency() {
    depsContainer.appendChild(createDependencyRow(0));
  }

  // Recursively serialize the UI into a JSON tree
  function serializeRows(container) {
    const nodes = [];
    container.querySelectorAll(":scope > .dependency-row").forEach(row => {
      const taskSel = row.querySelector(".dep-task");
      const typeSel = row.querySelector(".dep-type");
      const childrenContainer = row.querySelector(":scope > .child-dependencies");

      const node = {
        task_id: taskSel?.value || null,
        group_type: typeSel?.value || "ALL",
        children: childrenContainer ? serializeRows(childrenContainer) : []
      };

      if (node.task_id) nodes.push(node);
    });
    return nodes;
  }

  addBtn.addEventListener("click", addTopLevelDependency);

  form.addEventListener("submit", () => {
    const tree = serializeRows(depsContainer);
    hiddenTree.value = JSON.stringify(tree);
  });
})();
