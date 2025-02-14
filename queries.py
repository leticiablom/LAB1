def build_query(cursor=None):
    """Gera a query GraphQL com paginação opcional."""
    after_clause = f', after: "{cursor}"' if cursor else ''
    
    return f"""
    {{
      search(query: "stars:>10000", type: REPOSITORY, first: 10 {after_clause}) {{
        edges {{
          cursor
          node {{
            ... on Repository {{
              name
              createdAt
              pullRequests(states: MERGED) {{ totalCount }}
              releases {{ totalCount }}
              updatedAt
              primaryLanguage {{ name }}
              issues(first: 100) {{
                totalCount
                nodes {{ state }}
              }}
            }}
          }}
        }}
        pageInfo {{
          hasNextPage
          endCursor
        }}
      }}
    }}
    """
