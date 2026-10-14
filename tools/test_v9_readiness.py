"""Regression checks: 500 academic approvals are necessary, not sufficient."""
from v9_checkpoint import release_ready

def main():
    approved = [dict(status='確認済み') for _ in range(500)]
    passed = dict(questions=500, answers=500,
                  full_visual_qa_completed=True, release_ready=True)
    assert release_ready(approved, passed)
    for patch in [dict(full_visual_qa_completed=False), dict(release_ready=False),
                  dict(questions=499), dict(answers=499)]:
        assert not release_ready(approved, passed | patch)
    assert not release_ready(approved[:-1], passed)
    assert not release_ready([dict(status='要追加確認')] + approved[1:], passed)
    assert not release_ready(approved, {})
    print('readiness gate: 8 cases passed')

if __name__ == '__main__':
    main()
