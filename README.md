# EDSCC Discord Bot

*EDSCC Discord Bot* is a bot that interacts with [EDSCC](https://beta.edscc.net) to enrich experience by Discord users. Features include notification about event occurred in the game, ranking, etc.

### Features
* Event Notification
* Squadron Ranking
* Commander Ranking within Squadron
* More to be added later

### Requirements
* Python 3.5.3 or higher
* Libraries installed: `discord`, `requests`, `terminaltables`

### Commands

**User**

1. `!link` - Associate discord user account with EDSCC account
2. `!stats` - Commander statistics

**Squadron**

1. `!top50 [combat|trade|exploration]` - Top 50 overall earners

**Admins**

1. `!notify [alert_name] [on|off]` - Activate or deactivate notification alerts defined in the EDSCC squadron settings