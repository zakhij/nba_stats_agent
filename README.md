12/30/24 UPDATE: Due to the limitations of using X API's insanely restrictive free tier (not even able to access mentions timeline!?), this project will be sunset. I would've considered upgrading to the Basic tier to make this work, but alas, it's $200/month. Thanks, Elon. Development will continue on a [Discord-based agent](https://github.com/zakhij/nba-stats-discord-agent) that won't have these API constraints.


# NBA Twitter Agent 

An agentic twitter bot that answers NBA-related statistical queries. Uses Anthropic's SDK to build agents empowered with tools related to the [NBA Stats API](https://github.com/swar/nba_api) and the [Twitter API](https://www.tweepy.org/).



## How it works (WIP)

The project uses two main agents:
- `NBAAgent`: The "basketball expert" equipped with tools that map to NBA Stats API endpoints. When a query comes in, it selects and executes the appropriate tools and returns the NBA statistical data.
- `TweeterAgent`: Takes the data returned by the NBA agent, sanity-checks it as an LLM judge, and then tweets out the response.


## Current Limitations

- The `NBAAgent` has access to a limited set of NBA Stats API endpoints as tools. Need to expand this to answer a wider range of questions.
- Using a free tier of the [X API](https://developer.x.com/en), we can only read 100 tweets a month and write 500 tweets a month. Would need to upgrade to a paid tier to scale this.




