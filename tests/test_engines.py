"""Tests for the input-independent parts of the macro and autoclick engines.

Real mouse/keyboard calls are replaced with mocks, so nothing moves on screen.
"""

from unittest import mock

from swift import auto_engine, macro_engine
from swift.auto_engine import interval_ms
from swift.macro_engine import MacroRecorder


def test_interval_ms_sums_units():
    assert interval_ms(1, 2, 3, 4) == 3_723_004


def test_interval_ms_clamps_negative_parts():
    assert interval_ms(-1, 0, -5, 250) == 250


def test_stop_record_rebases_timestamps_to_first_event():
    rec = MacroRecorder()
    rec.events = [{"t": 2.5, "kind": "move", "x": 1, "y": 1},
                  {"t": 3.0, "kind": "move", "x": 2, "y": 2}]
    with mock.patch.object(macro_engine, "mouse"), mock.patch.object(macro_engine, "keyboard"):
        count = rec.stop_record()
    assert count == 2
    assert [e["t"] for e in rec.events] == [0, 0.5]
    assert rec.recording is False


def test_play_once_dispatches_every_event_kind():
    rec = MacroRecorder()
    rec.events = [
        {"t": 0, "kind": "move", "x": 10, "y": 20},
        {"t": 0, "kind": "mouse", "button": "left", "type": "down"},
        {"t": 0, "kind": "mouse", "button": "left", "type": "up"},
        {"t": 0, "kind": "mouse", "button": "right", "type": "double"},
        {"t": 0, "kind": "wheel", "delta": -1},
        {"t": 0, "kind": "key", "name": "a", "type": "down"},
        {"t": 0, "kind": "key", "name": "a", "type": "up"},
    ]
    steps = []
    with mock.patch.object(macro_engine, "mouse") as m, mock.patch.object(macro_engine, "keyboard") as k:
        rec._play_once(steps.append)
    m.move.assert_called_once_with(10, 20)
    m.press.assert_called_once_with("left")
    m.release.assert_called_once_with("left")
    m.double_click.assert_called_once_with("right")
    m.wheel.assert_called_once_with(-1)
    k.press.assert_called_once_with("a")
    k.release.assert_called_once_with("a")
    assert steps == list(range(1, 8))


def test_play_once_stops_when_flag_set():
    rec = MacroRecorder()
    rec.events = [{"t": 0, "kind": "move", "x": 1, "y": 1}]
    rec.stop_flag.set()
    with mock.patch.object(macro_engine, "mouse") as m, mock.patch.object(macro_engine, "keyboard"):
        rec._play_once()
    m.move.assert_not_called()


def test_play_loop_runs_requested_loops_then_calls_done():
    rec = MacroRecorder()
    rec.events = [{"t": 0, "kind": "wheel", "delta": 1}]
    done = mock.Mock()
    with mock.patch.object(macro_engine, "mouse") as m, mock.patch.object(macro_engine, "keyboard"):
        rec._play_loop({"continuous": False, "loops": 3}, None, done)
    assert m.wheel.call_count == 3
    done.assert_called_once()
    assert rec.playing is False


def test_autoclicker_stops_and_reports_done():
    clicker = auto_engine.AutoClicker()
    done = mock.Mock()

    def click(_btn):
        if clicker.count >= 2:
            clicker.stop()

    with mock.patch.object(auto_engine, "mouse") as m:
        m.click.side_effect = click
        clicker._loop({"interval_ms": 0, "button": "left", "double": False,
                       "target": None, "pos": None}, None, done)
    assert m.click.call_count == 3
    done.assert_called_once_with(3)


def test_autoclicker_stops_at_target_count():
    clicker = auto_engine.AutoClicker()
    done = mock.Mock()
    with mock.patch.object(auto_engine, "mouse") as m:
        clicker._loop({"interval_ms": 0, "button": "right", "double": True,
                       "target": 4, "pos": (5, 6)}, None, done)
    assert m.double_click.call_count == 4
    m.move.assert_called_with(5, 6)
    done.assert_called_once_with(4)
    assert clicker.running is False
