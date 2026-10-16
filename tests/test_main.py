from datetime import date, timedelta

from app.reorder import (
    classify_movement,
    is_consumption,
    average_daily_use,
    reorder_point,
    round_to_pack,
    days_of_cover,
    needs_reorder,
    suggested_order_qty,
)


def test_transfer_is_not_consumption():
    assert classify_movement("transfer_out", -10, "transfer-123") == "transfer"


def test_sale_is_consumption():
    movement = {"kind": "sale", "delta": -5, "transfer_id": None}
    assert is_consumption(movement) is True


def test_receipt_is_not_consumption():
    movement = {"kind": "receipt", "delta": 10, "transfer_id": None}
    assert is_consumption(movement) is False


def test_average_daily_use():
    movements = [
        {"kind": "sale", "delta": -30, "moved_at": date(2026, 10, 10)}
    ]
    assert average_daily_use(movements, date(2026, 10, 13), 30) == 1.0


def test_reorder_point():
    assert reorder_point(2, 10, 5) == 25.0


def test_round_to_pack():
    assert round_to_pack(13, 12) == 24


def test_days_of_cover():
    assert days_of_cover(100, 0) is None


def test_needs_reorder():
    assert needs_reorder(20, 20) is True
    assert needs_reorder(21, 20) is False


def test_suggested_order_qty():
    assert suggested_order_qty(
        on_hand=10,
        avg_daily_use=2,
        lead_time_days=5,
        safety_stock=5,
        review_days=7,
        pack_size=12,
        min_order=0,
        on_order=0,
    ) == 24


def test_no_reorder_when_stock_is_sufficient():
    assert needs_reorder(50, 20) is False
