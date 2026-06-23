/* Planet Explorer – frontend chat logic */
(function () {
  "use strict";

  const chatWindow = document.getElementById("chat-window");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");
  const sendBtn = form.querySelector(".input-bar__send");

  /** Append a message bubble to the chat window. */
  function appendMessage(text, role) {
    const wrapper = document.createElement("div");
    wrapper.className = "message message--" + role;

    const avatar = document.createElement("span");
    avatar.className = "message__avatar";
    avatar.textContent = role === "user" ? "👤" : "🤖";

    const bubble = document.createElement("div");
    bubble.className = "message__bubble";
    // Render **bold** markdown fragments
    bubble.innerHTML = formatText(text);

    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatWindow.appendChild(wrapper);
    scrollToBottom();
    return wrapper;
  }

  /** Show animated typing indicator and return the element. */
  function showTyping() {
    const wrapper = document.createElement("div");
    wrapper.className = "message message--bot";
    wrapper.id = "typing-indicator";

    const avatar = document.createElement("span");
    avatar.className = "message__avatar";
    avatar.textContent = "🤖";

    const bubble = document.createElement("div");
    bubble.className = "message__bubble";
    bubble.innerHTML =
      '<span class="typing-dot"></span>' +
      '<span class="typing-dot"></span>' +
      '<span class="typing-dot"></span>';

    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatWindow.appendChild(wrapper);
    scrollToBottom();
    return wrapper;
  }

  function removeTyping() {
    const el = document.getElementById("typing-indicator");
    if (el) el.remove();
  }

  function scrollToBottom() {
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

  /**
   * Convert a subset of markdown to HTML:
   *   **text** → <strong>text</strong>
   *   newlines  → <br>
   *   • bullet  → left as-is (pre-wrap handles it)
   */
  function formatText(text) {
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
      .replace(/\n/g, "<br>");
  }

  /** Send the user's message to the server and display the reply. */
  async function sendMessage(message) {
    sendBtn.disabled = true;
    appendMessage(message, "user");

    const typingEl = showTyping();

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      removeTyping();

      if (!response.ok) {
        appendMessage("Sorry, something went wrong. Please try again.", "bot");
        return;
      }

      const data = await response.json();
      appendMessage(data.reply || "No response received.", "bot");
    } catch (_err) {
      removeTyping();
      appendMessage(
        "Could not connect to the server. Please check your connection.",
        "bot"
      );
    } finally {
      sendBtn.disabled = false;
      input.focus();
    }
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    input.value = "";
    sendMessage(message);
  });
})();
