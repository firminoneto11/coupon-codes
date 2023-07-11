from fastapi import APIRouter

from .controllers import consume_coupon, register_coupon

router = APIRouter(prefix="v1/")


router.add_api_route(path="coupons/", endpoint=register_coupon, methods=["POST"], status_code=201)
router.add_api_route(path="coupons/{coupon_id}/", endpoint=consume_coupon, methods=["POST"])
