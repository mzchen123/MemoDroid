from getpass import getpass
from langchain_community.document_loaders.github import GitHubIssuesLoader


token = "your token"


ACCESS_TOKEN = token

loader = GitHubIssuesLoader(
    repo="langchain-ai/langchain",
    access_token=ACCESS_TOKEN,
    include_prs=False,
    state="open",
    since="2023-01-01T00:00:00Z",
)

docs = loader.load()

print(len(docs))


