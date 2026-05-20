// Citation popovers: hover to peek, click to pin.
// While pinned, the card stays open until you click outside it (so links inside are clickable).

const HIDE_DELAY = 200;

document.querySelectorAll('abbr.citation').forEach(button => {
  const title = button.getAttribute('data-papertitle');
  const url = button.getAttribute('data-url');
  const authors = button.getAttribute('data-authors');
  const conf = button.getAttribute('data-conf');
  const year = button.getAttribute('data-year');

  const content = `
    <div style="max-width: 260px;">
      <div><a href="${url}"><b>${title}</b></a></div>
      <div style="font-size: 0.85rem; color: #6b7280; margin: 4px 0;">${conf}, ${year}</div>
      <div style="font-size: 0.85rem; color: #6b7280;">${authors}</div>
    </div>
  `;

  const popover = new bootstrap.Popover(button, {
    trigger: 'manual',
    html: true,
    content,
    placement: 'bottom',
    container: 'body',
    animation: false,
  });

  let pinned = false;
  let hideTimer = null;
  const cancelHide = () => { if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; } };
  const scheduleHide = () => {
    cancelHide();
    if (pinned) return;
    hideTimer = setTimeout(() => popover.hide(), HIDE_DELAY);
  };

  // Once the popover is in the DOM, wire hover events on its tip too so the
  // user can move the mouse from the trigger into the card without it closing.
  button.addEventListener('shown.bs.popover', () => {
    const tip = popover.tip || document.querySelector('.popover');
    if (!tip) return;
    tip.addEventListener('mouseenter', cancelHide);
    tip.addEventListener('mouseleave', scheduleHide);
  });

  button.addEventListener('mouseenter', () => {
    cancelHide();
    popover.show();
  });
  button.addEventListener('mouseleave', scheduleHide);

  button.addEventListener('click', (e) => {
    e.preventDefault();
    e.stopPropagation();
    pinned = true;
    cancelHide();
    popover.show();
  });

  // Click outside to unpin / close.
  document.addEventListener('click', (e) => {
    if (!pinned) return;
    const tip = popover.tip || document.querySelector('.popover');
    const inTrigger = button.contains(e.target);
    const inTip = tip && tip.contains(e.target);
    if (!inTrigger && !inTip) {
      pinned = false;
      popover.hide();
    }
  });
});
