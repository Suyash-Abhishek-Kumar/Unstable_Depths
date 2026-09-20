import unittest

from unstable_depths.engine import Run


class RunTests(unittest.TestCase):
    def test_new_room_costs_integrity_and_counts_progress(self):
        run = Run(1)
        run.move("n")
        self.assertEqual(run.explored, 1)
        self.assertEqual(run.integrity, 292)

    def test_known_room_costs_two_integrity(self):
        run = Run(2)
        run.move("n")
        run.move("s")
        self.assertEqual(run.integrity, 290)
        self.assertEqual(run.position, (0, 0))

    def test_entrance_stays_locked_until_threshold(self):
        run = Run(3)
        self.assertFalse(run.extract())
        self.assertEqual(run.status, "active")
        self.assertFalse(run.unsealed)

    def test_lifeline_forces_forward_route_through_threshold(self):
        run = Run(9)
        direction = "n"
        for _ in range(run.threshold):
            self.assertIn(direction, run.room.exits)
            run.move(direction)
        self.assertEqual(run.explored, run.threshold)
        self.assertTrue(run.unsealed)

    def test_anchor_never_raises_integrity_above_starting_value(self):
        run = Run(5)
        room = run._make_room((0, 1), "n")
        room.kind = "anchor"
        run.rooms[(0, 0)].exits.add("n")
        run.move("n")
        self.assertLessEqual(run.integrity, run.starting_integrity)

    def test_anchor_pity_increases_and_resets(self):
        run = Run(7)
        self.assertEqual(run.anchor_pity, 0)
        run._make_room((0, 1), "n")
        self.assertGreaterEqual(run.anchor_pity, 0)
        run.anchor_pity = 10
        # A generated anchor resets the pity counter.
        original_kind = run.weighted_kind
        run.weighted_kind = lambda: "anchor"
        run._make_room((0, 2), "n")
        self.assertEqual(run.anchor_pity, 0)
        run.weighted_kind = original_kind

    def test_symptom_cutoffs_are_percentages_of_starting_integrity(self):
        run = Run(8)
        run.integrity = 211
        self.assertFalse(run.integrity <= run.starting_integrity * 0.70)
        run.integrity = 210
        self.assertTrue(run.integrity <= run.starting_integrity * 0.70)

    def test_score_only_banks_on_extraction(self):
        run = Run(6)
        run.loot = 8
        run.explored = 4
        self.assertEqual(run.score(), 0)
        run.status = "extracted"
        self.assertEqual(run.score(), 32)


if __name__ == "__main__":
    unittest.main()
