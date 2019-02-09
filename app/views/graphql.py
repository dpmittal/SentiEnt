import graphene

class Query(graphene.ObjectType):
    hello = graphene.String()
    
    def resolve_hello(self, info):
        return 'World'


schema = graphene.Schema(query=Query)

result = schema.execute('''
  query {
    hello
  }
''')
print(result)