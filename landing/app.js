const PAGES = {
  example: {
    title: "Example Domain",
    lines: [
      "This domain is for use in documentation examples",
      "without needing permission. Avoid use in operations.",
    ],
    links: [{ n: 1, text: "Learn more", target: "iana" }],
    footer: "(1 link — use links)",
  },
  iana: {
    title: "Example Domains",
    lines: [
      "As described in RFC 2606 and RFC 6761, a number of domains",
      "such as example.com and example.org are maintained for",
      "documentation purposes.",
    ],
    links: [{ n: 1, text: "RFC 2606", target: "example" }],
    footer: "(1 link — use links)",
  },
  spa: {
    spaWarning: true,
    title: "My React App",
    lines: ['<div id="root"></div>'],
    links: [],
    footer: "(0 links)",
  },
};

const INSTALL_CMD = "pip install curler-paperback";
const SPA_WARNING =
  "This page looks like a JavaScript SPA with little server-rendered content. " +
  "Try Stagecraft or Blockbuster for full browser rendering.";

let currentPage = "example";
const history = ["example"];

const typedEl = document.getElementById("typed-command");
const cursorEl = document.getElementById("cursor");
const sessionLog = document.getElementById("session-log");
const replSection = document.getElementById("repl-section");
const btnGo1 = document.getElementById("btn-go-1");
const btnBack = document.getElementById("btn-back");
const copyBtn = document.getElementById("copy-btn");
const spaDemoBtn = document.getElementById("spa-demo");

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}

function appendCommand(command) {
  const line = el("p", "block");
  line.innerHTML = `<span class="prompt">curler&gt;</span> ${command}`;
  sessionLog.appendChild(line);
}

function appendOutput(text, className) {
  const line = el("p", "block " + (className || ""));
  line.textContent = text;
  sessionLog.appendChild(line);
}

function appendPage(pageId) {
  const page = PAGES[pageId];
  const block = el("div", "page-block");

  if (page.spaWarning) {
    block.appendChild(el("p", "block warn", SPA_WARNING));
    block.appendChild(el("p", "block", ""));
  }

  block.appendChild(el("p", "block h1", "# " + page.title));

  for (const line of page.lines) {
    block.appendChild(el("p", "block", line));
  }

  for (const link of page.links) {
    const p = el("p", "block");
    const span = el("span", "link");
    span.textContent = `${link.text} [${link.n}]`;
    span.addEventListener("click", () => {
      navigateTo(link.target, { command: `go ${link.n}` });
    });
    p.appendChild(span);
    block.appendChild(p);
  }

  if (page.footer) {
    block.appendChild(el("p", "block dim", page.footer));
  }

  sessionLog.appendChild(block);
  updateReplButtons();
}

function navigateTo(pageId, { command = null } = {}) {
  if (command) appendCommand(command);
  if (pageId === currentPage) return;

  history.push(pageId);
  currentPage = pageId;
  appendPage(pageId);
}

function updateReplButtons() {
  const page = PAGES[currentPage];
  btnGo1.disabled = !page.links.length;
  btnBack.disabled = history.length <= 1;
}

function typeText(text, speed = 65) {
  return new Promise((resolve) => {
    let i = 0;
    typedEl.textContent = "";
    const tick = () => {
      if (i < text.length) {
        typedEl.textContent += text[i++];
        setTimeout(tick, speed);
      } else {
        resolve();
      }
    };
    tick();
  });
}

function runReplCommand(cmd) {
  replSection.classList.remove("hidden");
  appendCommand(cmd);

  if (cmd === "links") {
    const page = PAGES[currentPage];
    if (!page.links.length) {
      appendOutput("(no links)", "dim");
      return;
    }
    for (const link of page.links) {
      appendOutput(`[${link.n}] ${link.text} — (${link.target})`, "link");
    }
    btnGo1.disabled = false;
    return;
  }

  if (cmd === "go 1") {
    const target = PAGES[currentPage].links[0]?.target;
    if (target) navigateTo(target);
    return;
  }

  if (cmd === "back") {
    if (history.length <= 1) return;
    history.pop();
    currentPage = history[history.length - 1];
    appendPage(currentPage);
    updateReplButtons();
  }
}

document.querySelectorAll("[data-cmd]").forEach((btn) => {
  btn.addEventListener("click", () => runReplCommand(btn.dataset.cmd));
});

copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(INSTALL_CMD);
    copyBtn.textContent = "copied!";
    copyBtn.classList.add("copied");
    setTimeout(() => {
      copyBtn.textContent = "copy";
      copyBtn.classList.remove("copied");
    }, 1500);
  } catch {
    copyBtn.textContent = "failed";
    setTimeout(() => {
      copyBtn.textContent = "copy";
    }, 1500);
  }
});

spaDemoBtn.addEventListener("click", () => {
  history.length = 0;
  history.push("spa");
  currentPage = "spa";
  typedEl.textContent = "spa-demo.app";
  cursorEl.classList.add("hidden");
  replSection.classList.remove("hidden");
  appendCommand("spa-demo.app");
  appendPage("spa");
});

async function boot() {
  await typeText("example.com");
  cursorEl.classList.add("hidden");
  sessionLog.classList.remove("hidden");
  replSection.classList.remove("hidden");
  appendPage("example");
}

boot();
