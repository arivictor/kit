import kit

app = kit.New()

class Hello:
    def GET(self, request, name):
        return kit.json_response({"message": f"Hello, {name}!"})

    def POST(self, request):
        return kit.json_response({"message": "Hello, World!"})
    
if __name__ == "__main__":
    app.route("/hello/{name}", Hello.GET)
    app.route("/hello", Hello.POST)
    app.run(host="localhost", port=8000)