/**
 * Print Button for MkDocs
 * Adds a sticky print button to the top right of content pages
 */

document.addEventListener('DOMContentLoaded', function() {
  // Check if we're on a content page (not the homepage without article)
  const contentArea = document.querySelector('.md-content__inner');
  
  if (!contentArea) {
    return; // Exit if no content area found
  }
  
  // Create print button container
  const buttonContainer = document.createElement('div');
  buttonContainer.className = 'print-button-container';
  
  // Create print button
  const printButton = document.createElement('button');
  printButton.className = 'print-button';
  printButton.setAttribute('aria-label', 'Print this page');
  printButton.setAttribute('title', 'Print this page');
  
  // Add icon and text
  printButton.innerHTML = `
    <span class="print-icon">🖨</span>
    <span class="print-text">Print</span>
  `;
  
  // Add click event
  printButton.addEventListener('click', function() {
    window.print();
  });
  
  // Append button to container
  buttonContainer.appendChild(printButton);
  
  // Insert at the beginning of content area
  contentArea.insertBefore(buttonContainer, contentArea.firstChild);
  
  // Optional: Add keyboard shortcut (Ctrl+P is already handled by browser,
  // but we can add Ctrl+Shift+P as an alternative)
  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'P') {
      e.preventDefault();
      window.print();
    }
  });
});
