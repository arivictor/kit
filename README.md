# kit.py

<div align="center">
  <img src="docs/logo.png" alt="kit logo" width="150"/>
</div>

*the tiny class-based python api framework*

```python
import kit

k = kit.New()

class Hello:
    def GET(self, request, name):
        return kit.json_response({"hello": name})

if __name__ == "__main__":
    k.run()
```
