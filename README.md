# General:
* API for requesting blackjack-strategies
* Using untracked .env file for database password etc.

---

# Starting Backend from cmd:
1. env\Scripts\activate
2. cd blackjack_backend
3. .\manage.py runserver
Server available at: http://127.0.0.1:8000/

Database: MySQL
* database runs own seperate MySQL Server
* follow this setup: https://medium.com/@omaraamir19966/connect-django-with-mysql-database-f946d0f6f9e3

---

# Usage:
HTTP POST JSON to http://localhost/api/action
example JSON:
<code>
{
	“player_cards”:[“A”, “10”],	
	“dealer_card”: “6”,
	“nrDecks”: 1,
	“isSoft”: true,
	“isDAS”: true
}
</code>


--- 
# Docker

Using .env file to hide dockerid in docker-compose. File expected at base of project directory.

Command for building image and run container:
* DB not in same container/ remote: <code>docker-compose -f docker-compose.remotedb.yml up -d --build</code>
* ~~DB in same container: <code>docker-compose -f docker-compose.includedb.yml up -d --build</code>~~