document.addEventListener("DOMContentLoaded", function () {
  const addDependencyBtn = document.getElementById("add-dependency-btn");
  const container = document.getElementById("dependencies-container");

  addDependencyBtn.addEventListener("click", function () {
    const wrapper = document.createElement("div");
    wrapper.classList.add("dependency-field");

    wrapper.innerHTML = `
      <select name="dependency_group_type[]">
        <option value="ALL">Required (All)</option>
        <option value="ONE">Required (One-of)</option>
        <option value="OPT">Optional</option>
      </select>
      <input type="text" name="dependency_task[]" placeholder="Dependency Task Name" />
      <button type="button" class="remove-dependency-btn">Remove</button>
    `;

    container.appendChild(wrapper);

    // Handle remove
    wrapper.querySelector(".remove-dependency-btn").addEventListener("click", () => {
      wrapper.remove();
    });
  });
});
