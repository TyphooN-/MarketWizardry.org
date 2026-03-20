// GitHub-Flavored Markdown Parser for MarketWizardry.org
// Uses local marked.js for full GFM support + optional mermaid.js CDN for diagrams

(function() {
    'use strict';

    // Load mermaid.js from CDN (optional — diagrams are a nice-to-have)
    const mermaidScript = document.createElement('script');
    mermaidScript.src = 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js';
    mermaidScript.onload = function() {
        if (typeof mermaid !== 'undefined') {
            mermaid.initialize({
                startOnLoad: false,
                theme: 'dark',
                themeVariables: {
                    primaryColor: '#003300',
                    primaryTextColor: '#00ff00',
                    primaryBorderColor: '#00ff00',
                    lineColor: '#00ff00',
                    secondaryColor: '#001a00',
                    tertiaryColor: '#002200',
                    fontFamily: '"Courier New", monospace',
                    fontSize: '14px',
                    textColor: '#00ff00',
                    mainBkg: '#001a00',
                    nodeBorder: '#00ff00',
                    clusterBkg: '#002200',
                    clusterBorder: '#00ff00',
                    edgeLabelBackground: '#000000',
                    nodeTextColor: '#00ff00'
                }
            });
        }
    };
    document.head.appendChild(mermaidScript);

    function escapeHtml(text) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    function configureMarked() {
        if (typeof marked === 'undefined') return false;

        const renderer = new marked.Renderer();

        renderer.heading = function({ tokens, depth }) {
            const text = this.parser.parseInline(tokens);
            return '<h' + depth + ' class="md-h' + depth + '">' + text + '</h' + depth + '>';
        };

        renderer.paragraph = function({ tokens }) {
            const text = this.parser.parseInline(tokens);
            return '<p class="md-p">' + text + '</p>';
        };

        renderer.strong = function({ tokens }) {
            return '<strong class="md-bold">' + this.parser.parseInline(tokens) + '</strong>';
        };

        renderer.em = function({ tokens }) {
            return '<em class="md-italic">' + this.parser.parseInline(tokens) + '</em>';
        };

        renderer.link = function({ href, title, tokens }) {
            const text = this.parser.parseInline(tokens);
            const t = title ? ' title="' + title + '"' : '';
            return '<a class="md-link" href="' + href + '" target="_blank" rel="noopener noreferrer"' + t + '>' + text + '</a>';
        };

        renderer.code = function({ text, lang }) {
            if (lang === 'mermaid') {
                return '<pre class="md-mermaid">' + text + '</pre>';
            }
            return '<pre class="md-codeblock"><code>' + escapeHtml(text) + '</code></pre>';
        };

        renderer.codespan = function({ text }) {
            return '<code class="md-code">' + text + '</code>';
        };

        renderer.list = function({ items, ordered }) {
            const tag = ordered ? 'ol' : 'ul';
            const cls = ordered ? 'md-ol' : 'md-ul';
            const body = items.map(item => this.listitem(item)).join('');
            return '<' + tag + ' class="' + cls + '">' + body + '</' + tag + '>';
        };

        renderer.listitem = function({ tokens }) {
            return '<li class="md-li">' + this.parser.parse(tokens) + '</li>';
        };

        renderer.blockquote = function({ tokens }) {
            return '<blockquote class="md-blockquote">' + this.parser.parse(tokens) + '</blockquote>';
        };

        renderer.hr = function() { return '<hr class="md-hr">'; };

        renderer.table = function({ header, rows }) {
            let h = '<tr>' + header.map(c =>
                '<th class="md-th">' + this.parser.parseInline(c.tokens) + '</th>'
            ).join('') + '</tr>';
            let b = rows.map(r =>
                '<tr>' + r.map(c =>
                    '<td class="md-td">' + this.parser.parseInline(c.tokens) + '</td>'
                ).join('') + '</tr>'
            ).join('');
            return '<div class="md-table-wrapper"><table class="md-table"><thead>' + h + '</thead><tbody>' + b + '</tbody></table></div>';
        };

        renderer.image = function({ href, title, text }) {
            const t = title ? ' title="' + title + '"' : '';
            return '<img class="md-img" src="' + href + '" alt="' + text + '"' + t + ' loading="lazy">';
        };

        marked.setOptions({ renderer: renderer, gfm: true, breaks: false, pedantic: false });
        return true;
    }

    // Configure immediately (marked.min.js is loaded synchronously via <script> tag)
    let configured = false;

    function ensureConfigured() {
        if (!configured && typeof marked !== 'undefined') {
            configured = configureMarked();
        }
        return configured;
    }

    function renderMermaid() {
        if (typeof mermaid === 'undefined') return;
        const blocks = document.querySelectorAll('.md-mermaid');
        blocks.forEach(function(block, i) {
            const id = 'mermaid-' + Date.now() + '-' + i;
            try {
                mermaid.render(id, block.textContent).then(function(result) {
                    block.outerHTML = '<div class="md-mermaid-rendered">' + result.svg + '</div>';
                });
            } catch (e) { console.warn('Mermaid render failed:', e); }
        });
    }

    function parseMarkdown(text) {
        if (!text) return '';

        ensureConfigured();

        if (configured && typeof marked !== 'undefined') {
            let html = marked.parse(text);
            setTimeout(renderMermaid, 100);
            return html;
        }

        // Fallback if marked.js somehow didn't load
        return '<pre style="white-space:pre-wrap;color:#00ff00">' + escapeHtml(text) + '</pre>';
    }

    window.parseMarkdown = parseMarkdown;
})();
