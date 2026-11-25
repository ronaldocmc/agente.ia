from mcp.server.fastmcp import FastMCP
from comum import consultar_curso
mcp=FastMCP("catalogo-sintetico")
mcp.tool()(consultar_curso)
if __name__=="__main__":mcp.run(transport="stdio")
