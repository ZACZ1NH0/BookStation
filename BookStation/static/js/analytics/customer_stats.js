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
        if (!ctx) {
            console.log('Element customerGrowthChart not found');
            return;
        }

        // Kiểm tra dữ liệu
        if (typeof customerGrowthData === 'undefined' || !Array.isArray(customerGrowthData)) {
            console.log('Customer growth data not available or invalid');
            return;
        }
    
        const labels = customerGrowthData.map(item => {
            if (item.month) {
                const date = new Date(item.month);
                return date.toLocaleDateString('vi-VN', { month: 'short', year: 'numeric' });
            }
            return '';
        });
    
        const values = customerGrowthData.map(item => item.new_users || 0);

        const options = Object.assign({}, chartConfig, {
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0,0,0,0.05)'
                    },
                    ticks: {
                        precision: 0
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        });

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
                    fill: true
                }]
            },
            options: options
        });
    } catch (error) {
        console.error('Error initializing customer growth chart:', error);
    }
}


// Biểu đồ trạng thái khách hàng
function initCustomerStatusChart() {
    try {
        const ctx = document.getElementById('customerStatusChart');
        if (!ctx) {
            console.log('Element customerStatusChart not found');
            return;
        }

        // Kiểm tra dữ liệu
        if (typeof customerStatusData === 'undefined' || typeof customerStatusData !== 'object') {
            console.log('Customer status data not available or invalid');
            return;
        }

        const options = Object.assign({}, chartConfig, {
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                }
            }
        });

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
                        'rgba(28, 200, 138, 0.8)',
                        'rgba(246, 194, 62, 0.8)',
                        'rgba(231, 74, 59, 0.8)'
                    ],
                    borderColor: [
                        'rgba(28, 200, 138, 1)',
                        'rgba(246, 194, 62, 1)',
                        'rgba(231, 74, 59, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: options
        });
    } catch (error) {
        console.error('Error initializing customer status chart:', error);
    }
}

// Khởi tạo tất cả biểu đồ khi trang được load
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing charts...');
    
    // Debug: kiểm tra dữ liệu có sẵn
    console.log('Customer growth data:', typeof customerGrowthData !== 'undefined' ? customerGrowthData : 'undefined');
    console.log('Spending distribution data:', typeof spendingDistributionData !== 'undefined' ? spendingDistributionData : 'undefined');
    console.log('Customer status data:', typeof customerStatusData !== 'undefined' ? customerStatusData : 'undefined');
    
    // Khởi tạo biểu đồ
    initCustomerGrowthChart();
    initCustomerStatusChart();
});