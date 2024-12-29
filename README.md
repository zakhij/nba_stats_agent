# NBA Twitter Agent 

An agentic twitter bot that answers NBA-related statistical queries. Uses Anthropic's SDK to build agents empowered with tools related to the [NBA Stats API](https://github.com/swar/nba_api) and the [Twitter API](https://www.tweepy.org/).


## How it works (WIP)

The project uses two main agents:
- `NBAAgent`: The "basketball expert" equipped with tools that map to NBA Stats API endpoints. When a query comes in, it selects and executes the appropriate tools and returns the NBA statistical data.
- `TweeterAgent`: Takes the data returned by the NBA agent, sanity-checks it as an LLM judge, and then tweets out the response.


## Current Limitations

- The `TweeterAgent` does not use the Twitter API. We perform a mock tweet (prints to console) for the time being.
- The `NBAAgent` has access to a limited set of NBA Stats API endpoints as tools. Need to expand this to answer a wider range of questions.




