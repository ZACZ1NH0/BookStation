// Cấu hình chung cho biểu đồ
const chartConfig = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom'
        }
    }
};

// Biểu đồ tăng trưởng khách hàng
function initCustomerGrowthChart() {
    try {
        const ctx = document.getElementById('customerGrowthChart');
        if (!ctx) return;

        const labels = customerGrowthData.map(item => {
            if (item.month) {
                const date = new Date(item.month);
                return date.toLocaleDateString('vi-VN', { month: 'short', year: 'numeric' });
            }
            return '';
        });
    
        const values = customerGrowthData.map(item => item.new_users || 0);

        new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Khách hàng mới',
                    data: values,
                    borderColor: '#4e73df',
                    backgroundColor: 'rgba(78, 115, 223, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2,
                    pointRadius: 4,
                    pointBackgroundColor: '#4e73df',
                    pointBorderColor: '#ffffff',
                    pointHoverRadius: 6,
                    pointHoverBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 15,
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        displayColors: true,
                        titleFont: { size: 13 },
                        bodyFont: { size: 12 }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.05)',
                            drawBorder: false
                        },
                        ticks: {
                            precision: 0,
                            font: { size: 11 }
                        }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { size: 11 } }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error initializing customer growth chart:', error);
    }
}

// Biểu đồ trạng thái khách hàng
function initCustomerStatusChart() {
    try {
        const ctx = document.getElementById('customerStatusChart');
        if (!ctx) return;

        new Chart(ctx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Hoạt động', 'Không hoạt động', 'Chưa mua hàng'],
                datasets: [{
                    data: [
                        customerStatusData.active || 0, 
                        customerStatusData.inactive || 0, 
                        customerStatusData.no_orders || 0
                    ],
                    backgroundColor: [
                        'rgba(28, 200, 138, 0.85)',
                        'rgba(246, 194, 62, 0.85)',
                        'rgba(231, 74, 59, 0.85)'
                    ],
                    borderColor: [
                        'rgba(28, 200, 138, 1)',
                        'rgba(246, 194, 62, 1)',
                        'rgba(231, 74, 59, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                radius: '90%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        align: 'center',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: { size: 12 }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: { size: 14 },
                        bodyFont: { size: 13 },
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((context.raw / total) * 100);
                                return ` ${context.label}: ${context.raw} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error initializing customer status chart:', error);
    }
}

// Khởi tạo biểu đồ khi trang được load
document.addEventListener('DOMContentLoaded', function() {
    initCustomerGrowthChart();
    initCustomerStatusChart();
});