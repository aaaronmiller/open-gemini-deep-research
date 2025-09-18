// content.js - Enhanced with better error handling and signal confirmation
console.log('AI Chat Capture content script loaded');

function getProviderData(url) {
  const map = [
    {
      rx: /chat\.openai\.com/,
      service: "openai",
      selectors: [
        '[data-testid="conversation-turn-list"]',
        '.main .flex.flex-col.items-center .flex.flex-col.gap-2',
        '.chat-container',
        '[class^="react-scroll-to-bottom--"]'
      ]
    },
    {
      rx: /perplexity\.ai/,
      service: "perplexity",
      selectors: [
        '[data-testid="Conversation"]',
        '.main-chat-container'
      ]
    },
    {
      rx: /claude\.ai/,
      service: "claude",
      selectors: [
        'main[data-testid="chat-interface"]',
        '[class^="ThreadView_messageList__"]',
        '.conversation-main'
      ]
    },
    {
      rx: /gemini\.google\.com/,
      service: "gemini",
      selectors: [
        '[data-testid="conversation-history"]',
        '#conversation-container',
        '.chatbot-container',
        '[id^="conversation-container"]'
      ]
    },
    {
      rx: /grok\.x\.ai/,
      service: "grok",
      selectors: [
        '[data-testid="grok-chat"]',
        '.conversation-thread',
        'main[role="main"]'
      ]
    },
    {
      rx: /kimi/,
      service: "kimi",
      selectors: [
        'main[data-kimi-conversation="true"]',
        '.kimi-chat-container',
        '.conversation-page'
      ]
    },
    {
      rx: /deepseek/,
      service: "deepseek",
      selectors: [
        '.conversation-container',
        '.deepseek-conversation',
        '.chat-main'
      ]
    },
    {
      rx: /ernie/,
      service: "ernie",
      selectors: [
        'main.conversation',
        '.ernie-chat-main',
        '[data-testid="ernie-conversation"]'
      ]
    }
  ];

  for (const entry of map) {
    if (entry.rx.test(url)) return entry;
  }

  return {
    service: location.hostname.split('.')[0] || 'unknown',
    selectors: ['.main-chat-container', 'main', 'body']
  };
}

function htmlToMarkdown(html) {
  let md = html
    .replace(/<pre[^>]*>([\s\S]*?)<\/pre>/g, (match, code) => {
      // Clean up code blocks
      const cleanCode = code
        .replace(/<[^>]+>/g, '') // Remove HTML tags
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&amp;/g, '&');
      return '\n```\n' + cleanCode + '\n```\n';
    })
    .replace(/<code[^>]*>(.*?)<\/code>/g, '`$1`')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<li[^>]*>(.*?)<\/li>/gs, '- $1\n')
    .replace(/<\/ul>/g, '\n')
    .replace(/<\/ol>/g, '\n')
    .replace(/<b[^>]*>(.*?)<\/b>/gs, '**$1**')
    .replace(/<strong[^>]*>(.*?)<\/strong>/gs, '**$1**')
    .replace(/<em[^>]*>(.*?)<\/em>/gs, '*$1*')
    .replace(/<i[^>]*>(.*?)<\/i>/gs, '*$1*')
    .replace(/<h[1-6][^>]*>(.*?)<\/h[1-6]>/gs, '\n## $1\n')
    .replace(/<p[^>]*>/g, '\n')
    .replace(/<\/p>/g, '\n')
    .replace(/<div[^>]*>/g, '\n')
    .replace(/<\/div>/g, '\n')
    .replace(/<[^>]+>/g, '') // Remove remaining HTML tags
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/\n{3,}/g, '\n\n')
    .trim();

  return md;
}

async function extractAndSave() {
  try {
    console.log('Starting AI chat extraction...');

    const url = window.location.href;
    const providerData = getProviderData(url);
    let container = null;
    let html = '';
    let markdown = '';
    let usedSelector = '';

    // Try each selector until we find content
    for (const sel of providerData.selectors) {
      container = document.querySelector(sel);
      if (container && container.innerText && container.innerText.length > 50) {
        html = container.outerHTML;
        markdown = htmlToMarkdown(html);
        usedSelector = sel;
        console.log(`Found content using selector: ${sel}`);
        break;
      }
    }

    // Fallback to body if nothing found
    if (!container || markdown.length < 50) {
      container = document.body;
      html = container.outerHTML;
      markdown = htmlToMarkdown(html);
      usedSelector = "body (fallback)";
      console.log('Using body fallback');
    }

    const dt = new Date();
    const timeStr = dt.toISOString().replace(/:/g, '-').replace(/\..+/, '');
    const service = providerData.service;
    const fname = `ai-session-${service}-${timeStr}.md`;

    // Enhanced YAML frontmatter
    const yaml = `---
date: ${dt.toISOString()}
provider: ${service}
session_url: ${url}
chat_selector: "${usedSelector}"
extraction_time: ${dt.toISOString()}
word_count: ${markdown.split(/\s+/).length}
char_count: ${markdown.length}
---

`;

    // Compose final document
    const result = [
      yaml,
      markdown.trim(),
      '\n\n---\n\n',
      '## Extraction Metadata\n\n',
      `- **Provider**: ${service}\n`,
      `- **URL**: ${url}\n`,
      `- **Selector Used**: \`${usedSelector}\`\n`,
      `- **Captured**: ${dt.toLocaleString()}\n`,
      `- **Content Length**: ${markdown.length} characters, ${markdown.split(/\s+/).length} words\n`
    ].join('');

    // Create and download
    const blob = new Blob([result], { type: 'text/markdown' });
    const urlObj = URL.createObjectURL(blob);

    console.log(`Sending download request for: ${fname}`);
    chrome.runtime.sendMessage({ fname, urlObj });

    // Show user feedback
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed; top: 20px; right: 20px; z-index: 10000;
      background: #4CAF50; color: white; padding: 15px; border-radius: 5px;
      font-family: system-ui; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    `;
    notification.textContent = `✓ AI chat captured: ${fname}`;
    document.body.appendChild(notification);

    setTimeout(() => notification.remove(), 3000);

  } catch (error) {
    console.error('Extraction failed:', error);

    // Show error notification
    const errorNotif = document.createElement('div');
    errorNotif.style.cssText = `
      position: fixed; top: 20px; right: 20px; z-index: 10000;
      background: #f44336; color: white; padding: 15px; border-radius: 5px;
      font-family: system-ui; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    `;
    errorNotif.textContent = `✗ Extraction failed: ${error.message}`;
    document.body.appendChild(errorNotif);

    setTimeout(() => errorNotif.remove(), 5000);
  }
}

// Message listener
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  console.log('Content script received message:', msg);

  if (msg === 'extract_ai_chat') {
    extractAndSave();
    sendResponse({ status: 'started' });
  }

  return true; // Keep message channel open for async response
});

// Signal that content script is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('AI Chat Capture ready');
  });
} else {
  console.log('AI Chat Capture ready');
}
