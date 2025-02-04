# mcp-webinar

## Level one

![Level 1](./docs/l1.jpg)



- https://github.com/motherduckdb/mcp-server-motherduck
- https://huggingface.co/datasets/ibm-research/nestful
- https://duckdb.org/2024/05/29/access-150k-plus-datasets-from-hugging-face-with-duckdb.html


## Level Two

![Level 2](./docs/l2.jpg)


```
uv pip install "mcp[cli]"
mcp install ./src/server_github.py 
```


- https://github.com/kyryl-opens-ml/ml-in-production-practice/


## Level Three

![Level 3](./docs/l2.jpg)

```
uv run ./src/client_custom.py ./src/server_github.py
```

## Debug

```
npx @modelcontextprotocol/inspector uvx mcp-server-motherduck
mcp dev ./src/server_github.py 
```

