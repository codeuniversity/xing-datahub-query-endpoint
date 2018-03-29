from aiohttp import web
import hive_handler
import os
from prometheus_client import start_http_server, Counter

handled_Requests = Counter('hive_query_requests_handled', 'counts the hive query requests partitioned by record type and code', ['record', 'code'])

try:
  os.environ['token']
except Exception:
  raise(ValueError("token not set"))

def parse_params(request):
  query = request.rel_url.query
  params = {}
  try:
    params['limit'] = query['limit']
  except KeyError:
    params['limit'] = 100

  try:
    params['where'] = query['where']
  except KeyError:
    params['where'] = 'True'

  return params

@web.middleware
async def metrics_middleware(request, handler):
  response = await handler(request)
  handled_Requests.labels(request.path[1:], response.status).inc()
  return response

@web.middleware
async def check_token_middleware(request, handler):
  if request.headers.get('access-token') != os.environ['token']:
    print(request.headers.get('access-token'))
    return web.json_response({'error': 'not_allowed'}, status=401)
  return await handler(request)


async def handle_user(request):
  params = parse_params(request)
  data = hive_handler.fetch_users(limit=params['limit'], where=params['where'])
  return web.json_response(data)

async def handle_items(request):
  params = parse_params(request)
  data = hive_handler.fetch_items(limit=params['limit'], where=params['where'])
  return web.json_response(data)

async def handle_interactions(request):
  params = parse_params(request)
  data = hive_handler.fetch_interactions(limit=params['limit'], where=params['where'])
  return web.json_response(data)

async def handle_target_users(request):
  params = parse_params(request)
  data = hive_handler.fetch_target_users(limit=params['limit'], where=params['where'])
  return web.json_response(data)

async def handle_target_items(request):
  params = parse_params(request)
  data = hive_handler.fetch_target_items(limit=params['limit'], where=params['where'])
  return web.json_response(data)

hive_handler.init()
app = web.Application(middlewares=[metrics_middleware,check_token_middleware])

app.router.add_get('/users', handle_user)
app.router.add_get('/items', handle_items)
app.router.add_get('/interactions', handle_interactions)
app.router.add_get('/target_users', handle_target_users)
app.router.add_get('/target_items', handle_target_items)

start_http_server(3004)
web.run_app(app,port=3003)
