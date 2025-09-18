// background.js - Fixed version with proper content script handling
chrome.action.onClicked.addListener(async (tab) => {
  try {
    // First, ensure content script is injected
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ['content.js']
    });

    // Small delay to ensure script is fully loaded
    setTimeout(() => {
      chrome.tabs.sendMessage(tab.id, 'extract_ai_chat', (response) => {
        if (chrome.runtime.lastError) {
          console.error('Message failed:', chrome.runtime.lastError.message);
          // Fallback: try direct script execution
          chrome.scripting.executeScript({
            target: { tabId: tab.id },
            function: () => {
              if (typeof extractAndSave === 'function') {
                extractAndSave();
              }
            }
          });
        }
      });
    }, 100);

  } catch (error) {
    console.error('Failed to inject content script:', error);
  }
});

chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
  if (req.fname && req.urlObj) {
    // Direct download to Downloads folder - our background mover will handle it
    chrome.downloads.download({
      url: req.urlObj,
      filename: req.fname,
      saveAs: false, // No dialog - straight to Downloads
      conflictAction: 'uniquify'
    }, (downloadId) => {
      if (chrome.runtime.lastError) {
        console.error('Download failed:', chrome.runtime.lastError.message);
      } else {
        console.log('Download completed - background mover should handle it');
      }
    });
  }
});
