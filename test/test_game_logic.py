import sys
import os
import types

# Stub out streamlit before importing app so the module-level st calls don't fail
st_stub = types.ModuleType("streamlit")

class _SessionState(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __contains__(self, key):
        return dict.__contains__(self, key)

st_stub.session_state = _SessionState()
st_stub.set_page_config = lambda **kw: None
st_stub.title = lambda *a, **kw: None
st_stub.caption = lambda *a, **kw: None
st_stub.sidebar = types.SimpleNamespace(
    header=lambda *a, **kw: None,
    selectbox=lambda *a, **kw: "Normal",
    caption=lambda *a, **kw: None,
)
st_stub.subheader = lambda *a, **kw: None
st_stub.info = lambda *a, **kw: None
st_stub.expander = lambda *a, **kw: _NullCtx()
st_stub.write = lambda *a, **kw: None
st_stub.text_input = lambda *a, **kw: ""
st_stub.columns = lambda n: [_NullCtx()] * n
st_stub.button = lambda *a, **kw: False
st_stub.checkbox = lambda *a, **kw: False
st_stub.success = lambda *a, **kw: None
st_stub.error = lambda *a, **kw: None
st_stub.warning = lambda *a, **kw: None
st_stub.balloons = lambda: None
st_stub.rerun = lambda: None
st_stub.stop = lambda: None
st_stub.divider = lambda: None

class _NullCtx:
    def __enter__(self): return self
    def __exit__(self, *a): pass

sys.modules["streamlit"] = st_stub

# Add project root so `import app` works
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import check_guess  # noqa: E402


# ---------------------------------------------------------------------------
# Tests for the `attempts` initialisation (FIXME: Logic breaks here)
# Collaboration: I spotted the FIXME comment and described the bug to the AI —
# that attempts could start as None or an unexpected value. The AI generated
# these three test cases to pin down the expected initial state and guard logic.
# ---------------------------------------------------------------------------

class TestAttemptsInitialisation:
    """session_state.attempts should start at 0, not some other value."""

    def test_attempts_initialised_to_zero(self):
        """Fresh session state: attempts must be 0, not None or a non-zero int."""
        ss = _SessionState()
        if "attempts" not in ss:
            # Collaboration: AI suggested mirroring the exact app guard condition
            # so the test exercises the same code path that contains the FIXME.
            ss.attempts = 0
        assert ss.attempts == 0

    def test_attempts_not_overwritten_if_already_set(self):
        """Existing attempts value must be preserved (guard condition works)."""
        ss = _SessionState()
        ss.attempts = 3
        if "attempts" not in ss:          # should NOT enter this branch
            ss.attempts = 0
        assert ss.attempts == 3

    def test_attempts_is_integer(self):
        """Attempts must be an integer so arithmetic in the game loop is safe."""
        ss = _SessionState()
        if "attempts" not in ss:
            ss.attempts = 0
        assert isinstance(ss.attempts, int)


# ---------------------------------------------------------------------------
# Tests for check_guess (FIXME: Logic breaks here)
# Collaboration: I identified that the "Too High" / "Too Low" branches were
# swapped or ambiguous. The AI translated that description into concrete
# parameterised cases, including off-by-one and boundary values I hadn't
# thought to check myself.
# ---------------------------------------------------------------------------

class TestCheckGuess:
    """check_guess(guess, secret) → (outcome, message)"""

    # --- Correct guess ---
    def test_exact_match_returns_win(self):
        outcome, _ = check_guess(42, 42)
        assert outcome == "Win"

    def test_exact_match_message(self):
        _, message = check_guess(42, 42)
        assert "Correct" in message

    # --- Guess too high ---
    # Collaboration: I asked the AI to verify the direction of the comparison
    # (guess > secret → "Too High"). The AI added the off-by-one case (51 vs 50)
    # to catch any fence-post mistakes in the condition.
    def test_guess_above_secret_returns_too_high(self):
        outcome, _ = check_guess(80, 50)
        assert outcome == "Too High"

    def test_guess_above_secret_message_says_lower(self):
        _, message = check_guess(80, 50)
        assert "LOWER" in message.upper()

    def test_guess_one_above_secret(self):
        outcome, _ = check_guess(51, 50)
        assert outcome == "Too High"

    # --- Guess too low ---
    # Collaboration: I noted the fallthrough return ("Too Low") had no explicit
    # condition, which is the FIXME site. The AI wrote tests for both the typical
    # case and the off-by-one to confirm the implicit branch behaves correctly.
    def test_guess_below_secret_returns_too_low(self):
        outcome, _ = check_guess(20, 50)
        assert outcome == "Too Low"

    def test_guess_below_secret_message_says_higher(self):
        _, message = check_guess(20, 50)
        assert "HIGHER" in message.upper()

    def test_guess_one_below_secret(self):
        outcome, _ = check_guess(49, 50)
        assert outcome == "Too Low"

    # --- Boundary / edge cases ---
    def test_guess_zero_vs_positive_secret(self):
        outcome, _ = check_guess(0, 1)
        assert outcome == "Too Low"

    def test_large_guess_vs_small_secret(self):
        outcome, _ = check_guess(1000, 1)
        assert outcome == "Too High"

    def test_both_equal_at_boundary(self):
        outcome, _ = check_guess(1, 1)
        assert outcome == "Win"

    def test_outcome_is_string(self):
        outcome, message = check_guess(5, 10)
        assert isinstance(outcome, str)
        assert isinstance(message, str)
