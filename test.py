import asyncio, os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
VP="/home/debian/deliverables/mcp_products/arkhive_mcp/.venv/bin/python"
H=os.path.dirname(os.path.abspath(__file__))
async def c(s,n,a): return (await s.call_tool(n,a)).content[0].text
async def main():
    p=StdioServerParameters(command=VP,args=[os.path.join(H,"server.py")])
    async with stdio_client(p) as (r,w):
        async with ClientSession(r,w) as s:
            await s.initialize(); print("tools:",[t.name for t in (await s.list_tools()).tools])
            print("\n1 unborn remember -> REFUSED:", await c(s,"remember",{"actor":"nobody","action":"x"}))
            print("\n2 birth:", await c(s,"birth",{"name":"Ember","covenant":["truth over comfort"]}))
            print("\n3 govern(delete, irreversible):", await c(s,"govern",{"action":"delete all","flags":["irreversible"],"rules":[{"trigger":"irreversible","action":"block"}]}))
            print("\n4 born remember -> ALLOWED:", await c(s,"remember",{"actor":"ember-ri-001","action":"context kept forever, freely"}))
            print("\n5 recall:", await c(s,"recall",{"limit":2}))
            print("\n6 verify:", await c(s,"verify",{}))
asyncio.run(main())
