document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("add-dependency-btn");
  const container = document.getElementById("dependencies-container");

  const tasks = JSON.parse(document.getElementById("tasks-data").textContent);

  let groupCounter = 0;

  addBtn.addEventListener("click", () => {
    groupCounter++;

    const groupDiv = document.createElement("div");
    groupDiv.className = "card mb-3 p-2";
    groupDiv.dataset.group = groupCounter;

    // Group type selector
    const groupType = document.createElement("select");
    groupType.name = `group_${groupCounter}_type`;
    groupType.className = "form-select mb-2";
    ["ALL", "ONE", "OPT"].forEach(type => {
      const opt = document.createElement("option");
      opt.value = type;
      opt.textContent = type;
      groupType.appendChild(opt);
    });

    // Container for prereqs
    const prereqContainer = document.createElement("div");
    prereqContainer.className = "mb-2";
    prereqContainer.dataset.group = groupCounter;

    // Add prerequisite button
    const addPrereqBtn = document.createElement("button");
    addPrereqBtn.type = "button";
    addPrereqBtn.className = "btn btn-sm btn-outline-secondary";
    addPrereqBtn.textContent = "+ Add prerequisite";

    addPrereqBtn.addEventListener("click", () => {
      const select = document.createElement("select");
      select.name = `group_${groupCounter}_prereq`;
      select.className = "form-select mb-1";
      tasks.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t.id;
        opt.textContent = t.name;
        select.appendChild(opt);
      });
      prereqContainer.appendChild(select);
    });

    groupDiv.appendChild(document.createTextNode("Dependency Group:"));
    groupDiv.appendChild(groupType);
    groupDiv.appendChild(prereqContainer);
    groupDiv.appendChild(addPrereqBtn);

    container.appendChild(groupDiv);
  });
});
