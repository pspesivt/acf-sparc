# CI/CD Pipeline Templates
## Release Pipeline (.github/workflows/release.yml)
```yaml
name:Create and Publish Release
on:
  workflow_dispatch:
    inputs:
      version_type:
        description:'Semantic version type (major, minor, patch)'
        required:true
        type:choice
        options:[patch,minor,major]
jobs:
  release:
    runs-on:ubuntu-latest
    permissions:
      contents:write
      packages:write
    steps:
      - name:Checkout code
        uses:actions/checkout@v4
      - name:Setup Node.js for standard-version
        uses:actions/setup-node@v4
        with:{node-version:'20'}
      - id:versioning
        name:Bump version and create changelog
        run:"npm install -g standard-version\nstandard-version --release-as ${{inputs.version_type}}\nVERSION=$(jq -r .version package.json)\necho version=${VERSION}>>$GITHUB_OUTPUT"
      - uses:docker/login-action@v3
        with:{registry:ghcr.io,username:${{github.actor}},password:${{secrets.GITHUB_TOKEN}}}
      - run:"IMAGE_ID=ghcr.io/${{github.repository}}\nIMAGE_TAG=${{steps.versioning.outputs.version}}\ndocker build . -t ${IMAGE_ID}:${IMAGE_TAG}\ndocker push ${IMAGE_ID}:${IMAGE_TAG}"
      - run:"git push\ngit push --tags"
      - uses:benc-uk/workflow-dispatch@v1
        with:{workflow:deploy.yml,token:${{secrets.PAT_TOKEN}},inputs:'{"version":"${{steps.versioning.outputs.version}}","environment":"staging"}'}
```
## Deployment Pipeline (.github/workflows/deploy.yml)
```yaml
name:Deploy Release
on:
  workflow_dispatch:
    inputs:
      version:{description:'The exact version tag to deploy (e.g., v1.2.3)',required:true}
      environment:{description:'Target environment',required:true,type:choice,options:[staging,production]}
jobs:
  deploy:
    runs-on:ubuntu-latest
    environment:${{inputs.environment}}
    steps:
      - uses:appleboy/ssh-action@v1.0.0
        name:Deploy to ${{inputs.environment}}
        with:{host:${{secrets.DEPLOY_HOST}},username:deploy,key:${{secrets.DEPLOY_KEY}},script:"IMAGE=ghcr.io/${{github.repository}}:${{inputs.version}}\n/opt/scripts/deploy-app.sh $IMAGE"}
```