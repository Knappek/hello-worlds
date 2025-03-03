package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

const (
	// dbURL = "postgresql://pgadmin:6UE1k78239Oi0pv45PsD@tcp.172.30.7.140.nip.io:18000/postgres?sslmode=disable"
	dbURL = "postgresql://pgadmin:S429u157D360O8FrMjwK@tcp.172.30.7.140.nip.io:18001/postgres"
)

func main() {
	r := gin.Default()

	// Connect to the database
	db, err := sql.Open("postgres", dbURL)
	if err != nil {
		log.Fatal("Error opening database: ", err)
	}
	defer db.Close()

	// Ensure table exists
	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT)`)
	if err != nil {
		log.Fatal("Error creating table: ", err)
	}

	// Route to serve HTML form
	r.GET("/", func(c *gin.Context) {
		html := `<html><body>
			<form action="/add" method="post">
			<input type="text" name="name" placeholder="Enter name">
			<button type="submit">Submit</button>
			</form>
			</body></html>`
		c.Data(http.StatusOK, "text/html; charset=utf-8", []byte(html))
	})

	// Route to handle form submission
	r.POST("/add", func(c *gin.Context) {
		name := c.PostForm("name")
		if name == "" {
			c.String(http.StatusBadRequest, "Name cannot be empty")
			return
		}
		_, err := db.Exec(`INSERT INTO users (name) VALUES ($1)`, name)
		if err != nil {
			c.String(http.StatusInternalServerError, "Error inserting data")
			return
		}
		c.Redirect(http.StatusSeeOther, "/list")
	})

	// Route to display stored users
	r.GET("/list", func(c *gin.Context) {
		rows, err := db.Query("SELECT id, name FROM users")
		if err != nil {
			c.String(http.StatusInternalServerError, "Error reading data")
			return
		}
		defer rows.Close()

		var users []string
		for rows.Next() {
			var id int
			var name string
			if err := rows.Scan(&id, &name); err != nil {
				c.String(http.StatusInternalServerError, "Error scanning row")
				return
			}
			users = append(users, fmt.Sprintf("%d - %s", id, name))
		}
		c.String(http.StatusOK, "Users:\n%s", users)
	})

	// Start server
	r.Run(":8080")
}
