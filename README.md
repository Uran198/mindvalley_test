# mindvalley_test
Technical assignment for mindvalley

Results
-------

1. The project is located in the `cv` subdirectory. Created script to convert JSON into standalone html file.
   You can see the conversation result of my own CV [here](http://uran198.github.io/mindvalley_test/).

2. Used minimax algorithm for 3x3 board and depth based minimax with heuristic score based on position
   for higher dimensions. The project is located in the `tic_tac_toe` subdirectory. The game only has CLI interface.

3. I had never developed multi-server applications, and I have no time to dive into it right now. I have approximate
   idea, though, how I would do it. Approximate architecture:
   - Front end server. On this server I would serve static application, which would take user's url and built shorten
     one, probably, by taking it's hash. After that it would send request with generated url and user's url to the load
     balancer and will be redirected to one of the servers. From this server, application would receive shorten url and
     display it to the user.
   - Load balancer. Each request to this server will contain a shorted url. Based on this url it will distribute the
     load over back end servers. One approach is to use prefix and sort by it.
   - Back end servers. There would be a lot of this servers and each will contain the part of the DB, which will
     include, for example, all links with the same beginning. When an attempt is made to add an url to the database,
     server will check, that it's unique, and if it is not, it will preserve the start, but will try to randomize the
     rest, until, the free one is found and return it with the response.

  Possible drawbacks of this architecture:
  - It is not fault tolerant. If one of the back end servers dies, the users wouldn't be redirected.  
    Posible solution is to duplicate data across some servers. For example, the first server can contain data of the
    third and fourth one and act on it, if they are dead. The load balancer will have to check if servers alive and know
    on which servers which chunks are situated and each server should send it's duplicated data with some period or
    after each request based on the load.  
    If load balancer fails, the front end can have some fallback, or at least apologize to the users and show status
    page.  
    Also, there could be several servers with frontend to make sure that user will see at least something, if several of
    them are down.
  - One load balancer. I'm not sure that only one would handle a lot of requests per second.  
    Possible solution is to have several load balancers and build them in the form of tree. Also, will have to make sure
    that it is fault tolerant, i. e. some nodes can replace another ones.

Statement
---------

1. Your resume/CV in JSON format and a parser for the resume so it can be displayed. We’d like you to submit your resume
   in JSON format, and have an app consume the JSON data and display it. It can be done on web, mobile, or any platform
   or language that you’re most familiar with. You can display it any way you think would be impressive: good
   typography, visualizations, etc. Don’t worry if your design is not as good as you’d like; **we’re mostly interested in
   how you parse the JSON you made** and the pretty rendering is just a bonus.

2. Write a tic-tac-toe app that never loses on a 3x3 board. The app will have a computer player and a human player. The
   computer player should always play the best move and never lose.  
   **Super bonus points** for being able to play on a 4x4 board and a 5x5 board (we will have a very interesting and
   fruitful interview if you do this). As before, you can do it on web, mobile, or any platform or language that you’re
   most familiar with.

3. If you’re applying for a middle or senior developer position (or you just want to do this challenge anyway): Write a
   URL shortener app. The app needs to be on the web and needs to use a database (any kind: relational, non-relational,
   file-based, etc). **Please don’t use online services like bitly or tinyurl**; that’s not the point of this exercise.
   When crafting your solution, take note of the following:
    - if the app becomes famous and you have 10,000 people trying to shorten urls every minute, what would the
      bottlenecks be?
    - how would you work around these bottlenecks?
    - how does the performance characteristics change when you have 500 million new links per month?

  Your URL shortener app needs to be able to address these challenges.
