// GitHub-Flavored Markdown Parser for MarketWizardry.org
// Uses local marked.js (UMD) for full GFM support

(function() {
    'use strict';

    // Configure marked.js immediately (it's loaded synchronously before this script)
    var isConfigured = false;

    function setup() {
        if (isConfigured) return true;
        if (typeof marked === 'undefined') {
            console.error('markdown.js: marked is not loaded');
            return false;
        }

        try {
            marked.setOptions({
                gfm: true,
                breaks: false,
                pedantic: false
            });
            isConfigured = true;
        } catch (e) {
            console.error('markdown.js: failed to configure marked:', e);
            return false;
        }
        return true;
    }

    // Try to configure immediately
    setup();

    function escapeHtml(text) {
        var map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    function parseMarkdown(text) {
        if (!text) return '';

        // Ensure configured
        if (!isConfigured) setup();

        if (isConfigured && typeof marked !== 'undefined' && typeof marked.parse === 'function') {
            try {
                var html = marked.parse(text);

                // Post-process: add CSS classes to elements
                html = html.replace(/<h([1-6])>/g, '<h$1 class="md-h$1">');
                html = html.replace(/<p>/g, '<p class="md-p">');
                html = html.replace(/<strong>/g, '<strong class="md-bold">');
                html = html.replace(/<em>/g, '<em class="md-italic">');
                html = html.replace(/<a /g, '<a class="md-link" target="_blank" rel="noopener noreferrer" ');
                html = html.replace(/<code>/g, '<code class="md-code">');
                html = html.replace(/<pre>/g, '<pre class="md-codeblock">');
                html = html.replace(/<blockquote>/g, '<blockquote class="md-blockquote">');
                html = html.replace(/<hr>/g, '<hr class="md-hr">');
                html = html.replace(/<hr\/>/g, '<hr class="md-hr">');
                html = html.replace(/<table>/g, '<div class="md-table-wrapper"><table class="md-table">');
                html = html.replace(/<\/table>/g, '</table></div>');
                html = html.replace(/<th>/g, '<th class="md-th">');
                html = html.replace(/<th align="/g, '<th class="md-th" align="');
                html = html.replace(/<td>/g, '<td class="md-td">');
                html = html.replace(/<td align="/g, '<td class="md-td" align="');
                html = html.replace(/<ul>/g, '<ul class="md-ul">');
                html = html.replace(/<ol>/g, '<ol class="md-ol">');
                html = html.replace(/<li>/g, '<li class="md-li">');
                // Wrap images in clickable lightbox container with download link
                html = html.replace(/<img ([^>]*?)src="([^"]*?)"([^>]*?)alt="([^"]*?)"([^>]*?)>/g,
                    '<div class="md-img-container">' +
                    '<a href="$2" class="md-img-link" data-action="lightbox" title="Click to enlarge">' +
                    '<img class="md-img" loading="lazy" src="$2" alt="$4" $1$3$5>' +
                    '</a>' +
                    '<div class="md-img-actions">' +
                    '<a href="$2" download class="md-img-download" title="Download image">Download</a>' +
                    '<span class="md-img-caption">$4</span>' +
                    '</div></div>');
                // Fallback for img without alt before src
                html = html.replace(/<img ([^>]*?)src="([^"]*?)"([^>]*?)(?!.*class="md-img")>/g,
                    '<div class="md-img-container">' +
                    '<a href="$2" class="md-img-link" data-action="lightbox" title="Click to enlarge">' +
                    '<img class="md-img" loading="lazy" src="$2" $1$3>' +
                    '</a>' +
                    '<div class="md-img-actions">' +
                    '<a href="$2" download class="md-img-download" title="Download image">Download</a>' +
                    '</div></div>');

                // Handle mermaid code blocks
                html = html.replace(/<pre class="md-codeblock"><code class="md-code language-mermaid">([\s\S]*?)<\/code><\/pre>/g,
                    '<pre class="md-mermaid">$1</pre>');

                // Render mermaid after a short delay
                setTimeout(function() {
                    if (typeof mermaid !== 'undefined') {
                        var blocks = document.querySelectorAll('.md-mermaid');
                        blocks.forEach(function(block, i) {
                            var id = 'mermaid-' + Date.now() + '-' + i;
                            try {
                                mermaid.render(id, block.textContent).then(function(result) {
                                    block.outerHTML = '<div class="md-mermaid-rendered">' + result.svg + '</div>';
                                });
                            } catch (e) { /* mermaid optional */ }
                        });
                    }
                }, 200);

                return html;
            } catch (e) {
                console.error('markdown.js: marked.parse failed:', e);
            }
        }

        // Fallback: return escaped text in a pre
        return '<pre style="white-space:pre-wrap;color:#00ff00">' + escapeHtml(text) + '</pre>';
    }

    // Load mermaid from CDN (optional)
    var ms = document.createElement('script');
    ms.src = 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js';
    ms.onload = function() {
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({
                startOnLoad: false,
                theme: 'dark',
                themeVariables: {
                    primaryColor: '#003300', primaryTextColor: '#00ff00',
                    primaryBorderColor: '#00ff00', lineColor: '#00ff00',
                    secondaryColor: '#001a00', tertiaryColor: '#002200',
                    fontFamily: '"Courier New", monospace', fontSize: '14px',
                    textColor: '#00ff00', mainBkg: '#001a00', nodeBorder: '#00ff00'
                }
            });
        }
    };
    document.head.appendChild(ms);

    window.parseMarkdown = parseMarkdown;

    // Lightbox: click image to view full size in overlay
    document.addEventListener('click', function(e) {
        var link = e.target.closest('[data-action="lightbox"]');
        if (!link) return;
        e.preventDefault();
        var src = link.href;
        var alt = link.querySelector('img') ? link.querySelector('img').alt : '';

        // Create overlay
        var overlay = document.createElement('div');
        overlay.className = 'md-lightbox-overlay';
        overlay.innerHTML = '<div class="md-lightbox-content">' +
            '<img src="' + src + '" alt="' + alt + '" class="md-lightbox-img">' +
            '<div class="md-lightbox-bar">' +
            '<span class="md-lightbox-caption">' + alt + '</span>' +
            '<a href="' + src + '" download class="md-lightbox-download">Download</a>' +
            '<button class="md-lightbox-close">Close</button>' +
            '</div></div>';

        document.body.appendChild(overlay);
        document.body.style.overflow = 'hidden';

        // Close on click overlay, close button, or Escape
        function closeLightbox() {
            overlay.remove();
            document.body.style.overflow = '';
            document.removeEventListener('keydown', escHandler);
        }
        function escHandler(ev) { if (ev.key === 'Escape') closeLightbox(); }
        overlay.addEventListener('click', function(ev) {
            if (ev.target === overlay || ev.target.classList.contains('md-lightbox-close')) closeLightbox();
        });
        document.addEventListener('keydown', escHandler);
    });
})();
