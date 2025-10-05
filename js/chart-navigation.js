// Chart Navigation - CSP Compliant
// Handles back button functionality and Plotly chart rendering for standalone chart pages

(function() {
    'use strict';

    // Render Plotly chart from data attributes (CSP compliant)
    function renderChart() {
        const chartDiv = document.getElementById('chart');
        if (!chartDiv) return;

        const data = chartDiv.getAttribute('data-plotly-data');
        const layout = chartDiv.getAttribute('data-plotly-layout');
        const config = chartDiv.getAttribute('data-plotly-config');

        if (data && layout && config && typeof Plotly !== 'undefined') {
            try {
                // HTML attributes are already unescaped by the browser
                const parsedData = JSON.parse(data);
                const parsedLayout = JSON.parse(layout);
                const parsedConfig = JSON.parse(config);

                Plotly.newPlot('chart', parsedData, parsedLayout, parsedConfig);
            } catch (e) {
                console.error('Error rendering Plotly chart:', e);
                console.error('Data:', data);
                console.error('Layout:', layout);
                console.error('Config:', config);
            }
        }
    }

    // Event delegation for chart back button
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('chart-back-link') ||
            e.target.getAttribute('data-action') === 'chart-back') {
            e.preventDefault();
            window.history.back();
        }
    });

    // Render chart when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', renderChart);
    } else {
        renderChart();
    }
})();
