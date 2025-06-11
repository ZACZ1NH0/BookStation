// Cấu hình chung cho biểu đồ
const chartConfig = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom',
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
            bodyFont: { size: 13 }
        }
    }
};

// Biểu đồ doanh thu theo thời gian
function initRevenueChart() {
    try {
        const ctx = document.getElementById('revenueChart').getContext('2d');
        const data = JSON.parse(document.getElementById('revenue-data').textContent);
        console.log('Revenue Data:', data);

        // Sắp xếp dữ liệu theo thời gian và lấy 12 tháng gần nhất
        const sortedData = data.sort((a, b) => new Date(b.month) - new Date(a.month)).slice(0, 12);

        const labels = sortedData.map(item => {
            const date = new Date(item.month);
            return date.toLocaleDateString('vi-VN', { month: 'short', year: 'numeric' });
        }).reverse();

        const values = sortedData.map(item => item.revenue).reverse();

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Doanh thu',
                    data: values,
                    borderColor: '#4e73df',
                    backgroundColor: 'rgba(78, 115, 223, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointRadius: 4,
                    pointBackgroundColor: '#4e73df',
                    pointBorderColor: '#ffffff',
                    pointHoverRadius: 6,
                    pointHoverBorderWidth: 2
                }]
            },
            options: {
                ...chartConfig,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return new Intl.NumberFormat('vi-VN', {
                                    style: 'currency',
                                    currency: 'VND',
                                    maximumSignificantDigits: 3
                                }).format(value);
                            }
                        },
                        grid: {
                            drawBorder: false,
                            color: 'rgba(0, 0, 0, 0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return new Intl.NumberFormat('vi-VN', {
                                    style: 'currency',
                                    currency: 'VND'
                                }).format(context.raw);
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error in initRevenueChart:', error);
    }
}

// Biểu đồ trạng thái đơn hàng
function initOrderStatusChart() {
    try {
        const ctx = document.getElementById('orderStatusChart').getContext('2d');
        const data = JSON.parse(document.getElementById('order-status-data').textContent);
        console.log('Order Status Data:', data);

        const statusColors = {
            'pending': 'rgba(246, 194, 62, 0.8)',      // Vàng
            'processing': 'rgba(54, 185, 204, 0.8)',   // Xanh dương
            'shipping': 'rgba(78, 115, 223, 0.8)',     // Xanh da trời
            'completed': 'rgba(28, 200, 138, 0.8)',    // Xanh lá
            'cancelled': 'rgba(231, 74, 59, 0.8)'      // Đỏ
        };

        const statusLabels = {
            'pending': 'Chờ xử lý',
            'processing': 'Đang xử lý',
            'shipping': 'Đang giao',
            'completed': 'Hoàn thành',
            'cancelled': 'Đã hủy'
        };

        const colors = data.map(item => statusColors[item.status]);
        const labels = data.map(item => statusLabels[item.status] || item.status_display);
        const values = data.map(item => item.count);

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors,
                    borderColor: colors.map(color => color.replace('0.8', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                ...chartConfig,
                cutout: '70%',
                plugins: {
                    ...chartConfig.plugins,
                    tooltip: {
                        ...chartConfig.plugins.tooltip,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((context.raw / total) * 100);
                                return `${context.label}: ${context.raw} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error in initOrderStatusChart:', error);
    }
}

// Biểu đồ phương thức thanh toán
function initPaymentMethodChart() {
    try {
        const ctx = document.getElementById('paymentMethodChart').getContext('2d');
        const data = JSON.parse(document.getElementById('payment-method-data').textContent);
        console.log('Payment Method Data:', data);

        const methodColors = {
            'cash': 'rgba(28, 200, 138, 0.8)',        // Xanh lá
            'bank_transfer': 'rgba(78, 115, 223, 0.8)', // Xanh da trời
            'card': 'rgba(246, 194, 62, 0.8)',        // Vàng
            'momo': 'rgba(231, 74, 59, 0.8)'          // Đỏ
        };

        const methodLabels = {
            'cash': 'Tiền mặt',
            'bank_transfer': 'Chuyển khoản',
            'card': 'Thẻ tín dụng',
            'momo': 'Ví MoMo'
        };

        const colors = data.map(item => methodColors[item.payment_method]);
        const labels = data.map(item => methodLabels[item.payment_method] || item.payment_method);
        const values = data.map(item => item.count);

        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors,
                    borderColor: colors.map(color => color.replace('0.8', '1')),
                    borderWidth: 1
                }]
            },
            options: {
                ...chartConfig,
                plugins: {
                    ...chartConfig.plugins,
                    tooltip: {
                        ...chartConfig.plugins.tooltip,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((context.raw / total) * 100);
                                return `${context.label}: ${context.raw} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error in initPaymentMethodChart:', error);
    }
}

// Khởi tạo biểu đồ khi trang được load
document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('DOM Content Loaded');
        initRevenueChart();
        initOrderStatusChart();
        initPaymentMethodChart();
    } catch (error) {
        console.error('Error initializing charts:', error);
    }
});