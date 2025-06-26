from core.price_tracker import PriceTracker

def test_price_tracker_sma_logic():
    tracker = PriceTracker(window_size=3)

    assert tracker.get_sma() is None

    tracker.add_price(10)
    tracker.add_price(20)
    tracker.add_price(40)
    assert tracker.get_sma() == 23.33

    tracker.add_price(70)
    assert tracker.get_sma() == 43.33