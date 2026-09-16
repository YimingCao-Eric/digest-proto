function formatPublished(published) {
  const date = new Date(published);
  const minutes = (Date.now() - date.getTime()) / 60000;
  if (minutes < 60) {
    return Math.floor(minutes) + "m ago";
  }
  if (minutes < 24 * 60) {
    return Math.floor(minutes / 60) + "h ago";
  }
  return date.toLocaleDateString();
}

function renderItem(item) {
  const row = document.createElement("li");

  const link = document.createElement("a");
  link.href = item.url;
  link.textContent = item.title;
  row.appendChild(link);

  if (item.source === "GitHub Trending") {
    const meta = document.createElement("div");
    meta.textContent = item.extra.stars_today + " stars today · " + item.extra.language;
    row.appendChild(meta);

    const description = document.createElement("p");
    description.textContent = item.extra.description;
    row.appendChild(description);
  } else {
    row.appendChild(document.createTextNode(" "));

    const discussion = document.createElement("a");
    discussion.href = item.extra.comments;
    discussion.textContent = "discussion";
    row.appendChild(discussion);

    const published = document.createElement("span");
    published.textContent = " " + formatPublished(item.published_at);
    row.appendChild(published);
  }

  return row;
}

async function render() {
  const response = await fetch("/api/items");
  const data = await response.json();

  document.getElementById("fetched-at").textContent = new Date(data.fetched_at).toLocaleDateString();

  const container = document.getElementById("items");
  container.replaceChildren();

  const groups = new Map();
  for (const item of data.items) {
    if (!groups.has(item.source)) {
      groups.set(item.source, []);
    }
    groups.get(item.source).push(item);
  }

  for (const [source, items] of groups) {
    const group = document.createElement("li");

    const heading = document.createElement("h2");
    heading.textContent = source;
    group.appendChild(heading);

    const list = document.createElement("ul");
    for (const item of items) {
      list.appendChild(renderItem(item));
    }
    group.appendChild(list);

    container.appendChild(group);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("refresh").addEventListener("click", render);
  render();
});
