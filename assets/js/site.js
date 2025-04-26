const citations = document.querySelectorAll('.citation');
const popovers = new Map();  // Track popovers per button
const clickedState = new Map();  // Track clicked state per button

citations.forEach(button => {
  const title = button.getAttribute('data-papertitle');
  const url = button.getAttribute('data-url');
  const authors = button.getAttribute('data-authors');
  const conf = button.getAttribute('data-conf');
  const year = button.getAttribute('data-year');
  content = `
    <div style="max-width: 250px;">
      <div><a href="${url}"><b>${title}</b></a></div>
      <div style="font-size: 0.875rem; color: #6c757d; margin-bottom: 0.25rem;">
        ${conf}, ${year}
      </div>
      <div style="font-size: 0.8rem; color: #6c757d;">
        ${authors}
      </div>
    </div>
  `

  const popover = new bootstrap.Popover(button, {
    trigger: 'manual',
    html: true,
    content: content,
    placement: 'bottom',
    animation: false // disable fade in
  });
  popovers.set(button, popover);
  clickedState.set(button, false);

  button.addEventListener('mouseenter', () => {
    if (!clickedState.get(button)) {
      popover.show();
    }
  });

  button.addEventListener('mouseleave', () => {
    if (!clickedState.get(button)) {
      popover.hide();
    }
  });

  button.addEventListener('click', (e) => {
    e.stopPropagation();  // Prevent bubbling up
    clickedState.set(button, true);
    popover.show();
  });
});

// Click outside to close any open popover
document.addEventListener('click', (e) => {
  citations.forEach(button => {
    const popoverContent = document.querySelector('.popover'); // Bootstrap adds this when we use bootstrap.Popover
    if (clickedState.get(button) && !button.contains(e.target) && !(popoverContent && popoverContent.contains(e.target))) {
      clickedState.set(button, false);
      popovers.get(button).hide();
    }
  });
});