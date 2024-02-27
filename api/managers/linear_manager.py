import json
import os

import requests
from tenacity import retry, stop_after_attempt, wait_random_exponential


class LinearManager:
    def __init__(self, LINEAR_API_KEY=''):
        self.graphql_url = 'https://api.linear.app/graphql'
        self.LINEAR_API_KEY = LINEAR_API_KEY or os.getenv('LINEAR_API_KEY')
        self.headers = {
            "Authorization": self.LINEAR_API_KEY
        }

    def query_grapql(self, query, variables=None):
        r = requests.post(self.graphql_url, json={
            "query": query,
            'variables': variables
        }, headers=self.headers)

        response = json.loads(r.content)

        if 'errors' in response:
            raise Exception(response["errors"])

        return response

    def query_basic_resource(self, resource=''):
        resource_response = self.query_grapql(
            """
                query Resource {""" + resource + """{nodes{id,name}}}
            """
        )

        return resource_response["data"][resource]["nodes"]

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def create_issue(self, title, description='', label_ids=None, project_id='', state_id='', team_id=''):
        create_response = self.query_grapql(
            """
            mutation IssueCreate($input: IssueCreateInput!) {
              issueCreate(input: $input) {
                success
                issue {
                  id
                  title
                  labels {
                    nodes {
                      id
                      name
                    }
                  }
                }
              }
            }
            """,
            variables={
                "input": {
                    "title": title,
                    "description": description,
                    "projectId": project_id,
                    "stateId": state_id,
                    "teamId": team_id,
                    "labelIds": label_ids
                }
            })
        return create_response['data']['issueCreate']

    def query_issue(self, issue_id):
        issue_response = self.query_grapql(
            """
            {{
              issue(id: "{issue_id}") {{
                id
                title
                description
                labels {{
                  nodes {{
                    id
                    name
                  }}
                }}
                state {{
                  name
                }}
              }}
            }}
            """.format(issue_id=issue_id)
        )
        return issue_response['data']

    def teams(self):
        return self.query_basic_resource('teams')

    def states(self):
        return self.query_basic_resource('workflowStates')

    def projects(self):
        return self.query_basic_resource('projects')
