  const btn = document.getElementById("rnd_but");
  const dropdown = document.getElementById("rnd_but_drop");

  btn.addEventListener("click", () => {
    dropdown.hidden = !dropdown.hidden;
  });
    dropdown.addEventListener("click", () => {
    dropdown.hidden = true;
  });
    document.addEventListener("click", (e) => {
    if (!btn.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.hidden = true;
    }
  });