const chartConfig = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom'
        }
    }
};

function initRevenueChart() {
    const ctx = document.getElementById('revenueChart').getContext('2d');
    const data = JSON.parse(document.getElementById('revenue-data').textContent);

    const labels = data.map(item => {
        const date = new Date(item.month);
        return date.toLocaleDateString('vi-VN', { month: 'short', year: 'numeric' });
    }).reverse();

    const values = data.map(item => item.revenue).reverse();

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
                fill: true
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
}

function initOrderStatusChart() {
    const ctx = document.getElementById('orderStatusChart').getContext('2d');
    const data = JSON.parse(document.getElementById('order-status-data').textContent);

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
            cutout: '70%'
        }
    });
}

function initPaymentMethodChart() {
    const ctx = document.getElementById('paymentMethodChart').getContext('2d');
    const data = JSON.parse(document.getElementById('payment-method-data').textContent);

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
        options: chartConfig
    });
}

document.addEventListener('DOMContentLoaded', function() {
    initRevenueChart();
    initOrderStatusChart();
    initPaymentMethodChart();
});