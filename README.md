<div align="center">
  <img src="docs/logo.png" alt="kit logo" width="150"/>
</div>

<h3 align="center">kit.py</h3>

<p align="center"><em>the tiny class-based Python API framework</em></p>

---

### 🐱  Why kit?

- Minimal surface — build web APIs with plain classes
- Route methods like `GET`, `POST`, `DELETE` directly
- No decorators, no magic (unless you want it)
- Works with standard Python tooling
- Simple af


### 🚀 Example

```python
import kit

app = kit.New()

class Hello:
    def GET(self, request, name):
        return kit.json_response({"hello": name})

    def POST(self, request):
        return kit.json_response({"message": "Posted!"})

app.route("/hello/{name}", Hello.GET)
app.route("/hello", Hello.POST)

if __name__ == "__main__":
    app.run()
```

### 📦 Installation

```shell
pip install kit-py
```

---

### 💬 Feedback

Open an issue or just say hi.
This project is young, and it’s designed to stay tiny, readable and hackable.

