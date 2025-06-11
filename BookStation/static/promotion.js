// Promotion management functions
class PromotionManager {
    constructor() {
        this.appliedPromotion = null;
        this.originalTotal = 0;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadValidPromotions();
    }

    bindEvents() {
        // Apply promotion code button
        const applyBtn = document.getElementById('apply-promotion-btn');
        if (applyBtn) {
            applyBtn.addEventListener('click', () => this.applyPromotionCode());
        }

        // Remove promotion button
        const removeBtn = document.getElementById('remove-promotion-btn');
        if (removeBtn) {
            removeBtn.addEventListener('click', () => this.removePromotion());
        }

        // Enter key on promotion input
        const promotionInput = document.getElementById('promotion-code');
        if (promotionInput) {
            promotionInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.applyPromotionCode();
                }
            });
        }

        // Quick apply promotion buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('quick-apply-promotion')) {
                e.preventDefault();
                const code = e.target.getAttribute('data-code');
                this.quickApplyPromotion(code);
            }
        });
    }

    async loadValidPromotions() {
        try {
            const response = await fetch('/promotions/valid-promotions/', {
                method: 'GET',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.displayValidPromotions(data.promotions);
                }
            }
        } catch (error) {
            console.error('Error loading promotions:', error);
        }
    }

    displayValidPromotions(promotions) {
        const container = document.getElementById('valid-promotions-list');
        if (!container || promotions.length === 0) return;

        const html = promotions.map(promotion => `
            <div class="promotion-item mb-2">
                <div class="card border-success">
                    <div class="card-body p-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong class="text-success">${promotion.code}</strong>
                                <small class="text-muted d-block">${promotion.name}</small>
                                <small class="text-info">
                                    Giảm ${promotion.discount_type === 'percentage' ? 
                                        promotion.discount_value + '%' : 
                                        this.formatCurrency(promotion.discount_value)}
                                    ${promotion.min_order_amount > 0 ? 
                                        ` - Đơn tối thiểu ${this.formatCurrency(promotion.min_order_amount)}` : ''}
                                </small>
                            </div>
                            <button class="btn btn-sm btn-outline-success quick-apply-promotion" 
                                    data-code="${promotion.code}">
                                Áp dụng
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        container.innerHTML = `
            <h6 class="text-success">Khuyến mãi có thể sử dụng:</h6>
            ${html}
        `;
    }

    async applyPromotionCode() {
        const codeInput = document.getElementById('promotion-code');
        const code = codeInput.value.trim().toUpperCase();

        if (!code) {
            this.showMessage('Vui lòng nhập mã khuyến mãi', 'warning');
            return;
        }

        const orderAmount = this.getOrderTotal();
        if (orderAmount <= 0) {
            this.showMessage('Không có sản phẩm trong giỏ hàng', 'warning');
            return;
        }

        this.setLoading(true);

        try {
            const response = await fetch('/promotions/apply-code/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: code,
                    order_amount: orderAmount
                })
            });

            const data = await response.json();

            if (data.success) {
                this.appliedPromotion = data.data;
                this.updateOrderSummary();
                this.showMessage(data.message, 'success');
                this.showPromotionDetails();
                codeInput.value = '';
            } else {
                this.showMessage(data.message, 'error');
            }
        } catch (error) {
            console.error('Error applying promotion:', error);
            this.showMessage('Có lỗi xảy ra, vui lòng thử lại', 'error');
        } finally {
            this.setLoading(false);
        }
    }

    quickApplyPromotion(code) {
        const codeInput = document.getElementById('promotion-code');
        if (codeInput) {
            codeInput.value = code;
            this.applyPromotionCode();
        }
    }

    removePromotion() {
        this.appliedPromotion = null;
        this.updateOrderSummary();
        this.hidePromotionDetails();
        this.showMessage('Đã hủy mã khuyến mãi', 'info');
    }

    updateOrderSummary() {
        const subtotalElement = document.getElementById('order-subtotal');
        const discountElement = document.getElementById('order-discount');
        const totalElement = document.getElementById('order-total');

        if (!subtotalElement || !totalElement) return;

        const subtotal = this.getOrderTotal();
        let discount = 0;
        let total = subtotal;

        if (this.appliedPromotion) {
            discount = this.appliedPromotion.discount_amount;
            total = this.appliedPromotion.final_amount;
        }

        // Update display
        subtotalElement.textContent = this.formatCurrency(subtotal);
        totalElement.textContent = this.formatCurrency(total);

        if (discountElement) {
            if (discount > 0) {
                discountElement.parentElement.style.display = 'flex';
                discountElement.textContent = '-' + this.formatCurrency(discount);
            } else {
                discountElement.parentElement.style.display = 'none';
            }
        }
    }

    showPromotionDetails() {
        const container = document.getElementById('applied-promotion-details');
        if (!container || !this.appliedPromotion) return;

        container.innerHTML = `
            <div class="alert alert-success d-flex justify-content-between align-items-center">
                <div>
                    <i class="fas fa-check-circle"></i>
                    <strong>${this.appliedPromotion.promotion_code}</strong> - ${this.appliedPromotion.promotion_name}
                    <br><small>Giảm ${this.formatCurrency(this.appliedPromotion.discount_amount)}</small>
                </div>
                <button type="button" id="remove-promotion-btn" class="btn btn-sm btn-outline-danger">
                    <i class="fas fa-times"></i> Hủy
                </button>
            </div>
        `;

        // Re-bind remove button event
        const removeBtn = container.querySelector('#remove-promotion-btn');
        if (removeBtn) {
            removeBtn.addEventListener('click', () => this.removePromotion());
        }

        container.style.display = 'block';
    }

    hidePromotionDetails() {
        const container = document.getElementById('applied-promotion-details');
        if (container) {
            container.style.display = 'none';
            container.innerHTML = '';
        }
    }

    getOrderTotal() {
        // Get total from order summary or calculate from cart items
        const totalElement = document.getElementById('cart-total') || 
                           document.getElementById('order-subtotal') ||
                           document.querySelector('[data-order-total]');
        
        if (totalElement) {
            const totalText = totalElement.textContent || totalElement.getAttribute('data-order-total');
            return parseFloat(totalText.replace(/[^\d.-]/g, '')) || 0;
        }

        // Fallback: calculate from individual items
        let total = 0;
        document.querySelectorAll('[data-item-total]').forEach(item => {
            const itemTotal = parseFloat(item.getAttribute('data-item-total')) || 0;
            total += itemTotal;
        });

        return total;
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND',
            minimumFractionDigits: 0
        }).format(amount);
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
               document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
               '';
    }

    setLoading(loading) {
        const btn = document.getElementById('apply-promotion-btn');
        if (!btn) return;

        if (loading) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang xử lý...';
        } else {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-tags"></i> Áp dụng';
        }
    }

    showMessage(message, type) {
        const container = document.getElementById('promotion-messages') || 
                         document.querySelector('.alert-container') ||
                         document.body;

        const alertClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        }[type] || 'alert-info';

        const alert = document.createElement('div');
        alert.className = `alert ${alertClass} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert at the beginning of container
        container.insertBefore(alert, container.firstChild);

        // Auto dismiss after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    // Method to get applied promotion data for order submission
    getAppliedPromotionData() {
        return this.appliedPromotion;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('promotion-code') || document.getElementById('valid-promotions-list')) {
        window.promotionManager = new PromotionManager();
    }
});