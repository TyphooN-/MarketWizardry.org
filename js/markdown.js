// Simple Markdown Parser for MarketWizardry.org
// CSP-compliant - no inline styles or scripts

(function() {
    'use strict';

    /**
     * Parse markdown text into HTML
     * Supports: headers, bold, italic, lists, horizontal rules, links, blockquotes
     * @param {string} text - Markdown text to parse
     * @returns {string} - HTML string
     */
    function parseMarkdown(text) {
        if (!text) return '';

        // Escape HTML to prevent XSS (content is from trusted source but good practice)
        let html = escapeHtml(text);

        // Process line by line for block elements
        const lines = html.split('\n');
        const processedLines = [];
        let inList = false;
        let inOrderedList = false;
        let listItems = [];

        for (let i = 0; i < lines.length; i++) {
            let line = lines[i];

            // Horizontal rules
            if (/^---+$/.test(line.trim()) || /^\*\*\*+$/.test(line.trim())) {
                if (inList || inOrderedList) {
                    processedLines.push(closeList(listItems, inOrderedList));
                    inList = false;
                    inOrderedList = false;
                    listItems = [];
                }
                processedLines.push('<hr class="md-hr">');
                continue;
            }

            // Headers (## and ###)
            const h2Match = line.match(/^##\s+(.+)$/);
            const h3Match = line.match(/^###\s+(.+)$/);

            if (h3Match) {
                if (inList || inOrderedList) {
                    processedLines.push(closeList(listItems, inOrderedList));
                    inList = false;
                    inOrderedList = false;
                    listItems = [];
                }
                processedLines.push('<h3 class="md-h3">' + processInline(h3Match[1]) + '</h3>');
                continue;
            }

            if (h2Match) {
                if (inList || inOrderedList) {
                    processedLines.push(closeList(listItems, inOrderedList));
                    inList = false;
                    inOrderedList = false;
                    listItems = [];
                }
                processedLines.push('<h2 class="md-h2">' + processInline(h2Match[1]) + '</h2>');
                continue;
            }

            // Unordered list items (* or -)
            const ulMatch = line.match(/^[\*\-]\s+(.+)$/);
            if (ulMatch) {
                if (inOrderedList) {
                    processedLines.push(closeList(listItems, true));
                    inOrderedList = false;
                    listItems = [];
                }
                inList = true;
                listItems.push(processInline(ulMatch[1]));
                continue;
            }

            // Ordered list items (1. 2. etc)
            const olMatch = line.match(/^\d+\.\s+(.+)$/);
            if (olMatch) {
                if (inList) {
                    processedLines.push(closeList(listItems, false));
                    inList = false;
                    listItems = [];
                }
                inOrderedList = true;
                listItems.push(processInline(olMatch[1]));
                continue;
            }

            // End of list
            if ((inList || inOrderedList) && line.trim() === '') {
                processedLines.push(closeList(listItems, inOrderedList));
                inList = false;
                inOrderedList = false;
                listItems = [];
                processedLines.push('');
                continue;
            }

            // Blockquotes
            const bqMatch = line.match(/^>\s*(.*)$/);
            if (bqMatch) {
                if (inList || inOrderedList) {
                    processedLines.push(closeList(listItems, inOrderedList));
                    inList = false;
                    inOrderedList = false;
                    listItems = [];
                }
                processedLines.push('<blockquote class="md-blockquote">' + processInline(bqMatch[1]) + '</blockquote>');
                continue;
            }

            // Regular paragraph or empty line
            if (inList || inOrderedList) {
                processedLines.push(closeList(listItems, inOrderedList));
                inList = false;
                inOrderedList = false;
                listItems = [];
            }

            if (line.trim() === '') {
                processedLines.push('');
            } else {
                processedLines.push('<p class="md-p">' + processInline(line) + '</p>');
            }
        }

        // Close any remaining list
        if (inList || inOrderedList) {
            processedLines.push(closeList(listItems, inOrderedList));
        }

        return processedLines.join('\n');
    }

    /**
     * Close a list and return the HTML
     */
    function closeList(items, isOrdered) {
        if (items.length === 0) return '';
        const tag = isOrdered ? 'ol' : 'ul';
        const className = isOrdered ? 'md-ol' : 'md-ul';
        const listHtml = items.map(item => '<li class="md-li">' + item + '</li>').join('\n');
        return '<' + tag + ' class="' + className + '">\n' + listHtml + '\n</' + tag + '>';
    }

    /**
     * Process inline elements (bold, italic, links, code)
     */
    function processInline(text) {
        // Bold **text** or __text__
        text = text.replace(/\*\*([^*]+)\*\*/g, '<strong class="md-bold">$1</strong>');
        text = text.replace(/__([^_]+)__/g, '<strong class="md-bold">$1</strong>');

        // Italic *text* or _text_ (but not inside words)
        text = text.replace(/(?<![*\w])\*([^*]+)\*(?![*\w])/g, '<em class="md-italic">$1</em>');
        text = text.replace(/(?<![_\w])_([^_]+)_(?![_\w])/g, '<em class="md-italic">$1</em>');

        // Inline code `code`
        text = text.replace(/`([^`]+)`/g, '<code class="md-code">$1</code>');

        // Links [text](url)
        text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="md-link" target="_blank" rel="noopener">$1</a>');

        return text;
    }

    /**
     * Escape HTML special characters
     */
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    // Export to global scope
    window.parseMarkdown = parseMarkdown;
})();
