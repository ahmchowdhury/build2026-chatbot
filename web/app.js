// Build 2026 Chatbot UI
const $thread = document.getElementById('thread');
const $form = document.getElementById('composer');
const $input = document.getElementById('input');
const $chips = document.getElementById('chips');
const $health = document.getElementById('health');

const SUGGESTIONS = [
  { label: 'Prompt caching', q: 'What did Naomi say about prompt caching?' },
  { label: 'AI Foundry', q: 'Summarize all AI Foundry sessions' },
  { label: 'Windows', q: 'Summarize Windows sessions' },
  { label: 'AI Infrastructure', q: 'Summarize AI Infrastructure sessions' },
  { label: 'Models', q: 'Summarize Models sessions' },
  { label: 'Agents', q: 'Summarize Agents sessions' },
  { label: 'Microsoft IQ', q: 'Tell me about Microsoft IQ family' },
  { label: 'Agent 365', q: 'What is Agent 365?' },
  { label: 'Topics', q: 'topics' },
];

function renderChips() {
  $chips.innerHTML = '';
  SUGGESTIONS.forEach(s => {
    const c = document.createElement('button');
    c.className = 'chip';
    c.textContent = s.label;
    c.onclick = () => { $input.value = s.q; $input.focus(); $form.requestSubmit(); };
    $chips.appendChild(c);
  });
}

function autosize() {
  $input.style.height = 'auto';
  $input.style.height = Math.min($input.scrollHeight, 200) + 'px';
}

function appendUser(text) {
  const wrap = document.createElement('div');
  wrap.className = 'flex justify-end';
  const b = document.createElement('div');
  b.className = 'bubble-user';
  b.textContent = text;
  wrap.appendChild(b);
  $thread.appendChild(wrap);
  scrollDown();
}

function appendBot(markdown, kind) {
  const wrap = document.createElement('div');
  wrap.className = 'flex justify-start';
  const b = document.createElement('div');
  b.className = 'bubble-bot md';
  const html = DOMPurify.sanitize(marked.parse(markdown, { breaks: true }));
  b.innerHTML = html;
  wrap.appendChild(b);
  $thread.appendChild(wrap);
  // open all links in new tab
  b.querySelectorAll('a').forEach(a => { a.target = '_blank'; a.rel = 'noopener'; });
  scrollDown();
}

function appendTyping() {
  const wrap = document.createElement('div');
  wrap.className = 'flex justify-start';
  wrap.id = 'typing';
  const b = document.createElement('div');
  b.className = 'bubble-bot';
  b.innerHTML = '<span class="dot"></span><span class="dot"></span><span class="dot"></span>';
  wrap.appendChild(b);
  $thread.appendChild(wrap);
  scrollDown();
}

function removeTyping() {
  const t = document.getElementById('typing');
  if (t) t.remove();
}

function scrollDown() {
  $thread.scrollTo({ top: $thread.scrollHeight, behavior: 'smooth' });
}

async function ask(message) {
  appendUser(message);
  appendTyping();
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    removeTyping();
    if (!res.ok) {
      appendBot('⚠️ Server error: ' + res.status, 'error');
      return;
    }
    const data = await res.json();
    appendBot(data.answer, data.kind);
  } catch (e) {
    removeTyping();
    appendBot('⚠️ Network error: ' + e.message, 'error');
  }
}

$form.addEventListener('submit', e => {
  e.preventDefault();
  const text = $input.value.trim();
  if (!text) return;
  $input.value = '';
  autosize();
  ask(text);
});

$input.addEventListener('input', autosize);
$input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    $form.requestSubmit();
  }
});

(async function init() {
  renderChips();
  try {
    const r = await fetch('/api/health');
    const d = await r.json();
    $health.textContent = `${d.sessions} sessions indexed · ${d.with_ai_summary} with AI summary · live`;
  } catch {
    $health.textContent = 'health check failed';
  }
  appendBot(
    "**Welcome.** I'm grounded in **460 Microsoft Build 2026 sessions** " +
    "(170 with AI summaries, 185 with downloadable transcripts).\n\n" +
    "Try a chip above, ask a focused question (*“what is explicit prompt caching?”*), " +
    "ask for a topic summary (*“summarize AI Foundry sessions”*), or paste a session code (*BRK230*).\n\n" +
    "Type **`topics`** to see everything I cover.",
    'welcome'
  );
})();
