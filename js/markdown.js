// GitHub-Flavored Markdown Parser for MarketWizardry.org
// Uses marked.js for full GFM support + mermaid.js for diagrams
// CSP-compliant - loaded from trusted CDN

(function() {
    'use strict';

    // Load marked.js from CDN
    const markedScript = document.createElement('script');
    markedScript.src = 'https://cdn.jsdelivr.net/npm/marked@15.0.7/marked.min.js';

    // Load mermaid.js from CDN
    const mermaidScript = document.createElement('script');
    mermaidScript.src = 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js';

    let markedReady = false;
    let mermaidReady = false;

    markedScript.onload = function() {
        markedReady = true;
        configureMarked();
    };

    mermaidScript.onload = function() {
        mermaidReady = true;
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

    document.head.appendChild(markedScript);
    document.head.appendChild(mermaidScript);

    function configureMarked() {
        if (typeof marked === 'undefined') return;

        // Custom renderer for MarketWizardry.org styling
        const renderer = new marked.Renderer();

        // Headers with md- classes
        renderer.heading = function({ tokens, depth }) {
            const text = this.parser.parseInline(tokens);
            const tag = 'h' + depth;
            return '<' + tag + ' class="md-h' + depth + '">' + text + '</' + tag + '>';
        };

        // Paragraphs
        renderer.paragraph = function({ tokens }) {
            const text = this.parser.parseInline(tokens);
            // Check for mermaid code blocks that got wrapped in <p>
            if (text.startsWith('<pre class="md-mermaid">')) return text;
            return '<p class="md-p">' + text + '</p>';
        };

        // Bold
        renderer.strong = function({ tokens }) {
            const text = this.parser.parseInline(tokens);
            return '<strong class="md-bold">' + text + '</strong>';
        };

        // Italic
        renderer.em = function({ tokens }) {
            const text = this.parser.parseInline(tokens);
            return '<em class="md-italic">' + text + '</em>';
        };

        // Links
        renderer.link = function({ href, title, tokens }) {
            const text = this.parser.parseInline(tokens);
            const titleAttr = title ? ' title="' + title + '"' : '';
            return '<a class="md-link" href="' + href + '" target="_blank" rel="noopener noreferrer"' + titleAttr + '>' + text + '</a>';
        };

        // Code blocks
        renderer.code = function({ text, lang }) {
            if (lang === 'mermaid') {
                return '<pre class="md-mermaid">' + text + '</pre>';
            }
            const langClass = lang ? ' md-code-' + lang : '';
            return '<pre class="md-codeblock' + langClass + '"><code>' + escapeHtml(text) + '</code></pre>';
        };

        // Inline code
        renderer.codespan = function({ text }) {
            return '<code class="md-code">' + text + '</code>';
        };

        // Lists
        renderer.list = function({ items, ordered }) {
            const tag = ordered ? 'ol' : 'ul';
            const cls = ordered ? 'md-ol' : 'md-ul';
            const body = items.map(item => this.listitem(item)).join('');
            return '<' + tag + ' class="' + cls + '">' + body + '</' + tag + '>';
        };

        renderer.listitem = function({ tokens }) {
            const text = this.parser.parse(tokens);
            return '<li class="md-li">' + text + '</li>';
        };

        // Blockquotes
        renderer.blockquote = function({ tokens }) {
            const text = this.parser.parse(tokens);
            return '<blockquote class="md-blockquote">' + text + '</blockquote>';
        };

        // Horizontal rules
        renderer.hr = function() {
            return '<hr class="md-hr">';
        };

        // Tables (GFM)
        renderer.table = function({ header, rows }) {
            let headerHtml = '<tr>' + header.map(cell =>
                '<th class="md-th">' + this.parser.parseInline(cell.tokens) + '</th>'
            ).join('') + '</tr>';

            let bodyHtml = rows.map(row =>
                '<tr>' + row.map(cell =>
                    '<td class="md-td">' + this.parser.parseInline(cell.tokens) + '</td>'
                ).join('') + '</tr>'
            ).join('');

            return '<div class="md-table-wrapper"><table class="md-table"><thead>' +
                headerHtml + '</thead><tbody>' + bodyHtml + '</tbody></table></div>';
        };

        // Images
        renderer.image = function({ href, title, text }) {
            const titleAttr = title ? ' title="' + title + '"' : '';
            return '<img class="md-img" src="' + href + '" alt="' + text + '"' + titleAttr + ' loading="lazy">';
        };

        marked.setOptions({
            renderer: renderer,
            gfm: true,
            breaks: false,
            pedantic: false
        });
    }

    function escapeHtml(text) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    /**
     * Parse markdown text into HTML using marked.js (GFM) with fallback
     */
    function parseMarkdown(text) {
        if (!text) return '';

        // Use marked.js if loaded
        if (markedReady && typeof marked !== 'undefined') {
            let html = marked.parse(text);

            // Process mermaid blocks after render
            setTimeout(function() {
                if (mermaidReady && typeof mermaid !== 'undefined') {
                    const mermaidBlocks = document.querySelectorAll('.md-mermaid');
                    mermaidBlocks.forEach(function(block, i) {
                        const id = 'mermaid-' + Date.now() + '-' + i;
                        try {
                            mermaid.render(id, block.textContent).then(function(result) {
                                block.outerHTML = '<div class="md-mermaid-rendered">' + result.svg + '</div>';
                            });
                        } catch (e) {
                            console.warn('Mermaid render failed:', e);
                        }
                    });
                }
            }, 100);

            return html;
        }

        // Fallback: basic parser if marked.js hasn't loaded yet
        return fallbackParse(text);
    }

    /**
     * Basic fallback parser (used before marked.js loads)
     */
    function fallbackParse(text) {
        let html = escapeHtml(text);
        const lines = html.split('\n');
        let result = [];
        let inList = false;

        for (let i = 0; i < lines.length; i++) {
            let line = lines[i];

            if (line.match(/^## /)) {
                if (inList) { result.push('</ul>'); inList = false; }
                result.push('<h2 class="md-h2">' + line.replace(/^## /, '') + '</h2>');
            } else if (line.match(/^### /)) {
                if (inList) { result.push('</ul>'); inList = false; }
                result.push('<h3 class="md-h3">' + line.replace(/^### /, '') + '</h3>');
            } else if (line.match(/^[-*] /)) {
                if (!inList) { result.push('<ul class="md-ul">'); inList = true; }
                result.push('<li class="md-li">' + line.replace(/^[-*] /, '') + '</li>');
            } else if (line.match(/^---$/)) {
                if (inList) { result.push('</ul>'); inList = false; }
                result.push('<hr class="md-hr">');
            } else if (line.trim() === '') {
                if (inList) { result.push('</ul>'); inList = false; }
                result.push('');
            } else {
                if (inList) { result.push('</ul>'); inList = false; }
                line = line.replace(/\*\*(.+?)\*\*/g, '<strong class="md-bold">$1</strong>');
                line = line.replace(/\*(.+?)\*/g, '<em class="md-italic">$1</em>');
                line = line.replace(/`(.+?)`/g, '<code class="md-code">$1</code>');
                result.push('<p class="md-p">' + line + '</p>');
            }
        }
        if (inList) result.push('</ul>');
        return result.join('\n');
    }

    // Export globally
    window.parseMarkdown = parseMarkdown;
})();
