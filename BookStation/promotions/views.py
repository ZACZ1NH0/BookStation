from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Promotion, PromotionUsage
from decimal import Decimal


@login_required
@require_POST
def apply_promotion_code(request):
    """API để áp dụng mã khuyến mãi"""
    try:
        data = json.loads(request.body)
        promotion_code = data.get('code', '').strip().upper()
        order_amount = Decimal(str(data.get('order_amount', 0)))
        
        if not promotion_code:
            return JsonResponse({
                'success': False,
                'message': 'Vui lòng nhập mã khuyến mãi'
            })
        
        try:
            promotion = Promotion.objects.get(code=promotion_code)
        except Promotion.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Mã khuyến mãi không tồn tại'
            })
        
        # Kiểm tra khuyến mãi có hiệu lực
        if not promotion.is_valid():
            return JsonResponse({
                'success': False,
                'message': 'Mã khuyến mãi đã hết hạn hoặc không hoạt động'
            })
        
        # Kiểm tra user có thể sử dụng
        if not promotion.can_be_used_by_user(request.user):
            return JsonResponse({
                'success': False,
                'message': 'Bạn đã sử dụng hết lượt cho mã khuyến mãi này'
            })
        
        # Tính toán giảm giá
        discount_amount = promotion.calculate_discount(order_amount)
        
        if discount_amount == 0:
            return JsonResponse({
                'success': False,
                'message': f'Đơn hàng phải có giá trị tối thiểu {promotion.min_order_amount:,.0f}đ'
            })
        
        return JsonResponse({
            'success': True,
            'message': 'Áp dụng mã khuyến mãi thành công',
            'data': {
                'promotion_id': promotion.id,
                'promotion_code': promotion.code,
                'promotion_name': promotion.name,
                'discount_amount': float(discount_amount),
                'final_amount': float(order_amount - discount_amount)
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Dữ liệu không hợp lệ'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Có lỗi xảy ra, vui lòng thử lại'
        })


@login_required
def get_valid_promotions(request):
    """Lấy danh sách khuyến mãi có thể sử dụng"""
    now = timezone.now()
    
    # Lấy các khuyến mãi đang hiệu lực
    promotions = Promotion.objects.filter(
        status='active',
        start_date__lte=now,
        end_date__gte=now
    ).order_by('-created_at')
    
    valid_promotions = []
    for promotion in promotions:
        if promotion.can_be_used_by_user(request.user):
            valid_promotions.append({
                'id': promotion.id,
                'code': promotion.code,
                'name': promotion.name,
                'description': promotion.description,
                'discount_type': promotion.discount_type,
                'discount_value': float(promotion.discount_value),
                'min_order_amount': float(promotion.min_order_amount),
                'end_date': promotion.end_date.strftime('%d/%m/%Y %H:%M'),
                'usage_left': promotion.usage_limit_per_user - PromotionUsage.objects.filter(
                    promotion=promotion, 
                    user=request.user
                ).count() if promotion.usage_limit_per_user else None
            })
    
    return JsonResponse({
        'success': True,
        'promotions': valid_promotions
    })


def record_promotion_usage(promotion, user, order_id, discount_amount):
    """Ghi lại việc sử dụng khuyến mãi"""
    PromotionUsage.objects.create(
        promotion=promotion,
        user=user,
        order_id=order_id,
        discount_amount=discount_amount
    )


@login_required
def promotion_list(request):
    """Trang hiển thị danh sách khuyến mãi"""
    now = timezone.now()
    
    # Khuyến mãi đang hiệu lực
    active_promotions = Promotion.objects.filter(
        status='active',
        start_date__lte=now,
        end_date__gte=now
    ).order_by('-created_at')
    
    # Khuyến mãi sắp diễn ra
    upcoming_promotions = Promotion.objects.filter(
        status='active',
        start_date__gt=now
    ).order_by('start_date')
    
    context = {
        'active_promotions': active_promotions,
        'upcoming_promotions': upcoming_promotions,
    }
    
    return render(request, 'promotions/promotion_list.html', context)