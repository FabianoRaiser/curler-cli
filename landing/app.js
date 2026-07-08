const DEMO = {
  parsed: {
    shell: "curler example.com",
    html: `
      <div class="page-block">
        <p class="block h1"># Example Domain</p>
        <p class="block">This domain is for use in documentation examples</p>
        <p class="block">without needing permission. Avoid use in operations.</p>
        <p class="block"><span class="link">Learn more [1]</span></p>
        <p class="block dim">(1 link — use links)</p>
      </div>`,
  },
  raw: {
    shell: "curler --raw example.com",
    html: `
      <div class="page-block code-block">
        <p class="block code-line">&lt;!doctype html&gt;</p>
        <p class="block code-line">&lt;html&gt;</p>
        <p class="block code-line">&lt;head&gt;&lt;title&gt;Example Domain&lt;/title&gt;&lt;/head&gt;</p>
        <p class="block code-line">&lt;body&gt;</p>
        <p class="block code-line">&lt;div&gt;</p>
        <p class="block code-line">&lt;h1&gt;Example Domain&lt;/h1&gt;</p>
        <p class="block code-line">&lt;p&gt;This domain is for use in illustrative examples in documents.&lt;/p&gt;</p>
        <p class="block code-line">&lt;p&gt;&lt;a href="https://www.iana.org/domains/example"&gt;More information...&lt;/a&gt;&lt;/p&gt;</p>
        <p class="block code-line">&lt;/div&gt;</p>
        <p class="block code-line">&lt;/body&gt;</p>
        <p class="block code-line">&lt;/html&gt;</p>
      </div>`,
  },
  pretty: {
    shell: "curler --pretty example.com",
    html: `
      <div class="page-block code-block">
        <p class="block code-line">&lt;!doctype html&gt;</p>
        <p class="block code-line">&lt;html&gt;</p>
        <p class="block code-line">  &lt;head&gt;</p>
        <p class="block code-line">    &lt;title&gt;Example Domain&lt;/title&gt;</p>
        <p class="block code-line">  &lt;/head&gt;</p>
        <p class="block code-line">  &lt;body&gt;</p>
        <p class="block code-line">    &lt;div&gt;</p>
        <p class="block code-line">      &lt;h1&gt;Example Domain&lt;/h1&gt;</p>
        <p class="block code-line">      &lt;p&gt;</p>
        <p class="block code-line">        This domain is for use in illustrative examples in documents.</p>
        <p class="block code-line">      &lt;/p&gt;</p>
        <p class="block code-line">      &lt;p&gt;</p>
        <p class="block code-line">        &lt;a href="https://www.iana.org/domains/example"&gt;More information...&lt;/a&gt;</p>
        <p class="block code-line">      &lt;/p&gt;</p>
        <p class="block code-line">    &lt;/div&gt;</p>
        <p class="block code-line">  &lt;/body&gt;</p>
        <p class="block code-line">&lt;/html&gt;</p>
      </div>`,
  },
  headers: {
    shell: "curler --headers example.com",
    html: `
      <div class="page-block">
        <p class="block kv"><span class="kv-key">content-type  </span><span class="kv-val">text/html; charset=UTF-8</span></p>
        <p class="block kv"><span class="kv-key">content-length</span><span class="kv-val">1256</span></p>
        <p class="block kv"><span class="kv-key">server        </span><span class="kv-val">ECS (nyb/1D2A)</span></p>
        <p class="block kv"><span class="kv-key">date          </span><span class="kv-val">Wed, 08 Jul 2026 12:00:00 GMT</span></p>
        <p class="block kv"><span class="kv-key">cache-control </span><span class="kv-val">max-age=86400</span></p>
      </div>`,
  },
};

function renderDemo(tabName) {
  const config = DEMO[tabName];
  const panel = document.getElementById("demo-output");
  panel.innerHTML = `
    <p class="block shell-cmd"><span class="prompt">$</span> ${config.shell}</p>
    ${config.html}`;
}

function initTabs() {
  const tabs = document.querySelectorAll(".tab");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");
      renderDemo(tab.dataset.tab);
    });
  });

  renderDemo("parsed");
}

function initCopyButtons() {
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        btn.textContent = "copied!";
        btn.classList.add("copied");
        setTimeout(() => {
          btn.textContent = "copy";
          btn.classList.remove("copied");
        }, 1500);
      } catch {
        btn.textContent = "failed";
        setTimeout(() => {
          btn.textContent = "copy";
        }, 1500);
      }
    });
  });
}

initTabs();
initCopyButtons();
