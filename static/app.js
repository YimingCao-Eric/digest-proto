async function render() {
  const response = await fetch("/api/items");
  const data = await response.json();

  document.getElementById("fetched-at").textContent = "Fetched at " + data.fetched_at;

  const list = document.getElementById("items");
  list.replaceChildren();

  for (const item of data.items) {
    const row = document.createElement("li");

    const link = document.createElement("a");
    link.href = item.url;
    link.textContent = item.title;
    row.appendChild(link);

    const meta = document.createElement("div");
    meta.textContent = item.extra.stars_today + " stars today · " + item.extra.language;
    row.appendChild(meta);

    const description = document.createElement("p");
    description.textContent = item.extra.description;
    row.appendChild(description);

    list.appendChild(row);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("refresh").addEventListener("click", render);
  render();
});
