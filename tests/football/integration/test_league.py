from unittest import TestCase
from espn_api.football import League

# Integration test to make sure ESPN's API didnt change


class LeagueTest(TestCase):
    LEAUGEID = 777
    CURRENTYEAR = 2022
    PASTYEAR = 2018
    PRIVATEKEYESPN = "%3D"
    PRIVATEKEYSWID = ''

    def test_league_init(self):
        league = League(self.LEAUGEID, self.CURRENTYEAR,
                        self.PRIVATEKEYESPN, self.PRIVATEKEYSWID)

        self.assertEqual(league.current_week, 17)

    def test_past_league(self):
        league = League(self.LEAUGEID, self.PASTYEAR,
                        self.PRIVATEKEYESPN, self.PRIVATEKEYSWID)

        self.assertEqual(league.nfl_week, 18)

    def test_private_league(self):
        # with self.assertRaises(Exception)
        leagueTest = League(self.LEAUGEID, self.CURRENTYEAR,
                            self.PRIVATEKEYESPN, self.PRIVATEKEYSWID)

        self.assertIsInstance(leagueTest, League, "League not retruned")

    def test_unknown_league(self):
        with self.assertRaises(Exception):
            League(2, self.CURRENTYEAR)

    def test_bad_box_scores(self):
        league = League(self.LEAUGEID, self.CURRENTYEAR,
                        self.PRIVATEKEYESPN, self.PRIVATEKEYSWID)

        with self.assertRaises(Exception):
            league.box_scores()

    def test_bad_free_agents(self):
        league = League(self.LEAUGEID, self.CURRENTYEAR,
                        self.PRIVATEKEYESPN, self.PRIVATEKEYSWID)

        with self.assertRaises(Exception):
            league.free_agents()

    def test_box_scores(self):
        league = League(self.LEAUGEID, self.CURRENTYEAR,
                        self.PRIVATEKEYESPN, self.PRIVATEKEYSWID)

        box_scores = league.box_scores(week=2)

        self.assertEqual(repr(box_scores[1].away_team), 'Team(TEAM BERRY)')
        self.assertEqual(repr(box_scores[1].away_lineup[1]),
                         'Player(Odell Beckham Jr., points:29.0, projected:16.72)')
        self.assertEqual(
            repr(box_scores[1]), 'Box Score(Team(TEAM BERRY) at Team(TEAM HOLLAND))')

    def test_player_info(self):
        league = League(self.LEAUGEID, self.CURRENTYEAR,
                        self.PRIVATEKEYESPN, self.PRIVATEKEYSWID)

        # Single ID
        player = league.player_info(playerId=3139477)
        self.assertEqual(player.name, 'Patrick Mahomes')

        # Two ID
        players = league.player_info(playerId=[3139477, 3068267])
        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].name, 'Patrick Mahomes')
        self.assertEqual(players[1].name, 'Austin Ekeler')

    def test_blank_league_init(self):
        blank_league = League(48153503, self.CURRENTYEAR, fetch_league=False)
        self.assertEqual(len(blank_league.teams), 0)
