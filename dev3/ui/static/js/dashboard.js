const Dashboard = {
    init: function(stats) {
        // Global Chart.js Config
        Chart.defaults.font.family = "'Outfit', sans-serif";
        Chart.defaults.color = '#64748b';

        this.renderPerformanceChart(stats.comparison);
        this.renderComplaintsChart(stats.complaints);
        this.renderCollectionChart(stats.revenue_trends);
        this.renderSocietyRevenueChart(stats.summary);
    },

    renderPerformanceChart: function(data) {
        const ctx = document.getElementById('performanceChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.month),
                datasets: [{
                    label: 'Revenue',
                    data: data.map(d => d.revenue),
                    borderColor: '#4f46e5',
                    backgroundColor: 'rgba(79, 70, 229, 0.1)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 3
                }, {
                    label: 'Expenses',
                    data: data.map(d => d.expenses),
                    borderColor: '#ef4444',
                    borderDash: [5, 5],
                    tension: 0.4,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'top', align: 'end' } },
                scales: {
                    y: { beginAtZero: true, grid: { display: false } },
                    x: { grid: { display: false } }
                }
            }
        });
    },

    renderComplaintsChart: function(data) {
        const ctx = document.getElementById('complaintsChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.status),
                datasets: [{
                    data: data.map(d => d.count),
                    backgroundColor: ['#f59e0b', '#10b981', '#3b82f6'],
                    borderWidth: 0,
                    cutout: '70%'
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } }
            }
        });
    },

    renderCollectionChart: function(data) {
        const ctx = document.getElementById('collectionChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(d => d.month),
                datasets: [{
                    label: 'Collected',
                    data: data.map(d => d.actual),
                    backgroundColor: '#10b981',
                    borderRadius: 6
                }, {
                    label: 'Target',
                    data: data.map(d => d.target),
                    backgroundColor: '#e2e8f0',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'top', align: 'end' } },
                scales: {
                    y: { beginAtZero: true, grid: { display: false } },
                    x: { grid: { display: false } }
                }
            }
        });
    },

    renderSocietyRevenueChart: function(data) {
        const ctx = document.getElementById('societyRevenueChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.name),
                datasets: [{
                    data: data.map(d => d.total_collected),
                    backgroundColor: ['#4f46e5', '#8b5cf6', '#ec4899', '#f97316'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'right' } }
            }
        });
    }
};
